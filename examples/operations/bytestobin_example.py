#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bytestobin_example.py
An example of how to use the bytes_to_bin function.

This example demonstrates:
1. Converting bytes to binary values
2. Using different byte orders (big and little endian)
3. Outputting binary values in different types (int, bool, str)
4. Handling edge cases
"""


# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects.operations import bytes_to_bin

# Local Packages #


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of bytes_to_bin."""
    print("\nBasic bytes_to_bin Usage:")
    
    # Create some sample bytes
    sample_bytes = b'\x0F\xA0'  # 00001111 10100000 in binary
    
    # Convert to binary using default settings (big endian, int output)
    binary_values = bytes_to_bin(sample_bytes)
    
    print(f"Sample bytes: {sample_bytes.hex()} (hex)")
    print("Binary representation (big endian, int output):")
    print(f"  {binary_values}")
    print(f"  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")
    
    # Print in a more readable format
    first_byte = binary_values[:8]
    second_byte = binary_values[8:]
    
    print(f"First byte (0x0F): {first_byte}")
    print(f"Second byte (0xA0): {second_byte}")


def byte_order_example():
    """Demonstrate using different byte orders with bytes_to_bin."""
    print("\nByte Order Example:")
    
    # Create a sample byte
    sample_byte = b'\x0F'  # 00001111 in binary
    
    # Convert using big endian (default)
    big_endian = bytes_to_bin(sample_byte, byteorder="big")
    
    # Convert using little endian
    little_endian = bytes_to_bin(sample_byte, byteorder="little")
    
    print(f"Sample byte: {sample_byte.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print(f"  Expected: (0, 0, 0, 0, 1, 1, 1, 1)")
    print(f"Little endian: {little_endian}")
    print(f"  Expected: (0, 0, 0, 0, 1, 1, 1, 1)")  # For this specific byte, the result is the same
    
    # Example where the results differ
    sample_byte = b'\x81'  # 10000001 in binary
    
    # Convert using big endian (default)
    big_endian = bytes_to_bin(sample_byte, byteorder="big")
    
    # Convert using little endian
    little_endian = bytes_to_bin(sample_byte, byteorder="little")
    
    print(f"\nSample byte: {sample_byte.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print(f"  Expected: (1, 0, 0, 0, 0, 0, 0, 1)")
    print(f"Little endian: {little_endian}")
    print(f"  Expected: (1, 0, 0, 0, 0, 0, 0, 1)")  # For this specific byte, the result is the same
    
    # Example with multiple bytes where the results differ
    sample_bytes = b'\x0F\xA0'  # 00001111 10100000 in binary
    
    # Convert using big endian (default)
    big_endian = bytes_to_bin(sample_bytes, byteorder="big")
    
    # Convert using little endian
    little_endian = bytes_to_bin(sample_bytes, byteorder="little")
    
    print(f"\nSample bytes: {sample_bytes.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print(f"  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")
    print(f"Little endian: {little_endian}")
    print(f"  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")


def output_type_example():
    """Demonstrate different output types with bytes_to_bin."""
    print("\nOutput Type Example:")
    
    # Create a sample byte
    sample_byte = b'\xA5'  # 10100101 in binary
    
    # Convert to int (default)
    int_output = bytes_to_bin(sample_byte, out_type=int)
    
    # Convert to bool
    bool_output = bytes_to_bin(sample_byte, out_type=bool)
    
    # Convert to str
    str_output = bytes_to_bin(sample_byte, out_type=str)
    
    print(f"Sample byte: {sample_byte.hex()} (hex)")
    print(f"Int output: {int_output}")
    print(f"  Expected: (1, 0, 1, 0, 0, 1, 0, 1)")
    print(f"Bool output: {bool_output}")
    print(f"  Expected: (True, False, True, False, False, True, False, True)")
    print(f"Str output: {str_output}")
    print(f"  Expected: ('True', 'False', 'True', 'False', 'False', 'True', 'False', 'True')")


def s_example():
    """Demonstrate edge cases with bytes_to_bin."""
    print("\nEdge Cases Example:")
    
    # Empty bytes
    empty_bytes = b''
    empty_result = bytes_to_bin(empty_bytes)
    
    print(f"Empty bytes: {empty_bytes}")
    print(f"Result: {empty_result}")
    print(f"  Expected: ()")
    
    # Single zero byte
    zero_byte = b'\x00'
    zero_result = bytes_to_bin(zero_byte)
    
    print(f"\nZero byte: {zero_byte.hex()} (hex)")
    print(f"Result: {zero_result}")
    print(f"  Expected: (0, 0, 0, 0, 0, 0, 0, 0)")
    
    # Single 0xFF byte (all bits set)
    ff_byte = b'\xFF'
    ff_result = bytes_to_bin(ff_byte)
    
    print(f"\nFF byte: {ff_byte.hex()} (hex)")
    print(f"Result: {ff_result}")
    print(f"  Expected: (1, 1, 1, 1, 1, 1, 1, 1)")
    
    # Invalid byte order
    print("\nInvalid byte order:")
    try:
        invalid_result = bytes_to_bin(b'\x00', byteorder="invalid")
        print(f"Result: {invalid_result}")
    except ValueError as e:
        print(f"ValueError: {e}")
        print("  Expected: ValueError: byteorder must be either 'little' or 'big'")


def practical_example():
    """Demonstrate a practical use case for bytes_to_bin."""
    print("\nPractical Example - Parsing a Flag Byte:")
    
    # Define a flag byte where each bit represents a different setting
    # Bit 0 (LSB): Read permission
    # Bit 1: Write permission
    # Bit 2: Execute permission
    # Bit 3: Is directory
    # Bit 4: Is hidden
    # Bit 5: Is system
    # Bit 6: Is archive
    # Bit 7 (MSB): Is readonly
    
    flag_byte = b'\x93'  # 10010011 in binary
    
    # Convert to binary
    flags = bytes_to_bin(flag_byte, out_type=bool)
    
    # Parse the flags
    is_readonly = flags[0]
    is_archive = flags[1]
    is_system = flags[2]
    is_hidden = flags[3]
    is_directory = flags[4]
    has_execute = flags[5]
    has_write = flags[6]
    has_read = flags[7]
    
    print(f"Flag byte: {flag_byte.hex()} (hex)")
    print(f"Binary representation: {flags}")
    print("\nParsed flags:")
    print(f"  Read permission: {has_read}")
    print(f"  Write permission: {has_write}")
    print(f"  Execute permission: {has_execute}")
    print(f"  Is directory: {is_directory}")
    print(f"  Is hidden: {is_hidden}")
    print(f"  Is system: {is_system}")
    print(f"  Is archive: {is_archive}")
    print(f"  Is readonly: {is_readonly}")
    
    # Use the flags to make decisions
    print("\nFile permissions:")
    if has_read:
        print("  - File can be read")
    if has_write:
        print("  - File can be written")
    if has_execute:
        print("  - File can be executed")
    
    print("\nFile attributes:")
    if is_directory:
        print("  - This is a directory")
    else:
        print("  - This is a file")
    
    if is_readonly:
        print("  - File is read-only")
    
    if is_hidden:
        print("  - File is hidden")
    
    if is_system:
        print("  - File is a system file")
    
    if is_archive:
        print("  - File is archived")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    byte_order_example()
    output_type_example()
    edge_cases_example()
    practical_example()