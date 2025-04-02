import requests
from datetime import datetime, timedelta
import sys
import time
from random import uniform


def get_available_dates(start_date, end_date):
    """
    Checks for available camping dates within the specified date range.

    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format

    Returns:
        list: List of available dates with their remaining quota
    """
    # Base URL with the parameters provided
    base_url = "https://camping.bcparks.ca/api/availability/resourcedailyavailability"

    # Parameters for the request
    params = {
        "resourceId": "-2147483209",
        "bookingCategoryId": "4",
        "startDate": start_date,
        "endDate": end_date,
        "isReserving": "true",
        "partySize": "2",
        "numEquipment": "1",
        "filterData": "[]",
        "bookingUid": "3513977b-d699-469e-9559-591a2e0ecd3e"
    }

    try:
        # Add headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://camping.bcparks.ca/",
            "Origin": "https://camping.bcparks.ca",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "DNT": "1"
        }

        # Add a small delay to mimic human behavior
        time.sleep(uniform(1, 2))

        # Make the request with headers
        response = requests.get(base_url, params=params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully connected to the BC Parks API!")
            data = response.json()

            # Generate a list of dates from start_date to end_date
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            available_dates = []
            current_date = start

            # Loop through each item in the response and check if it's available
            for index, item in enumerate(data):
                # Only process if the current date is within our date range
                if current_date <= end:
                    # Check if the availability is 0 (available)
                    if item.get("availability") == 0:
                        available_dates.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "day_of_week": current_date.strftime("%A"),
                            "formatted_date": current_date.strftime("%a, %b %d"),
                            "remaining_quota": item.get("remainingQuota")
                        })

                    # Move to the next date
                    current_date += timedelta(days=1)

            return available_dates
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text[:200]}...")  # Print first 200 chars of response
            print("\nTry opening the URL in a browser first to accept any cookies/terms before running this script.")
            return []

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def print_available_dates(available_dates):
    """
    Prints the available dates in a nice format.

    Args:
        available_dates (list): List of available dates with their remaining quota
    """
    if not available_dates:
        print("No available dates found.")
        return

    print("\n" + "=" * 50)
    print("AVAILABLE CAMPING DATES")
    print("=" * 50)

    for date_info in available_dates:
        remaining = date_info["remaining_quota"]
        quota_display = f"Remaining Quota: {remaining}" if remaining is not None else "Remaining Quota: unlimited"

        print(f"{date_info['formatted_date']} - {quota_display}")

    print("\n" + "=" * 50)
    print(f"Total Available Dates: {len(available_dates)}")
    print("=" * 50)


def main():
    # Default date range from the prompt
    start_date = "2025-06-25"
    end_date = "2025-09-10"

    print(f"Running script with properly configured browser headers to bypass protections...")

    # Allow command line arguments to override defaults
    if len(sys.argv) > 1:
        start_date = sys.argv[1]
    if len(sys.argv) > 2:
        end_date = sys.argv[2]

    print(f"Checking availability from {start_date} to {end_date}...")

    # Get available dates
    available_dates = get_available_dates(start_date, end_date)

    # Print the results
    print_available_dates(available_dates)


if __name__ == "__main__":
    main()