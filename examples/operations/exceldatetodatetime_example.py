#!/usr/bin/env python
"""exceldatetodatetime_example.py
An example of how to use the excel_date_to_datetime function.

This example demonstrates:
1. Basic usage of excel_date_to_datetime
2. Converting different types of Excel date values (int, float, str)
3. Working with different timezones
4. Handling Excel date peculiarities
5. Practical applications for Excel date conversion
"""


# Imports #
# Standard Libraries #
import datetime

# Source Packages #
from baseobjects.operations import excel_date_to_datetime


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of excel_date_to_datetime."""
    print("\nBasic excel_date_to_datetime Usage:")

    # Excel dates are stored as the number of days since December 30, 1899
    # For example, January 1, 1900 is represented as 2

    # Example Excel date value (as an integer)
    # This represents January 1, 2023
    excel_date_int = 44927

    # Convert to datetime
    dt = excel_date_to_datetime(excel_date_int)

    print(f"Excel date (int): {excel_date_int}")
    print(f"Converted datetime: {dt}")
    print("Expected: 2023-01-01 00:00:00+00:00")

    # Verify the timezone
    print(f"Timezone: {dt.tzinfo}")
    print("Expected: UTC")


def different_types_example():
    """Demonstrate converting different types of Excel date values."""
    print("\nDifferent Types Example:")

    # Integer Excel date
    excel_date_int = 44927  # January 1, 2023
    dt_from_int = excel_date_to_datetime(excel_date_int)

    print(f"From integer ({excel_date_int}):")
    print(f"  {dt_from_int}")
    print("  Expected: 2023-01-01 00:00:00+00:00")

    # Float Excel date (with time component)
    # 44927.5 represents January 1, 2023 at 12:00 PM (noon)
    excel_date_float = 44927.5
    dt_from_float = excel_date_to_datetime(excel_date_float)

    print(f"\nFrom float ({excel_date_float}):")
    print(f"  {dt_from_float}")
    print("  Expected: 2023-01-01 12:00:00+00:00")

    # String Excel date (same value)
    excel_date_str = "44927.75"  # January 1, 2023 at 6:00 PM
    dt_from_str = excel_date_to_datetime(excel_date_str)

    print(f"\nFrom string ('{excel_date_str}'):")
    print(f"  {dt_from_str}")
    print("  Expected: 2023-01-01 18:00:00+00:00")

    # Bytes Excel date (same value)
    excel_date_bytes = b"44927.25"  # January 1, 2023 at 6:00 AM
    dt_from_bytes = excel_date_to_datetime(excel_date_bytes)

    print(f"\nFrom bytes ({excel_date_bytes}):")
    print(f"  {dt_from_bytes}")
    print("  Expected: 2023-01-01 06:00:00+00:00")


def timezone_example():
    """Demonstrate working with different timezones."""
    print("\nTimezone Example:")

    # Example Excel date value
    excel_date = 44927.5  # January 1, 2023 at 12:00 PM

    # Convert to datetime with UTC timezone (default)
    dt_utc = excel_date_to_datetime(excel_date)

    print("With UTC timezone:")
    print(f"  {dt_utc}")
    print(f"  Timezone: {dt_utc.tzinfo}")

    # Convert to datetime with local timezone
    local_tz = datetime.datetime.now().astimezone().tzinfo
    dt_local = excel_date_to_datetime(excel_date, tzinfo=local_tz)

    print("\nWith local timezone:")
    print(f"  {dt_local}")
    print(f"  Timezone: {dt_local.tzinfo}")

    # Convert to datetime with no timezone
    dt_none = excel_date_to_datetime(excel_date, tzinfo=None)

    print("\nWith no timezone:")
    print(f"  {dt_none}")
    print(f"  Timezone: {dt_none.tzinfo}")

    # Convert to datetime with Eastern timezone
    eastern = datetime.timezone(datetime.timedelta(hours=-5))  # UTC-5
    dt_eastern = excel_date_to_datetime(excel_date, tzinfo=eastern)

    print("\nWith Eastern timezone (UTC-5):")
    print(f"  {dt_eastern}")
    print(f"  Timezone: {dt_eastern.tzinfo}")


def excel_date_peculiarities_example():
    """Demonstrate handling Excel date peculiarities."""
    print("\nExcel Date Peculiarities Example:")

    # Excel incorrectly treats 1900 as a leap year
    # February 29, 1900 (day 60) doesn't actually exist, but Excel includes it

    # January 31, 1900 (day 32)
    jan_31_1900 = excel_date_to_datetime(32)
    print(f"January 31, 1900: {jan_31_1900}")

    # February 28, 1900 (day 59)
    feb_28_1900 = excel_date_to_datetime(59)
    print(f"February 28, 1900: {feb_28_1900}")

    # February 29, 1900 (day 60) - This date doesn't actually exist!
    feb_29_1900 = excel_date_to_datetime(60)
    print(f"February 29, 1900: {feb_29_1900}")
    print("Note: February 29, 1900 doesn't actually exist (1900 wasn't a leap year)")

    # March 1, 1900 (day 61)
    mar_1_1900 = excel_date_to_datetime(61)
    print(f"March 1, 1900: {mar_1_1900}")

    # Excel's day 1 is January 1, 1900, but the epoch is December 30, 1899
    day_0 = excel_date_to_datetime(0)
    print(f"\nExcel day 0: {day_0}")
    print("Expected: 1899-12-30 00:00:00+00:00")

    day_1 = excel_date_to_datetime(1)
    print(f"Excel day 1: {day_1}")
    print("Expected: 1899-12-31 00:00:00+00:00")

    day_2 = excel_date_to_datetime(2)
    print(f"Excel day 2: {day_2}")
    print("Expected: 1900-01-01 00:00:00+00:00")


def date_calculation_example():
    """Demonstrate date calculations with Excel dates."""
    print("\nDate Calculation Example:")

    # Convert some dates to Excel format and back

    # Today's date
    today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    # Convert to Excel date
    # Excel dates are days since December 30, 1899
    # Python datetime epoch is January 1, 1970
    # The difference is 25569 days
    excel_epoch = datetime.datetime(1899, 12, 30, tzinfo=datetime.timezone.utc)
    excel_date = (today - excel_epoch).days

    print(f"Today's date: {today}")
    print(f"Converted to Excel date: {excel_date}")

    # Convert back to datetime
    dt = excel_date_to_datetime(excel_date)

    print(f"Converted back to datetime: {dt}")

    # Calculate the difference
    diff = (today - dt).total_seconds()

    print(f"Difference: {abs(diff)} seconds")
    print("Expected: 0 seconds")

    # Add time component (12:30 PM)
    excel_date_with_time = excel_date + 0.5208333333  # 0.5 days + 0.0208333333 (30 minutes)
    dt_with_time = excel_date_to_datetime(excel_date_with_time)

    print(f"\nExcel date with time (12:30 PM): {excel_date_with_time}")
    print(f"Converted to datetime: {dt_with_time}")
    print("Expected: Today at 12:30 PM UTC")


def practical_example():
    """Demonstrate a practical use case for excel_date_to_datetime."""
    print("\nPractical Example - Processing Excel Data:")

    # Simulate data exported from Excel
    excel_data = [
        {"ID": 1001, "Name": "Alice", "DOB": 36526, "StartDate": 44562, "Hours": 37.5},
        {"ID": 1002, "Name": "Bob", "DOB": 33237, "StartDate": 44927, "Hours": 40.0},
        {"ID": 1003, "Name": "Charlie", "DOB": 29915, "StartDate": 43831, "Hours": 20.0},
    ]

    print("Raw Excel data:")
    for row in excel_data:
        print(f"  {row}")

    # Process the data to convert Excel dates to Python datetimes
    processed_data = []
    for row in excel_data:
        processed_row = row.copy()
        processed_row["DOB"] = excel_date_to_datetime(row["DOB"])
        processed_row["StartDate"] = excel_date_to_datetime(row["StartDate"])
        processed_data.append(processed_row)

    print("\nProcessed data with converted dates:")
    for row in processed_data:
        print(f"  {row}")

    # Calculate age and tenure for each person
    today = datetime.datetime.now(datetime.timezone.utc)

    print("\nCalculated information:")
    for row in processed_data:
        name = row["Name"]
        dob = row["DOB"]
        start_date = row["StartDate"]

        # Calculate age
        age_days = (today - dob).days
        age_years = age_days / 365.25

        # Calculate tenure
        tenure_days = (today - start_date).days
        tenure_years = tenure_days / 365.25

        print(f"  {name}:")
        print(f"    Date of Birth: {dob.strftime('%Y-%m-%d')}")
        print(f"    Age: {age_years:.1f} years")
        print(f"    Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"    Tenure: {tenure_years:.1f} years")

        # Format dates for display in a report
        print(f"    Formatted DOB: {dob.strftime('%B %d, %Y')}")
        print(f"    Formatted Start Date: {start_date.strftime('%B %d, %Y')}")


def error_handling_example():
    """Demonstrate error handling with excel_date_to_datetime."""
    print("\nError Handling Example:")

    # Try with an invalid type
    print("Trying with an invalid type (list):")
    try:
        dt = excel_date_to_datetime([1, 2, 3])
        print(f"Result: {dt}")
    except TypeError as e:
        print(f"TypeError: {e}")
        print("Expected: TypeError indicating lists cannot be converted to a datetime")

    # Try with a negative value (before Excel epoch)
    print("\nTrying with a negative value:")
    try:
        dt = excel_date_to_datetime(-10)
        print(f"Result: {dt}")
        print("Expected: A date 10 days before December 30, 1899")
    except Exception as e:
        print(f"Exception: {e}")
        print("Note: Negative values may or may not be handled depending on implementation")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    different_types_example()
    timezone_example()
    excel_date_peculiarities_example()
    date_calculation_example()
    practical_example()
    error_handling_example()
