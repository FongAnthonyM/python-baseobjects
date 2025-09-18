#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""filetimetodatetime_example.py
An example of how to use the filetime_to_datetime function.

This example demonstrates:
1. Basic usage of filetime_to_datetime
2. Converting different types of filetime values (int, float, str, bytes)
3. Working with different timezones
4. Practical applications for Windows filetime conversion
"""
# Imports #
# Standard Libraries #
import datetime
import struct

# Third-Party Packages #
from baseobjects.operations import filetime_to_datetime

# Local Packages #


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of filetime_to_datetime."""
    print("\nBasic filetime_to_datetime Usage:")
    
    # Windows filetime is a 64-bit value representing the number of 100-nanosecond
    # intervals since January 1, 1601 (UTC)
    
    # Example filetime value (as an integer)
    # This represents 2023-06-15 12:00:00 UTC
    filetime_int = 133322452000000000
    
    # Convert to datetime
    dt = filetime_to_datetime(filetime_int)
    
    print(f"Filetime (int): {filetime_int}")
    print(f"Converted datetime: {dt}")
    print(f"Expected: A datetime around 2023-06-15 12:00:00+00:00")
    
    # Verify the timezone
    print(f"Timezone: {dt.tzinfo}")
    print(f"Expected: UTC")


def different_types_example():
    """Demonstrate converting different types of filetime values."""
    print("\nDifferent Types Example:")
    
    # Integer filetime
    filetime_int = 133322452000000000  # 2023-06-15 12:00:00 UTC
    dt_from_int = filetime_to_datetime(filetime_int)
    
    print(f"From integer ({filetime_int}):")
    print(f"  {dt_from_int}")
    
    # Float filetime (same value)
    filetime_float = float(filetime_int)
    dt_from_float = filetime_to_datetime(filetime_float)
    
    print(f"\nFrom float ({filetime_float}):")
    print(f"  {dt_from_float}")
    
    # String filetime (same value)
    filetime_str = str(filetime_int)
    dt_from_str = filetime_to_datetime(filetime_str)
    
    print(f"\nFrom string ('{filetime_str}'):")
    print(f"  {dt_from_str}")
    
    # Bytes filetime (same value)
    # Windows stores filetime as a little-endian 64-bit value
    filetime_bytes = struct.pack("<Q", filetime_int)
    dt_from_bytes = filetime_to_datetime(filetime_bytes)
    
    print(f"\nFrom bytes ({filetime_bytes.hex()}):")
    print(f"  {dt_from_bytes}")
    
    # Verify all conversions produce the same result
    print("\nVerifying all conversions produce the same result:")
    print(f"  All equal: {dt_from_int == dt_from_float == dt_from_str == dt_from_bytes}")


def timezone_example():
    """Demonstrate working with different timezones."""
    print("\nTimezone Example:")
    
    # Example filetime value
    filetime = 133322452000000000  # 2023-06-15 12:00:00 UTC
    
    # Convert to datetime with UTC timezone (default)
    dt_utc = filetime_to_datetime(filetime)
    
    print(f"With UTC timezone:")
    print(f"  {dt_utc}")
    print(f"  Timezone: {dt_utc.tzinfo}")
    
    # Convert to datetime with local timezone
    local_tz = datetime.datetime.now().astimezone().tzinfo
    dt_local = filetime_to_datetime(filetime, tzinfo=local_tz)
    
    print(f"\nWith local timezone:")
    print(f"  {dt_local}")
    print(f"  Timezone: {dt_local.tzinfo}")
    
    # Convert to datetime with no timezone
    dt_none = filetime_to_datetime(filetime, tzinfo=None)
    
    print(f"\nWith no timezone:")
    print(f"  {dt_none}")
    print(f"  Timezone: {dt_none.tzinfo}")
    
    # Convert to datetime with Eastern timezone
    eastern = datetime.timezone(datetime.timedelta(hours=-5))  # UTC-5
    dt_eastern = filetime_to_datetime(filetime, tzinfo=eastern)
    
    print(f"\nWith Eastern timezone (UTC-5):")
    print(f"  {dt_eastern}")
    print(f"  Timezone: {dt_eastern.tzinfo}")
    
    # Verify the time values are adjusted correctly
    print("\nVerifying time values are adjusted correctly:")
    print(f"  UTC hour: {dt_utc.hour}")
    print(f"  Eastern hour: {dt_eastern.hour}")
    print(f"  Difference: {(dt_utc.hour - dt_eastern.hour) % 24} hours")
    print(f"  Expected difference: 5 hours")


def current_filetime_example():
    """Demonstrate converting current time to filetime and back."""
    print("\nCurrent Filetime Example:")
    
    # Get current UTC time
    now_utc = datetime.datetime.now()
    print(f"Current UTC time: {now_utc}")
    
    # Convert to Windows filetime
    # Windows filetime is 100-nanosecond intervals since January 1, 1601 (UTC)
    # Python datetime epoch is January 1, 1970
    # The difference is 11,644,473,600 seconds
    epoch_diff = 11644473600
    filetime = int((now_utc.timestamp() + epoch_diff) * 10000000)
    
    print(f"Converted to filetime: {filetime}")
    
    # Convert back to datetime
    dt = filetime_to_datetime(filetime)
    
    print(f"Converted back to datetime: {dt}")
    
    # Calculate the difference
    diff = (now_utc - dt).total_seconds()
    
    print(f"Difference: {abs(diff)} seconds")
    print(f"Expected: Close to 0 seconds (allowing for processing time)")


def practical_example():
    """Demonstrate a practical use case for filetime_to_datetime."""
    print("\nPractical Example - Windows File Metadata:")
    
    # In a real application, these values would come from Windows API calls
    # For this example, we'll use sample values
    
    # Sample file creation time (filetime)
    file_creation_time = 133322452000000000  # 2023-06-15 12:00:00 UTC
    
    # Sample file modification time (filetime)
    file_modification_time = 133322488000000000  # 2023-06-15 13:00:00 UTC
    
    # Sample file access time (filetime)
    file_access_time = 133322524000000000  # 2023-06-15 14:00:00 UTC
    
    # Convert to datetime objects
    creation_dt = filetime_to_datetime(file_creation_time, datetime.timezone.utc)
    modification_dt = filetime_to_datetime(file_modification_time, datetime.timezone.utc)
    access_dt = filetime_to_datetime(file_access_time, datetime.timezone.utc)
    
    print("File: example.txt")
    print(f"Created: {creation_dt}")
    print(f"Modified: {modification_dt}")
    print(f"Accessed: {access_dt}")
    
    # Calculate time differences
    mod_diff = (modification_dt - creation_dt).total_seconds() / 60  # minutes
    access_diff = (access_dt - modification_dt).total_seconds() / 60  # minutes
    
    print(f"\nTime since creation to modification: {mod_diff} minutes")
    print(f"Time since modification to last access: {access_diff} minutes")
    
    # Check if file was modified recently (within the last day)
    now = datetime.datetime.now(datetime.timezone.utc)
    modified_recently = (now - modification_dt).total_seconds() < 86400  # 24 hours in seconds
    
    print(f"\nFile was modified recently: {modified_recently}")
    
    # Format dates for display
    print("\nFormatted dates for display:")
    date_format = "%Y-%m-%d %H:%M:%S %Z"
    print(f"Created: {creation_dt.strftime(date_format)}")
    print(f"Modified: {modification_dt.strftime(date_format)}")
    print(f"Accessed: {access_dt.strftime(date_format)}")


def error_handling_example():
    """Demonstrate error handling with filetime_to_datetime."""
    print("\nError Handling Example:")
    
    # Try with an invalid type
    print("Trying with an invalid type (list):")
    try:
        dt = filetime_to_datetime([1, 2, 3])
        print(f"Result: {dt}")
    except TypeError as e:
        print(f"TypeError: {e}")
        print("Expected: TypeError indicating lists cannot be converted to datetime")
    
    # Try with a negative value (before Windows epoch)
    print("\nTrying with a negative value:")
    try:
        dt = filetime_to_datetime(-1000)
        print(f"Result: {dt}")
    except Exception as e:
        print(f"Exception: {e}")
        print("Note: Negative values may or may not be handled depending on implementation")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    different_types_example()
    timezone_example()
    current_filetime_example()
    practical_example()
    error_handling_example()