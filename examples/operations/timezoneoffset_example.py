#!/usr/bin/env python
"""timezoneoffset_example.py
An example of how to use the timezone_offset function.

This example demonstrates:
1. Basic usage of timezone_offset
2. Getting offsets from different timezone types
3. Working with timezone-aware datetime objects
4. Practical applications of timezone offsets
"""

# Imports #
# Standard Libraries #
import datetime
import zoneinfo

# Source Packages #
from baseobjects.operations import timezone_offset


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of timezone_offset."""
    print("\nBasic timezone_offset Usage:")

    # Get the UTC timezone
    utc = datetime.timezone.utc

    # Get the offset of UTC
    utc_offset = timezone_offset(utc)

    print(f"UTC timezone: {utc}")
    print(f"UTC offset: {utc_offset}")
    print("Expected: 0:00:00 (zero offset)")

    # Get a fixed timezone with a positive offset
    eastern = datetime.timezone(datetime.timedelta(hours=-5))  # UTC-5 (Eastern Standard Time)

    # Get the offset
    eastern_offset = timezone_offset(eastern)

    print(f"\nEastern timezone: {eastern}")
    print(f"Eastern offset: {eastern_offset}")
    print("Expected: -5:00:00 (5 hours behind UTC)")

    # Get a fixed timezone with a negative offset
    central_europe = datetime.timezone(datetime.timedelta(hours=1))  # UTC+1 (Central European Time)

    # Get the offset
    cet_offset = timezone_offset(central_europe)

    print(f"\nCentral European timezone: {central_europe}")
    print(f"Central European offset: {cet_offset}")
    print("Expected: 1:00:00 (1 hour ahead of UTC)")


def different_timezone_types_example() -> None:
    """Demonstrate timezone_offset with different timezone types."""
    print("\nDifferent Timezone Types Example:")

    # Using datetime.timezone (fixed offset)
    fixed_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))  # UTC+5:30 (India)
    fixed_offset = timezone_offset(fixed_tz)

    print(f"Fixed timezone (UTC+5:30): {fixed_tz}")
    print(f"Offset: {fixed_offset}")
    print("Expected: 5:30:00")

    # Using zoneinfo.ZoneInfo (IANA timezone database)
    try:
        # This requires Python 3.9+ and the tzdata package on Windows
        new_york_tz = zoneinfo.ZoneInfo("America/New_York")
        ny_offset = timezone_offset(new_york_tz)

        # Note: The offset may vary depending on Daylight Saving Time
        print(f"\nNew York timezone: {new_york_tz}")
        print(f"Offset: {ny_offset}")
        print("Note: This offset may be -5:00:00 (EST) or -4:00:00 (EDT) depending on the date")

        # Get the current time in New York to check if it's DST
        now = datetime.datetime.now(new_york_tz)
        is_dst = now.dst() != datetime.timedelta(0)
        print(f"Current time in New York: {now}")
        print(f"Is Daylight Saving Time: {is_dst}")
    except (ImportError, zoneinfo.ZoneInfoNotFoundError):
        print("\nZoneInfo example skipped: requires Python 3.9+ and tzdata package on Windows")


def timezone_aware_datetime_example() -> None:
    """Demonstrate working with timezone-aware datetime objects."""
    print("\nTimezone-Aware Datetime Example:")

    # Create timezone objects
    utc = datetime.timezone.utc
    eastern = datetime.timezone(datetime.timedelta(hours=-5))  # UTC-5

    # Create timezone-aware datetime objects
    utc_now = datetime.datetime.now(utc)
    eastern_now = datetime.datetime.now(eastern)

    # Get the offsets
    utc_offset = timezone_offset(utc)
    eastern_offset = timezone_offset(eastern)

    print(f"Current UTC time: {utc_now}")
    print(f"UTC offset: {utc_offset}")

    print(f"\nCurrent Eastern time: {eastern_now}")
    print(f"Eastern offset: {eastern_offset}")

    # Calculate the time difference
    time_diff = utc_now - eastern_now
    print(f"\nTime difference between UTC and Eastern: {time_diff}")
    print(f"Expected difference: {abs(eastern_offset)} (ignoring microseconds)")

    # Convert from one timezone to another
    eastern_to_utc = eastern_now.astimezone(utc)
    print(f"\nEastern time converted to UTC: {eastern_to_utc}")
    print(f"Original Eastern time: {eastern_now}")
    print(f"Time values should be equal: {eastern_to_utc.hour == (eastern_now.hour + 5) % 24}")


def practical_example() -> None:
    """Demonstrate a practical use case for timezone_offset."""
    print("\nPractical Example - Meeting Scheduler:")

    # Define timezones for participants
    try:
        # Using zoneinfo for named timezones (Python 3.9+)
        new_york_tz = zoneinfo.ZoneInfo("America/New_York")
        london_tz = zoneinfo.ZoneInfo("Europe/London")
        tokyo_tz = zoneinfo.ZoneInfo("Asia/Tokyo")
        sydney_tz = zoneinfo.ZoneInfo("Australia/Sydney")

        # Get the offsets
        ny_offset = timezone_offset(new_york_tz)
        london_offset = timezone_offset(london_tz)
        tokyo_offset = timezone_offset(tokyo_tz)
        sydney_offset = timezone_offset(sydney_tz)

        # Print the offsets
        print("Timezone offsets for meeting participants:")
        print(f"  New York: {ny_offset}")
        print(f"  London: {london_offset}")
        print(f"  Tokyo: {tokyo_offset}")
        print(f"  Sydney: {sydney_offset}")

        # Schedule a meeting in UTC
        meeting_time_utc = datetime.datetime(2023, 6, 15, 14, 0, tzinfo=datetime.timezone.utc)  # 2 PM UTC

        # Convert to local times for participants
        meeting_time_ny = meeting_time_utc.astimezone(new_york_tz)
        meeting_time_london = meeting_time_utc.astimezone(london_tz)
        meeting_time_tokyo = meeting_time_utc.astimezone(tokyo_tz)
        meeting_time_sydney = meeting_time_utc.astimezone(sydney_tz)

        print("\nMeeting scheduled for:")
        print(f"  UTC: {meeting_time_utc.strftime('%Y-%m-%d %H:%M')}")
        print(f"  New York: {meeting_time_ny.strftime('%Y-%m-%d %H:%M')}")
        print(f"  London: {meeting_time_london.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Tokyo: {meeting_time_tokyo.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Sydney: {meeting_time_sydney.strftime('%Y-%m-%d %H:%M')}")

        # Check if the meeting is during working hours (9 AM to 5 PM) for each participant
        def is_working_hours(dt):
            return 9 <= dt.hour < 17

        print("\nIs the meeting during working hours (9 AM - 5 PM)?")
        print(f"  New York: {is_working_hours(meeting_time_ny)}")
        print(f"  London: {is_working_hours(meeting_time_london)}")
        print(f"  Tokyo: {is_working_hours(meeting_time_tokyo)}")
        print(f"  Sydney: {is_working_hours(meeting_time_sydney)}")

        # Find a better meeting time if needed
        if not all(
            is_working_hours(t) for t in [meeting_time_ny, meeting_time_london, meeting_time_tokyo, meeting_time_sydney]
        ):
            print("\nNot all participants can attend during their working hours.")
            print("Searching for a better meeting time...")

            # Try different UTC hours to find a time that works for everyone
            for hour in range(24):
                proposed_time_utc = datetime.datetime(2023, 6, 15, hour, 0, tzinfo=datetime.timezone.utc)
                proposed_time_ny = proposed_time_utc.astimezone(new_york_tz)
                proposed_time_london = proposed_time_utc.astimezone(london_tz)
                proposed_time_tokyo = proposed_time_utc.astimezone(tokyo_tz)
                proposed_time_sydney = proposed_time_utc.astimezone(sydney_tz)

                if all(
                    is_working_hours(t)
                    for t in [proposed_time_ny, proposed_time_london, proposed_time_tokyo, proposed_time_sydney]
                ):
                    print("\nFound a suitable time for all participants:")
                    print(f"  UTC: {proposed_time_utc.strftime('%Y-%m-%d %H:%M')}")
                    print(f"  New York: {proposed_time_ny.strftime('%Y-%m-%d %H:%M')}")
                    print(f"  London: {proposed_time_london.strftime('%Y-%m-%d %H:%M')}")
                    print(f"  Tokyo: {proposed_time_tokyo.strftime('%Y-%m-%d %H:%M')}")
                    print(f"  Sydney: {proposed_time_sydney.strftime('%Y-%m-%d %H:%M')}")
                    break
            else:
                print("\nNo time works for all participants during their working hours.")
                print("Some participants will need to join outside their normal working hours.")
    except (ImportError, zoneinfo.ZoneInfoNotFoundError):
        # Fallback for older Python versions or missing tzdata
        print("This example requires Python 3.9+ and the tzdata package on Windows.")
        print("Using fixed offsets instead:")

        # Define timezones with fixed offsets
        new_york_tz = datetime.timezone(datetime.timedelta(hours=-5))  # EST
        london_tz = datetime.timezone(datetime.timedelta(hours=0))  # GMT
        tokyo_tz = datetime.timezone(datetime.timedelta(hours=9))  # JST
        sydney_tz = datetime.timezone(datetime.timedelta(hours=10))  # AEST

        # Get the offsets
        ny_offset = timezone_offset(new_york_tz)
        london_offset = timezone_offset(london_tz)
        tokyo_offset = timezone_offset(tokyo_tz)
        sydney_offset = timezone_offset(sydney_tz)

        print("Timezone offsets for meeting participants (fixed):")
        print(f"  New York: {ny_offset}")
        print(f"  London: {london_offset}")
        print(f"  Tokyo: {tokyo_offset}")
        print(f"  Sydney: {sydney_offset}")

        print("\nNote: Fixed offsets don't account for Daylight Saving Time.")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    different_timezone_types_example()
    timezone_aware_datetime_example()
    practical_example()
