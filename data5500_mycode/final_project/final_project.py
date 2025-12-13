from __future__ import annotations

import os
import json
import math
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import pytz
import requests
import networkx as nx


# -----------------------------
# CONFIGURATION
# -----------------------------

# 7 original + 6 more = 13 coins total
COINS: List[str] = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "cardano",
    "bitcoin-cash",
    "eos",
    "solana",
    "polkadot",
    "chainlink",
    "stellar",
    "dogecoin",
    "avalanche-2",
]

# CoinGecko coin ID -> ticker label used as graph nodes
ID_TO_TICKER: Dict[str, str] = {
    "bitcoin": "btc",
    "ethereum": "eth",
    "litecoin": "ltc",
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
    "solana": "sol",
    "polkadot": "dot",
    "chainlink": "link",
    "stellar": "xlm",
    "dogecoin": "doge",
    "avalanche-2": "avax",
}

#only make a trade if the profit arbitrage meets this threshold
MIN_PROFIT_RATIO: float = 1.01  # 0.01%

#paper trade sizing
USD_NOTIONAL_PER_LEG: float = 50.0

#output locations in final_project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_PATH = os.path.join(BASE_DIR, "results.json")

#time zone
ET = pytz.timezone("America/Denver")


#DATA STRUCTURES
@dataclass
class CycleResult:
    """Stores one detected arbitrage cycle and its computed profitability."""
    cycle: List[str]                       # e.g., ["btc","eth","xlm","btc"]
    profit_ratio: float                    # multiplicative
    profit_percent: float                  # (profit_ratio-1)*100
    edges: List[Tuple[str, str, float]]    # (from,to,rate) along cycle


@dataclass
class TradeAttempt:
    """Stores whether we submitted paper orders and what happened."""
    attempted: bool
    reason: str
    orders: List[dict]


#FETCH COIN GECKO

def fetch_prices_coingecko(ids: List[str], vs: List[str], timeout: int = 20) -> dict:
    """
    Calls CoinGecko /simple/price to get a JSON matrix of coin-to-coin prices.
    Includes retry + exponential backoff to handle CoinGecko 429 rate limits.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(ids), "vs_currencies": ",".join(vs)}

    max_retries = 6
    base_sleep = 2.0  #seconds

    for attempt in range(max_retries):
        r = requests.get(url, params=params, timeout=timeout)

        #if success
        if r.status_code == 200:
            return r.json()

        #if limited: wait and retry
        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After")
            if retry_after is not None:
                sleep_s = float(retry_after)
            else:
                sleep_s = base_sleep * (2 ** attempt)

            print(f"[WARN] CoinGecko rate limited (429). Sleeping {sleep_s:.1f}s then retrying...")
            time.sleep(sleep_s)
            continue

        #other
        r.raise_for_status()

    raise RuntimeError("CoinGecko 429: exceeded max retries; try again later.")


def build_exchange_rates(price_json: dict) -> Dict[Tuple[str, str], float]:
    """
    Convert CoinGecko JSON to directed exchange rates:
      rate[(a,b)] = units of b you receive for 1 unit of a
    """
    rates: Dict[Tuple[str, str], float] = {}
    ticker_to_id = {v: k for k, v in ID_TO_TICKER.items()}
    tickers = [ID_TO_TICKER[c] for c in COINS]

    for from_ticker in tickers:
        from_id = ticker_to_id[from_ticker]
        if from_id not in price_json:
            continue

        for to_ticker in tickers:
            if to_ticker == from_ticker:
                continue

            if to_ticker in price_json[from_id]:
                rate = float(price_json[from_id][to_ticker])
                if rate > 0:
                    rates[(from_ticker, to_ticker)] = rate

    return rates


def save_rates_snapshot(rates: Dict[Tuple[str, str], float]) -> str:
    """
    Save raw currency pair data to EC2:
      data/currency_pair_YYYY.MM.DD_HH.MM.txt
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    ts = datetime.now(ET).strftime("%Y.%m.%d_%H.%M")
    path = os.path.join(DATA_DIR, f"currency_pair_{ts}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write("currency_from,currency_to,exchange_rate\n")
        for (a, b), r in sorted(rates.items()):
            f.write(f"{a},{b},{r}\n")

    return path


# ARBITRAGE ANALYSIS // nEGATIVE CYCLE DETECTION

def build_graph_for_arbitrage(rates: Dict[Tuple[str, str], float]) -> nx.DiGraph:
    """
    Convert multiplicative arbitrage into additive weights:
      weight = -log(rate)
    Negative cycle => product(rates) > 1 => arbitrage opportunity.
    """
    G = nx.DiGraph()
    for (a, b), r in rates.items():
        G.add_edge(a, b, rate=r, weight=-math.log(r))
    return G


def extract_cycle_bellman_ford(H: nx.DiGraph, source: str) -> Optional[List[str]]:
    """
    Bellman-Ford with predecessor tracking to reconstruct a negative cycle.
    """
    nodes = list(H.nodes())
    dist = {n: float("inf") for n in nodes}
    pred = {n: None for n in nodes}
    dist[source] = 0.0

    # Relax edges |V|-1 times
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, data in H.edges(data=True):
            w = data.get("weight", 0.0)
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break

    #detect a node affected by negative cycle
    cycle_start = None
    for u, v, data in H.edges(data=True):
        w = data.get("weight", 0.0)
        if dist[u] + w < dist[v]:
            cycle_start = v
            pred[v] = u
            break

    if cycle_start is None:
        return None

    #ensure in cucle
    x = cycle_start
    for _ in range(len(nodes)):
        x = pred[x]
        if x is None:
            return None

    #collect nodes
    cycle = [x]
    cur = pred[x]
    while cur is not None and cur not in cycle:
        cycle.append(cur)
        cur = pred[cur]

    if cur is None:
        return None

    cycle.append(cur)
    cycle = list(reversed(cycle))

    #close loop
    cycle = [n for n in cycle if n != source and n != "__SOURCE__"]
    if cycle and cycle[0] != cycle[-1]:
        cycle.append(cycle[0])

    return cycle if len(cycle) >= 4 else None


def find_negative_cycle(G: nx.DiGraph) -> Optional[List[str]]:
    """
    Adds a super-source so all nodes are reachable, then checks for negative cycles.
    """
    nodes = list(G.nodes())
    if not nodes:
        return None

    super_source = "__SOURCE__"
    H = G.copy()
    H.add_node(super_source)
    for n in nodes:
        H.add_edge(super_source, n, weight=0.0, rate=1.0)

    try:
        nx.single_source_bellman_ford_path_length(H, super_source, weight="weight")
        return None
    except nx.NetworkXUnbounded:
        return extract_cycle_bellman_ford(H, super_source)


def evaluate_cycle(G: nx.DiGraph, cycle: List[str]) -> CycleResult:
    """
    Multiply rates along the cycle to compute total profit ratio.
    """
    edges: List[Tuple[str, str, float]] = []
    profit = 1.0

    for i in range(len(cycle) - 1):
        a, b = cycle[i], cycle[i + 1]
        r = G[a][b]["rate"]
        edges.append((a, b, r))
        profit *= r

    return CycleResult(
        cycle=cycle,
        profit_ratio=profit,
        profit_percent=(profit - 1.0) * 100.0,
        edges=edges,
    )


#ALPACA PAPER TRADING

def alpaca_client():
    """
    Create Alpaca TradingClient using env vars.
    Returns None if keys are missing.
    """
    api_key = os.getenv("ALPACA_API_KEY")
    secret = os.getenv("ALPACA_SECRET_KEY")
    is_paper = os.getenv("ALPACA_PAPER", "true").lower() == "true"

    if not api_key or not secret:
        return None

    from alpaca.trading.client import TradingClient
    return TradingClient(api_key, secret, paper=is_paper)


def attempt_paper_trade_cycle(cycle: CycleResult) -> TradeAttempt:
    """
    Submit PAPER orders when a profitable cycle is detected.

    Alpaca crypto is typically quoted vs USD (e.g., BTCUSD), not coin->coin.
    We use a simple USD-bridged approach: for each edge (a -> b), submit a
    USD-notional BUY order for the destination coin b.
    """
    client = alpaca_client()
    if client is None:
        return TradeAttempt(False, "Missing Alpaca keys (ALPACA_API_KEY / ALPACA_SECRET_KEY).", [])

    ALPACA_SUPPORTED = {"btc", "eth", "ltc", "doge", "sol", "avax", "dot", "link", "xlm", "bch", "ada", "eos"}

    cycle_tickers = cycle.cycle[:-1]  #ignore the repeated final node
    if not all(t in ALPACA_SUPPORTED for t in cycle_tickers):
        return TradeAttempt(False, f"Skipped trade: unsupported coin in cycle {cycle_tickers}.", [])

    orders: List[dict] = []
    try:
        from alpaca.trading.requests import MarketOrderRequest
        from alpaca.trading.enums import OrderSide, TimeInForce

        for (_a, b, _r) in cycle.edges:
            symbol = f"{b.upper()}USD"
            req = MarketOrderRequest(
                symbol=symbol,
                notional=USD_NOTIONAL_PER_LEG,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.GTC,
            )
            o = client.submit_order(req)
            orders.append({"symbol": symbol, "notional": USD_NOTIONAL_PER_LEG, "alpaca_order_id": str(o.id)})
            time.sleep(0.25)

        return TradeAttempt(True, "Submitted USD-notional BUY orders (USD-bridged).", orders)

    except Exception as e:
        return TradeAttempt(True, f"Trade submission error: {e}", orders)



#OUTPUt RESULTS

def write_results_json(snapshot_path: str, cycle_result: Optional[CycleResult], trade: TradeAttempt) -> None:
    """
    Store run output to results.json for grading.
    """
    payload = {
        "timestamp_et": datetime.now(ET).isoformat(),
        "snapshot_file": snapshot_path,
        "coins_ids": COINS,
        "coins_tickers": [ID_TO_TICKER[c] for c in COINS],
        "min_profit_ratio": MIN_PROFIT_RATIO,
        "best_cycle": asdict(cycle_result) if cycle_result else None,
        "paper_trade": asdict(trade),
    }
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


#MAIN PROGRAM

def main() -> None:
    tickers = [ID_TO_TICKER[c] for c in COINS]

    # 1) Fetch latest data from CoinGecko JSON API
    price_json = fetch_prices_coingecko(COINS, tickers)

    # 2) Build exchange rates and save raw snapshot file to EC2
    rates = build_exchange_rates(price_json)
    snapshot_path = save_rates_snapshot(rates)

    # 3) Detect arbitrage cycle using negative-cycle detection
    G = build_graph_for_arbitrage(rates)
    cycle_nodes = find_negative_cycle(G)

    best_cycle: Optional[CycleResult] = None
    trade_attempt = TradeAttempt(False, "No trade attempted.", [])

    if cycle_nodes:
        best_cycle = evaluate_cycle(G, cycle_nodes)

        if best_cycle.profit_ratio >= MIN_PROFIT_RATIO:
            trade_attempt = attempt_paper_trade_cycle(best_cycle)
        else:
            trade_attempt = TradeAttempt(
                False,
                f"Cycle found but below threshold: {best_cycle.profit_ratio:.6f}",
                [],
            )
    else:
        trade_attempt = TradeAttempt(False, "No negative cycle detected.", [])


#Save json results
    write_results_json(snapshot_path, best_cycle, trade_attempt)

    #Summary for the video
    print(f"[OK] Saved snapshot: {snapshot_path}")
    print(f"[OK] Updated results: {RESULTS_PATH}")
    print(f"[TRADE] {trade_attempt.reason}")
    if best_cycle:
        print(f"[CYCLE] profit_ratio={best_cycle.profit_ratio:.6f} profit%={best_cycle.profit_percent:.4f}")
        print(f"[CYCLE] path={' -> '.join(best_cycle.cycle)}")
    else:
        print("[CYCLE] None")


if __name__ == "__main__":
    main()