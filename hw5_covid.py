import json
import cloudscraper
from collections import defaultdict
import os

#create list of states
scraper = cloudscraper.create_scraper()

state_codes = [
    'al', 'ar', 'as', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'gu',
    'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi',
    'mn', 'mo', 'mp', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv',
    'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut',
    'va', 'vi', 'vt', 'wa', 'wi', 'wv', 'wy'
]

BASE_URL =  "https://api.covidtracking.com/v1/states/"      #base URL to add the states to for each state code

#format the date into a readable string
def format_date(date_int):
    s = str(date_int)
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"

#function to fetch the data from api
def fetch_data(state_code):
    url = f"{BASE_URL}{state_code}/daily.json"
    print(f"\n{'~'*30}")                                                  #print a ~ as the separator for easier reading
    print(f"State: {state_code.upper()}")
    print(f"Using Url {url}")

    try:
        response = scraper.get(url, timeout = 10)                     #chat helped me with this because I have not used cloudscraper before
        response.raise_for_status()
        data = response.json()

        folder = "states_data"                  #create a folder. The first time i had the states being saved everywhere and it was annoying and messy
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{state_code}.json")                #make sure the state data is stored in its own file/folder
        with open(file_path, 'w') as f:                   #open the file in write mode
            json.dump(data, f, indent = 4)

        print(f"Data saved to: {file_path}")            #confirm data is saved
        return data
    
    except Exception as e:                                  #error catch
        print(f"Error fetching {state_code}: {e}")
        return None
        
def analyze(state_code, data):                                              #function to loop through api and pull new cases for each state and puts them in a list
    daily_new_cases = [day.get("positiveIncrease", 0) for day in data]

    if not daily_new_cases:                                                  #unless theres no cases
        print(f"No new data for {state_code.upper()}")
        return

    avg_daily = sum(daily_new_cases) / len(daily_new_cases)                     #calculate the mean cases

    highest_record = max(data, key = lambda r: r.get("positiveIncrease", 0))           #max new cases
    highest_date = format_date(highest_record["date"])                                  #day of max
    highest_value = highest_record.get("positiveIncrease", 0)                                 

    most_recent_0 = None                                                        #last day with 0 new cases
    for record in data:
        if record.get("positiveIncrease", 0) == 0:                                #if the increase was 0 pull the date
            most_recent_0 = format_date(record["date"])
            break
    
    monthly_totals = defaultdict(int)                                           #chat helped me with this one. defaultdict prevents dictionaries from crashing if there is not a value    
    for record in data:
        d = str(record["date"])
        y, m = int(d[:4]), int(d[4:6])
        monthly_totals[(y, m)] += record.get("positiveIncrease", 0)            #loop to add every case to the specific month for a monthly totatl

    highest_month, highest_month_total = max(monthly_totals.items(), key=lambda x: x[1])    #highest monthly total
    lowest_month, lowest_month_total = min(monthly_totals.items(), key=lambda x: x[1])          #lowest monthly toal

    print("\nCovid confirmed cases statistics")                                         #print everything out
    print(f"\nState name: {state_code.upper()}")
    print(f"Average number of new daily confirmed cases: {avg_daily:.2f}")
    print(f"Date with highest new number of covid cases: {highest_date} ({highest_value:,} cases)")
    print(f"Most recent date with no new covid cases: {most_recent_0}")
    print(f"Month and Year with highest new number of covid cases: {highest_month[0]}-{highest_month[1]:02d} ({highest_month_total:,} cases)")
    print(f"Month and Year with lowest new number of covid cases: {lowest_month[0]}-{lowest_month[1]:02d} ({lowest_month_total:,} cases)")

def main():
    for code in state_codes:
        data = fetch_data(code)
        if data:
            analyze(code, data)

if __name__ == "__main__":
    main()
