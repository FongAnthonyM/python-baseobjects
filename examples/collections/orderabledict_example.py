#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""orderabledict_example.py
An example of how to use OrderableDict class.

This example demonstrates:
1. Creating and using an OrderableDict
2. Manipulating the order of items
3. Accessing items by index
4. Practical use cases for OrderableDict
"""
# Imports #
# Standard Libraries #
from typing import Any, Dict

# Third-Party Packages #
from baseobjects.collections import OrderableDict

# Local Packages #


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of OrderableDict."""
    print("\nBasic OrderableDict Usage:")

    # Create an OrderableDict with initial items
    user_info = OrderableDict({"name": "John Doe", "email": "john.doe@example.com", "age": 30})

    print("Initial dictionary:")
    for key, value in user_info.items():
        print(f"  {key}: {value}")

    # Access items by key (like a regular dictionary)
    print("\nAccessing items by key:")
    print(f"Name: {user_info['name']} == 'John Doe'")
    print(f"Email: {user_info['email']} == 'john.doe@example.com'")
    print(f"Age: {user_info['age']} == 30")

    # Add new items (they are appended to the order)
    print("\nAdding new items:")
    user_info["phone"] = "555-1234"
    user_info["address"] = "123 Main St"

    print("Dictionary after adding items:")
    for key, value in user_info.items():
        print(f"  {key}: {value}")

    # Update existing items (order is preserved)
    print("\nUpdating existing items:")
    user_info["age"] = 31

    print("Dictionary after updating items:")
    for key, value in user_info.items():
        print(f"  {key}: {value}")

    # Remove items
    print("\nRemoving items:")
    del user_info["email"]

    print("Dictionary after removing 'email':")
    for key, value in user_info.items():
        print(f"  {key}: {value}")

    # Check the order
    print("\nOrder of keys:")
    print(f"  {list(user_info.keys())} == ['name', 'age', 'phone', 'address']")


def order_manipulation_example():
    """Demonstrate manipulating the order of items in OrderableDict."""
    print("\nOrder Manipulation Example:")

    # Create an OrderableDict
    menu = OrderableDict()

    # Add items in a specific order
    menu["appetizers"] = ["Salad", "Soup", "Bruschetta"]
    menu["main_courses"] = ["Steak", "Pasta", "Fish"]
    menu["desserts"] = ["Cake", "Ice Cream", "Fruit"]
    menu["drinks"] = ["Water", "Soda", "Wine"]

    print("Initial menu order:")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")

    # Reverse the order
    print("\nReversing the order:")
    menu.reverse()

    print("Menu after reversing:")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")

    # Insert a new item at a specific position
    print("\nInserting 'specials' at position 1:")
    menu.insert(1, "specials", ["Chef's Special", "Catch of the Day"])

    print("Menu after insertion:")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")

    # Move an existing item to a new position
    print("\nMoving 'desserts' to position 1:")
    menu.insert_move(1, "desserts", menu["desserts"])

    print("Menu after moving 'desserts':")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")

    # Pop the last item
    print("\nPopping the last item:")
    last_key, last_value = menu.popitem()
    print(f"Popped item: {last_key}: {last_value}")

    print("Menu after popping:")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")

    # Pop an item by index
    print("\nPopping item at index 1:")
    popped_value = menu.pop_index(1)
    print(f"Popped value: {popped_value}")

    print("Menu after popping index 1:")
    for i, (section, items) in enumerate(menu.items()):
        print(f"  {i+1}. {section}: {items}")


def index_access_example():
    """Demonstrate accessing items by index in OrderableDict."""
    print("\nIndex Access Example:")

    # Create an OrderableDict
    colors = OrderableDict()
    colors["red"] = "#FF0000"
    colors["green"] = "#00FF00"
    colors["blue"] = "#0000FF"
    colors["yellow"] = "#FFFF00"
    colors["purple"] = "#800080"

    print("Colors dictionary:")
    for key, value in colors.items():
        print(f"  {key}: {value}")

    # Access items by index
    print("\nAccessing items by index:")
    print(f"First color (index 0): {colors.get_index(0)} == '#FF0000'")
    print(f"Third color (index 2): {colors.get_index(2)} == '#0000FF'")
    print(f"Last color (index -1): {colors.get_index(-1)} == '#800080'")

    # Access with default value for out-of-range index
    print("\nAccessing out-of-range index with default:")
    print(f"Index 10 (with default 'Not found'): {colors.get_index(10, 'Not found')} == 'Not found'")

    # Set value by index
    print("\nSetting value by index:")
    colors.set_index(1, "#00CC00")  # Change green to a different shade

    print("Colors after setting index 1:")
    for key, value in colors.items():
        print(f"  {key}: {value}")

    # Get the key at a specific index
    print("\nGetting key at index:")
    third_key = colors.order[2]
    print(f"Key at index 2: {third_key} == 'blue'")


def compare_with_dict_example():
    """Compare OrderableDict with regular dict and collection.OrderedDict."""
    print("\nComparing OrderableDict with other dictionary types:")

    # Create dictionaries with the same initial content
    regular_dict = {"a": 1, "b": 2, "c": 3}
    orderable_dict = OrderableDict({"a": 1, "b": 2, "c": 3})

    print("Initial dictionaries:")
    print(f"  Regular dict: {regular_dict}")
    print(f"  OrderableDict: {orderable_dict}")

    # Add items in a different order
    print("\nAdding items in a different order:")

    # For regular dict (Python 3.7+), insertion order is preserved but can't be manipulated
    regular_dict["e"] = 5
    regular_dict["d"] = 4

    # For OrderableDict, we can control the order
    orderable_dict["e"] = 5
    orderable_dict["d"] = 4

    print("After adding items:")
    print(f"  Regular dict keys: {list(regular_dict.keys())} == ['a', 'b', 'c', 'e', 'd']")
    print(f"  OrderableDict keys: {list(orderable_dict.keys())} == ['a', 'b', 'c', 'e', 'd']")

    # Now manipulate the order in OrderableDict
    print("\nManipulating order in OrderableDict:")
    orderable_dict.insert(0, "z", 26)  # Insert at beginning
    orderable_dict.insert_move(1, "d", 4)  # Move 'd' to position 1

    print("After manipulating order:")
    print(f"  OrderableDict keys: {list(orderable_dict.keys())} == ['z', 'd', 'a', 'b', 'c', 'e']")

    # This kind of manipulation isn't possible with regular dict
    print("\nWith regular dict, you can't manipulate the order directly.")


def practical_example():
    """Demonstrate a practical use case for OrderableDict."""
    print("\nPractical Example - Form Field Ordering:")

    # Create a form with fields in a specific order
    form_fields = OrderableDict()

    # Add fields in the desired order
    form_fields["first_name"] = {"label": "First Name", "type": "text", "required": True}

    form_fields["last_name"] = {"label": "Last Name", "type": "text", "required": True}

    form_fields["email"] = {"label": "Email Address", "type": "email", "required": True}

    form_fields["phone"] = {"label": "Phone Number", "type": "tel", "required": False}

    form_fields["address"] = {"label": "Address", "type": "textarea", "required": False}

    form_fields["submit"] = {"label": "Submit", "type": "button", "required": False}

    # Render the form in the specified order
    print("Rendering form in original order:")
    for field_name, field_props in form_fields.items():
        print(f"  {field_props['label']} ({field_name}): {field_props['type']} field")

    # User testing shows that address should come before phone
    print("\nReordering fields based on user testing:")

    # Move address before phone
    address_props = form_fields.pop("address")
    phone_index = list(form_fields.keys()).index("phone")
    form_fields.insert(phone_index, "address", address_props)

    # Render the form in the new order
    print("Rendering form in new order:")
    for field_name, field_props in form_fields.items():
        print(f"  {field_props['label']} ({field_name}): {field_props['type']} field")

    # Add a new field in a specific position
    print("\nAdding a new field in a specific position:")
    form_fields.insert(2, "middle_name", {"label": "Middle Name", "type": "text", "required": False})

    # Render the form with the new field
    print("Rendering form with new field:")
    for field_name, field_props in form_fields.items():
        print(f"  {field_props['label']} ({field_name}): {field_props['type']} field")


def error_handling_example():
    """Demonstrate error handling with OrderableDict."""
    print("\nError Handling Example:")

    # Create an OrderableDict
    data = OrderableDict({"a": 1, "b": 2, "c": 3})

    # Try to access a non-existent key
    print("Trying to access a non-existent key:")
    try:
        value = data["d"]
        print(f"Value: {value}")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Try to access a non-existent index
    print("\nTrying to access a non-existent index:")
    try:
        value = data.get_index(10)
        print(f"Value: {value}")
    except IndexError as e:
        print(f"  IndexError: {e}")

    # Using get_index with a default value
    print("\nUsing get_index with a default value:")
    value = data.get_index(10, default="Not found")
    print(f"  Value: {value} == 'Not found'")

    # Try to insert a key that already exists
    print("\nTrying to insert a key that already exists:")
    try:
        data.insert(0, "a", 100)
        print("  Inserted successfully")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Using insert_move instead
    print("\nUsing insert_move for existing key:")
    data.insert_move(0, "a", 100)
    print(f"  New order: {list(data.keys())} == ['a', 'b', 'c']")
    print(f"  New value for 'a': {data['a']} == 100")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    order_manipulation_example()
    index_access_example()
    compare_with_dict_example()
    practical_example()
    error_handling_example()
