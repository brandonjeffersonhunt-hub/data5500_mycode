import requests
import networkx as nx

#pick coins
COINS = [
    "ethereum",
    "bitcoin",
    "litecoin",
    "ripple",
    "cardano",
    "bitcoin-cash",
    "eos",
]

#set tickers
TICKERS = [
    "eth",
    "btc",
    "ltc",
    "xrp",
    "ada",
    "bch",
    "eos",
]

#write a function to fetch the prices
def fetch_prices():
    ids_param = ",".join(COINS)
    vs_param = ",".join(TICKERS)

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids_param}&vs_currencies={vs_param}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


#match tickers and IDs
ID_TO_TICKER = {
    "ethereum": "eth",
    "bitcoin": "btc",
    "litecoin": "ltc",
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
}

#build the graph
def build_prices_graph(prices: dict) -> nx.DiGraph:
    g = nx.DiGraph()

    for ticker in TICKERS:
        g.add_node(ticker)

    for coin_id, rate_dict in prices.items():
        from_ticker = ID_TO_TICKER[coin_id]

        for to_ticker, rate in rate_dict.items():
            if to_ticker in TICKERS and rate is not None and rate > 0:
                g.add_edge(from_ticker, to_ticker, weight=rate)

    return g

#path weight
def compute_path_weight(graph: nx.DiGraph, path: list[str]) -> float:
    weight = 1.0
    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]
        weight *= graph[a][b]['weight']
    return weight

def get_all_paths(graph, source: str, target: str):
    return list(nx.all_simple_paths(graph, source, target))

#find paths
def find_all_paths(graph):
    all_results = []

    for source in TICKERS:
        for target in TICKERS:
            if source == target:
                continue

            paths = get_all_paths(graph, source, target)

            for path in paths:
                forward_weight = compute_path_weight(graph, path)

                reverse_path = list(reversed(path)) #--------------------> Chat gpt addition

                valid_reverse = True
                for i in range(len(reverse_path) - 1):
                    a = reverse_path[i]
                    b = reverse_path[i + 1]
                    if not graph.has_edge(a, b):
                        valid_reverse = False
                        break

                if not valid_reverse:
                    continue

                reverse_weight = compute_path_weight(graph, reverse_path)

                factor = forward_weight * reverse_weight

                all_results.append({
                    "from": source,
                    "to": target,
                    "path": path,
                    "forward_weight": forward_weight,
                    "reverse_path": reverse_path,
                    "reverse_weight": reverse_weight,
                    "factor": factor,
                })

    return all_results


#pretty summary
def print_arbitrage_summary(results):
    if not results:
        print("No paths found")
        return

    # FIXED: use x['factor'], NOT x[factor] -----------------------> CHat gpt fix
    sorted_results = sorted(results, key=lambda x: x["factor"])
    smallest = sorted_results[0]
    largest = sorted_results[-1]

    print("\n==============================")
    print("      ARBITRAGE SUMMARY")
    print("==============================")

    print("\nBEST Arbitrage (factor ABOVE 1.0):")
    print(f"Factor: {largest['factor']:.10f}")
    print("Forward path:", " ---> ".join(largest['path']))
    print("Reverse path:", " ---> ".join(largest['reverse_path']))

    print("\nWORST Arbitrage (factor BELOW 1.0):")
    print(f"Factor: {smallest['factor']:.10f}")
    print("Forward path:", " ---> ".join(smallest['path']))
    print("Reverse path:", " ---> ".join(smallest['reverse_path']))

    print("\n==============================\n")


if __name__ == "__main__":
    prices = fetch_prices()
    g = build_prices_graph(prices)
    results = find_all_paths(g)

    #print first 10
    for r in results[:10]:
        print(r)

    print_arbitrage_summary(results)
