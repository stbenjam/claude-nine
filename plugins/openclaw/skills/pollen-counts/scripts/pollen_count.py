#!/usr/bin/python3

import sys
import requests
import argparse
from datetime import datetime

def get_pollen_info(zip_code):
    """
    Fetches pollen information for a given US ZIP code using the Pollen.com API.
    """
    # The Pollen.com API requires a Referer header to work properly
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.pollen.com'
    }
    
    url = f"https://www.pollen.com/api/forecast/current/pollen/{zip_code}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if we got valid data (periods will be empty for invalid ZIPs)
        if not data.get('Location') or not data['Location'].get('periods'):
            print(f"Error: No data found for ZIP code {zip_code}. Please ensure it is a valid US ZIP code.")
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_level_description(index):
    """
    Returns a textual description and emoji indicator of the pollen index level.
    Scale used by Pollen.com: 0-12
    """
    if index <= 2.4:
        return "Low", "🟢"
    elif index <= 4.8:
        return "Low-Medium", "🟡"
    elif index <= 7.2:
        return "Medium", "🟡"
    elif index <= 9.6:
        return "Medium-High", "🟠"
    else:
        return "High", "🔴"

def report_pollen(data):
    """
    Prints a formatted report of the pollen information.
    """
    loc = data['Location']
    city = loc.get('City', 'Unknown')
    state = loc.get('State', '??')
    zip_code = loc.get('ZIP', '?????')

    forecast_date = data.get('ForecastDate', '')
    try:
        dt = datetime.fromisoformat(forecast_date.replace('Z', '+00:00'))
        date_str = dt.strftime('%a, %b %d, %Y')
    except (ValueError, AttributeError):
        date_str = forecast_date.split('T')[0] if forecast_date else 'N/A'

    print(f"\n🌼 POLLEN REPORT 🌼")
    print(f"{city}, {state} ({zip_code}) | {date_str}")
    print()

    periods = loc.get('periods', [])
    all_triggers = []

    for period in periods:
        p_type = period.get('Type')
        index = period.get('Index')
        triggers = period.get('Triggers', [])

        if p_type not in ["Yesterday", "Today", "Tomorrow"]:
            continue

        desc, emoji = get_level_description(index)
        print(f"📅 {p_type}: {index} {emoji} {desc}")

        for t in triggers:
            name = t.get('Name')
            if name and name not in all_triggers:
                all_triggers.append(name)

    if all_triggers:
        print(f"\n🌿 Top Allergens:\n")
        for name in all_triggers:
            print(f"  • {name}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Fetch pollen levels for a given US ZIP code.")
    parser.add_argument("zip_code", help="The 5-digit US ZIP code to check.")
    
    args = parser.parse_args()
    
    if not args.zip_code.isdigit() or len(args.zip_code) != 5:
        print("Error: Please provide a valid 5-digit US ZIP code.")
        sys.exit(1)
        
    pollen_data = get_pollen_info(args.zip_code)
    
    if pollen_data:
        report_pollen(pollen_data)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
