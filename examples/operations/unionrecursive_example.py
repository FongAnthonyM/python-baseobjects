#!/usr/bin/env python
"""unionrecursive_example.py
An example of how to use the union_recursive function.

This example demonstrates:
1. Basic usage of union_recursive
2. Unioning nested dictionaries
3. Comparing union_recursive with update_recursive
4. Preserving original dictionaries
5. Practical use cases for union_recursive
"""


# Imports #
# Standard Libraries #
from copy import deepcopy

# Source Packages #
from baseobjects.operations import union_recursive, update_recursive


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of union_recursive."""
    print("\nBasic union_recursive Usage:")

    # Create a simple dictionary
    dict1 = {"a": 1, "b": 2, "c": 3}

    # Create another dictionary
    dict2 = {"b": 22, "d": 4}

    # Create a union of the two dictionaries
    result = union_recursive(dict1, dict2)

    print(f"Dictionary 1: {dict1}")
    print(f"Dictionary 2: {dict2}")
    print(f"Union result: {result}")
    print("Expected: {'a': 1, 'b': 22, 'c': 3, 'd': 4}")

    # Verify that the original dictionaries are unchanged
    print(f"Dictionary 1 unchanged: {dict1 == {'a': 1, 'b': 2, 'c': 3}} == True")
    print(f"Dictionary 2 unchanged: {dict2 == {'b': 22, 'd': 4}} == True")

    # Verify that result is a new object
    print(f"Result is new object: {result is not dict1 and result is not dict2} == True")


def nested_dictionary_example():
    """Demonstrate unioning nested dictionaries with union_recursive."""
    print("\nNested Dictionary Example:")

    # Create a nested dictionary
    dict1 = {
        "user": {"name": "John", "age": 30, "address": {"city": "New York", "zip": "10001"}},
        "settings": {"theme": "dark", "notifications": True},
    }

    # Create another nested dictionary
    dict2 = {
        "user": {"age": 31, "address": {"state": "NY"}},  # Different value  # New nested value
        "settings": {"language": "en"},  # New value
    }

    # Create a union of the two dictionaries
    result = union_recursive(dict1, dict2)

    print("Dictionary 1:")
    print(f"  {dict1}")

    print("\nDictionary 2:")
    print(f"  {dict2}")

    print("\nUnion result:")
    print(f"  {result}")

    # Expected result
    expected = {
        "user": {
            "name": "John",
            "age": 31,  # Updated from dict2
            "address": {"city": "New York", "zip": "10001", "state": "NY"},  # Added from dict2
        },
        "settings": {"theme": "dark", "notifications": True, "language": "en"},  # Added from dict2
    }

    print("\nExpected:")
    print(f"  {expected}")

    # Verify that nested structures are preserved in the result
    print("\nVerifying nested structures in result:")
    print(f"  User name: {result['user']['name']} == 'John'")
    print(f"  User age: {result['user']['age']} == 31")
    print(f"  User city: {result['user']['address']['city']} == 'New York'")
    print(f"  User state: {result['user']['address']['state']} == 'NY'")
    print(f"  Settings language: {result['settings']['language']} == 'en'")

    # Verify that original dictionaries are unchanged
    print("\nVerifying original dictionaries are unchanged:")
    print(f"  Dict1 user age: {dict1['user']['age']} == 30")
    print(f"  'state' in Dict1 user address: {'state' in dict1['user']['address']} == False")
    print(f"  'language' in Dict1 settings: {'language' in dict1['settings']} == False")


def compare_with_update_recursive_example():
    """Compare union_recursive with update_recursive."""
    print("\nComparing union_recursive with update_recursive:")

    # Create a nested dictionary
    original = {"a": 1, "b": {"x": 10, "y": 20}}

    # Create an update dictionary
    updates = {"b": {"y": 25, "z": 30}, "c": 3}

    # Make a copy for update_recursive
    original_copy = deepcopy(original)

    # Use update_recursive (modifies in-place)
    update_result = update_recursive(original_copy, updates)

    # Use union_recursive (creates a new dictionary)
    union_result = union_recursive(original, updates)

    print("Original dictionary:")
    print(f"  {original}")

    print("\nUpdates:")
    print(f"  {updates}")

    print("\nupdate_recursive result:")
    print(f"  {update_result}")
    print(f"  Original modified: {original_copy is update_result} == True")

    print("\nunion_recursive result:")
    print(f"  {union_result}")
    print(f"  Original unchanged: {original != union_result} == True")
    print(f"  New object created: {union_result is not original and union_result is not updates} == True")

    # Verify the results are equivalent
    print("\nVerifying results are equivalent:")
    print(f"  Results equal: {update_result == union_result} == True")


def deep_copy_example():
    """Demonstrate how union_recursive creates deep copies."""
    print("\nDeep Copy Example:")

    # Create a dictionary with a nested list
    dict1 = {"name": "John", "scores": [85, 90, 95]}

    # Create another dictionary
    dict2 = {"age": 30}

    # Create a union
    result = union_recursive(dict1, dict2)

    print(f"Dictionary 1: {dict1}")
    print(f"Dictionary 2: {dict2}")
    print(f"Union result: {result}")

    # Modify the original list
    dict1["scores"].append(100)

    print("\nAfter modifying the original list:")
    print(f"Dictionary 1: {dict1}")
    print(f"Union result: {result}")
    print("Note: The list in the union result is not affected by changes to the original")

    # Verify that the lists are different objects
    print(f"\nLists are different objects: {id(dict1['scores']) != id(result['scores'])} == True")


def practical_example():
    """Demonstrate a practical use case for union_recursive."""
    print("\nPractical Example - Template System:")

    # Base template
    base_template = {
        "header": {"title": "Default Title", "logo": "default_logo.png", "menu": ["Home", "About", "Contact"]},
        "content": {"main": "Default content", "sidebar": "Default sidebar"},
        "footer": {"copyright_": "© 2023 Company", "links": ["Privacy", "Terms"]},
    }

    # Page-specific customizations
    about_page = {
        "header": {"title": "About Us"},
        "content": {"main": "About page content", "sidebar": "About page sidebar", "extra_section": "Our history"},
    }

    # Create the final page by unioning the base template with the customizations
    about_page_final = union_recursive(base_template, about_page)

    print("Base template:")
    print(f"  {base_template}")

    print("\nPage customizations:")
    print(f"  {about_page}")

    print("\nFinal page (union of base and customizations):")
    print(f"  {about_page_final}")

    # Verify specific elements
    print("\nVerifying specific elements:")
    print(f"  Title: {about_page_final['header']['title']} == 'About Us'")
    print(f"  Logo: {about_page_final['header']['logo']} == 'default_logo.png'")
    print(f"  Menu: {about_page_final['header']['menu']} == ['Home', 'About', 'Contact']")
    print(f"  Main content: {about_page_final['content']['main']} == 'About page content'")
    print(f"  Extra section: {about_page_final['content']['extra_section']} == 'Our history'")
    print(f"  Footer copyright_: {about_page_final['footer']['copyright_']} == '© 2023 Company'")

    # Create another page
    contact_page = {
        "header": {"title": "Contact Us"},
        "content": {"main": "Contact page content", "form": {"fields": ["Name", "Email", "Message"], "submit": "Send"}},
    }

    # Create the final contact page
    contact_page_final = union_recursive(base_template, contact_page)

    print("\nAnother page customization:")
    print(f"  {contact_page}")

    print("\nAnother final page:")
    print(f"  {contact_page_final}")

    # Verify the base template is unchanged
    print("\nVerifying base template is unchanged:")
    print(f"  Base title: {base_template['header']['title']} == 'Default Title'")
    print(f"  'form' in base content: {'form' in base_template['content']} == False")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    nested_dictionary_example()
    compare_with_update_recursive_example()
    deep_copy_example()
    practical_example()
