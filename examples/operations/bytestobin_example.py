#!/usr/bin/env python
"""bytestobin_example.py
An example of how to use the bytes_to_bin function.

This example demonstrates:
1. Converting bytes to binary values
2. Using different byte orders (big and little endian)
3. Outputting binary values in different types (int, bool, str)
4. Handling edge cases
"""


# Imports #
# Source Packages #
from baseobjects.operations import bytes_to_bin

# Example Sections #


def basic_usage_example() -> None:
    """Demonstrates basic usage of bytes_to_bin."""
    print("\nBasic bytes_to_bin Usage:")

    # Creates some sample bytes
    sample_bytes = b"\x0f\xa0"  # 00001111 10100000 in binary

    # Converts to binary using default settings (big endian, int output)
    binary_values = bytes_to_bin(sample_bytes)

    print(f"Sample bytes: {sample_bytes.hex()} (hex)")
    print("Binary representation (big endian, int output):")
    print(f"  {binary_values}")
    print("  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")

    # Prints in a more readable format
    first_byte = binary_values[:8]
    second_byte = binary_values[8:]

    print(f"First byte (0x0F): {first_byte}")
    print(f"Second byte (0xA0): {second_byte}")


def byte_order_example() -> None:
    """Demonstrates using different byte orders with bytes_to_bin."""
    print("\nByte Order Example:")

    # Creates a sample byte
    sample_byte = b"\x0f"  # 00001111 in binary

    # Converts using big endian (default)
    big_endian = bytes_to_bin(sample_byte, byteorder="big")

    # Converts using little endian
    little_endian = bytes_to_bin(sample_byte, byteorder="little")

    print(f"Sample byte: {sample_byte.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print("  Expected: (0, 0, 0, 0, 1, 1, 1, 1)")
    print(f"Little endian: {little_endian}")
    print("  Expected: (0, 0, 0, 0, 1, 1, 1, 1)")  # For this specific byte, the result is the same

    # Example where the results differ
    sample_byte = b"\x81"  # 10000001 in binary

    # Converts using big endian (default)
    big_endian = bytes_to_bin(sample_byte, byteorder="big")

    # Converts using little endian
    little_endian = bytes_to_bin(sample_byte, byteorder="little")

    print(f"\nSample byte: {sample_byte.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print("  Expected: (1, 0, 0, 0, 0, 0, 0, 1)")
    print(f"Little endian: {little_endian}")
    print("  Expected: (1, 0, 0, 0, 0, 0, 0, 1)")  # For this specific byte, the result is the same

    # Example with multiple bytes where the results differ
    sample_bytes = b"\x0f\xa0"  # 00001111 10100000 in binary

    # Converts using big endian (default)
    big_endian = bytes_to_bin(sample_bytes, byteorder="big")

    # Converts using little endian
    little_endian = bytes_to_bin(sample_bytes, byteorder="little")

    print(f"\nSample bytes: {sample_bytes.hex()} (hex)")
    print(f"Big endian: {big_endian}")
    print("  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")
    print(f"Little endian: {little_endian}")
    print("  Expected: (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0)")


def output_type_example() -> None:
    """Demonstrates different output types with bytes_to_bin."""
    print("\nOutput Type Example:")

    # Creates a sample byte
    sample_byte = b"\xa5"  # 10100101 in binary

    # Converts to int (default)
    int_output = bytes_to_bin(sample_byte, out_type=int)

    # Converts to bool
    bool_output = bytes_to_bin(sample_byte, out_type=bool)

    # Converts to str
    str_output = bytes_to_bin(sample_byte, out_type=str)

    print(f"Sample byte: {sample_byte.hex()} (hex)")
    print(f"Int output: {int_output}")
    print("  Expected: (1, 0, 1, 0, 0, 1, 0, 1)")
    print(f"Bool output: {bool_output}")
    print("  Expected: (True, False, True, False, False, True, False, True)")
    print(f"Str output: {str_output}")
    print("  Expected: ('True', 'False', 'True', 'False', 'False', 'True', 'False', 'True')")


def edge_cases_example() -> None:
    """Demonstrates edge cases with bytes_to_bin."""
    print("\nEdge Cases Example:")

    # Empty bytes
    empty_bytes = b""
    empty_result = bytes_to_bin(empty_bytes)

    print(f"Empty bytes: {empty_bytes!r}")
    print(f"Result: {empty_result}")
    print("  Expected: ()")

    # Single zero byte
    zero_byte = b"\x00"
    zero_result = bytes_to_bin(zero_byte)

    print(f"\nZero byte: {zero_byte.hex()} (hex)")
    print(f"Result: {zero_result}")
    print("  Expected: (0, 0, 0, 0, 0, 0, 0, 0)")

    # Single 0xFF byte (all bits set)
    ff_byte = b"\xff"
    ff_result = bytes_to_bin(ff_byte)

    print(f"\nFF byte: {ff_byte.hex()} (hex)")
    print(f"Result: {ff_result}")
    print("  Expected: (1, 1, 1, 1, 1, 1, 1, 1)")

    # Invalid byte order
    print("\nInvalid byte order:")
    try:
        invalid_result = bytes_to_bin(b"\x00", byteorder="invalid")
        print(f"Result: {invalid_result}")
    except ValueError as e:
        print(f"ValueError: {e}")
        print("  Expected: ValueError: byteorder must be either 'little' or 'big'")


def practical_example() -> None:
    """Demonstrates a practical use case for bytes_to_bin."""
    print("\nPractical Example - Parsing a Flag Byte:")

    # Defines a flag byte where each bit represents a different setting
    # Bit 0 (LSB): Read permission
    # Bit 1: Write permission
    # Bit 2: Execute permission
    # Bit 3: Is directory
    # Bit 4: Is hidden
    # Bit 5: Is system
    # Bit 6: Is archive
    # Bit 7 (MSB): Is readonly

    flag_byte = b"\x93"  # 10010011 in binary

    # Converts to binary
    flags = bytes_to_bin(flag_byte, out_type=bool)

    # Parse the flags
    is_readonly = bool(flags[0])
    is_archive = bool(flags[1])
    is_system = bool(flags[2])
    is_hidden = bool(flags[3])
    is_directory = bool(flags[4])
    has_execute = bool(flags[5])
    has_write = bool(flags[6])
    has_read = bool(flags[7])

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
    # Runs examples
    basic_usage_example()
    byte_order_example()
    output_type_example()
    edge_cases_example()
    practical_example()
