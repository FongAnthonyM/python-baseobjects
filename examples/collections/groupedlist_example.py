#!/usr/bin/env python
"""groupedlist_example.py
An example of how to use GroupedList class.

This example demonstrates:
1. Creating and using a GroupedList
2. Working with named groups
3. Nested groups and hierarchical data
4. Accessing and manipulating items across groups
5. Practical use cases for GroupedList
"""
# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.collections import GroupedList


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of GroupedList."""
    print("\nBasic GroupedList Usage:")

    # Create a GroupedList with initial items
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    grouped_list = GroupedList(items)

    print(f"Initial list: {grouped_list}")
    print(f"Length: {len(grouped_list)} == 5")

    # Access items by index
    print("\nAccessing items:")
    print(f"First item: {grouped_list[0]} == 'apple'")
    print(f"Last item: {grouped_list[-1]} == 'elderberry'")

    # Modify items
    print("\nModifying items:")
    grouped_list[1] = "blueberry"
    print(f"After modification: {grouped_list}")
    print(f"New second item: {grouped_list[1]} == 'blueberry'")

    # Add items
    print("\nAdding items:")
    grouped_list.append("fig")
    print(f"After append: {grouped_list}")

    # Insert items
    grouped_list.insert(2, "grape")
    print(f"After insert: {grouped_list}")

    # Remove items
    print("\nRemoving items:")
    grouped_list.remove("date")
    print(f"After remove: {grouped_list}")

    popped = grouped_list.pop()
    print(f"Popped item: {popped} == 'fig'")
    print(f"After pop: {grouped_list}")

    # Check membership
    print("\nChecking membership:")
    print(f"'apple' in list: {'apple' in grouped_list} == True")
    print(f"'date' in list: {'date' in grouped_list} == False")

    # Get flat representation
    print("\nFlat representation:")
    flat_list = grouped_list.as_flat_list()
    print(f"As flat list: {flat_list}")

    flat_tuple = grouped_list.as_flat_tuple()
    print(f"As flat tuple: {flat_tuple}")


def group_operations_example() -> None:
    """Demonstrate operations with named groups."""
    print("\nGroup Operations Example:")

    # Create an empty GroupedList
    grouped_list = GroupedList()

    # Create named groups
    print("Creating named groups:")
    fruits = grouped_list.create_group("fruits")
    vegetables = grouped_list.create_group("vegetables")

    # Add items to groups
    fruits.append("apple")
    fruits.append("banana")
    fruits.append("cherry")

    vegetables.append("carrot")
    vegetables.append("broccoli")
    vegetables.append("spinach")

    # Access groups by name
    print("\nAccessing groups by name:")
    print(f"Fruits group: {grouped_list['fruits']}")
    print(f"Vegetables group: {grouped_list['vegetables']}")

    # Add items directly to a group using the group name
    print("\nAdding items to a group using the group name:")
    grouped_list.append("date", group="fruits")
    grouped_list.append("eggplant", group="vegetables")

    print(f"Updated fruits group: {grouped_list['fruits']}")
    print(f"Updated vegetables group: {grouped_list['vegetables']}")

    # Access items across all groups
    print("\nAccessing all items (flattened view):")
    print(f"All items: {grouped_list}")
    print(f"Total number of items: {len(grouped_list)} == 8")

    # Access individual items by index (flattened view)
    print("\nAccessing items by index (flattened view):")
    print(f"First item: {grouped_list[0]} == 'apple'")
    print(f"Fifth item: {grouped_list[4]} == 'carrot'")

    # Remove a group
    print("\nRemoving a group:")
    grouped_list.remove_group("vegetables")
    print(f"After removing vegetables group: {grouped_list}")
    print(f"Total number of items: {len(grouped_list)} == 4")

    # Check if a group exists and create if it doesn't
    print("\nRequiring a group (creates if it doesn't exist):")
    dairy = grouped_list.require_group("dairy")
    dairy.append("milk")
    dairy.append("cheese")

    print(f"Dairy group: {grouped_list['dairy']}")
    print(f"All items after adding dairy: {grouped_list}")
    print(f"Total number of items: {len(grouped_list)} == 6")


def nested_groups_example() -> None:
    """Demonstrate nested groups and hierarchical data."""
    print("\nNested Groups Example:")

    # Create a GroupedList for a file system structure
    file_system = GroupedList()

    # Create top-level directories
    documents = file_system.create_group("documents")
    pictures = file_system.create_group("pictures")

    # Create subdirectories in documents
    work = documents.create_group("work")
    personal = documents.create_group("personal")

    # Add files to directories
    work.append("report.docx")
    work.append("presentation.pptx")
    work.append("budget.xlsx")

    personal.append("resume.pdf")
    personal.append("notes.txt")

    pictures.append("vacation.jpg")
    pictures.append("family.png")
    pictures.append("pet.jpg")

    # Access nested groups
    print("File system structure:")
    print(f"Documents: {file_system['documents']}")
    print(f"Pictures: {file_system['pictures']}")
    print(f"Work documents: {file_system['documents']['work']}")
    print(f"Personal documents: {file_system['documents']['personal']}")

    # Access using require_group with a path
    print("\nAccessing nested groups with require_group:")
    work_dir = file_system.require_group(["documents", "work"])
    print(f"Work directory: {work_dir}")

    # Add a new file to a nested directory
    print("\nAdding a file to a nested directory:")
    file_system.append("contract.pdf", group=["documents", "work"])
    print(f"Updated work directory: {file_system['documents']['work']}")

    # Count total files
    print("\nCounting total files:")
    print(f"Total number of files: {len(file_system)} == 9")

    # Flatten the structure
    print("\nFlattened file system:")
    flat_files = file_system.as_flat_list()
    print(f"All files: {flat_files}")

    # Access files by index in the flattened view
    print("\nAccessing files by index (flattened view):")
    print(f"First file: {file_system[0]} == 'report.docx'")
    print(f"Fifth file: {file_system[4]} == 'vacation.jpg'")


def comparison_operations_example() -> None:
    """Demonstrate comparison operations with GroupedList."""
    print("\nComparison Operations Example:")

    # Create two GroupedLists
    list1 = GroupedList(["a", "b", "c"])
    fruits = list1.create_group("fruits")
    fruits.append("apple")
    fruits.append("banana")

    list2 = GroupedList(["a", "b", "c"])
    fruits2 = list2.create_group("fruits")
    fruits2.append("apple")
    fruits2.append("banana")

    list3 = GroupedList(["a", "b", "d"])
    fruits3 = list3.create_group("fruits")
    fruits3.append("apple")
    fruits3.append("cherry")

    # Compare GroupedLists
    print("Comparing GroupedLists:")
    print(f"list1 == list2: {list1 == list2} == True")
    print(f"list1 == list3: {list1 == list3} == False")
    print(f"list1 < list3: {list1 < list3} == True")
    print(f"list3 > list1: {list3 > list1} == True")

    # Compare with regular lists
    regular_list = ["a", "b", "c", "apple", "banana"]
    print("\nComparing with regular lists:")
    print(f"list1 == regular_list: {list1 == regular_list} == True")

    # Arithmetic operations
    print("\nArithmetic operations:")
    list4 = [*list1, "d", "e"]
    print(f"list1 + ['d', 'e']: {list4}")

    list5 = list1 * 2
    print(f"list1 * 2: {list5}")


def practical_example() -> None:
    """Demonstrate a practical use case for GroupedList."""
    print("\nPractical Example - Task Management System:")

    # Create a task management system using GroupedList
    tasks = GroupedList()

    # Create task categories
    work = tasks.create_group("work")
    personal = tasks.create_group("personal")

    # Create priority levels within work tasks
    high_priority = work.create_group("high_priority")
    medium_priority = work.create_group("medium_priority")
    low_priority = work.create_group("low_priority")

    # Add tasks
    high_priority.append("Complete project proposal")
    high_priority.append("Prepare for client meeting")

    medium_priority.append("Review team's code")
    medium_priority.append("Update documentation")

    low_priority.append("Organize email inbox")

    personal.append("Buy groceries")
    personal.append("Schedule dentist appointment")
    personal.append("Plan weekend trip")

    # Display all tasks
    print("All tasks:")
    for i, task in enumerate(tasks):
        print(f"  {i + 1}. {task}")

    # Display tasks by category
    print("\nWork tasks:")
    for task in tasks["work"]:
        print(f"  - {task}")

    print("\nPersonal tasks:")
    for task in tasks["personal"]:
        print(f"  - {task}")

    # Display tasks by priority
    print("\nHigh priority work tasks:")
    for task in tasks["work"]["high_priority"]:
        print(f"  - {task}")

    # Add a new task to a specific category and priority
    print("\nAdding a new high priority work task:")
    tasks.append("Respond to urgent email", group=["work", "high_priority"])

    print("Updated high priority work tasks:")
    for task in tasks["work"]["high_priority"]:
        print(f"  - {task}")

    # Mark a task as completed (remove it)
    print("\nMarking 'Buy groceries' as completed:")
    tasks.remove("Buy groceries")

    print("Updated personal tasks:")
    for task in tasks["personal"]:
        print(f"  - {task}")

    # Count tasks by category
    print("\nTask counts:")
    print(f"Total tasks: {len(tasks)} == 8")
    print(f"Work tasks: {len(tasks['work'])} == 6")
    print(f"Personal tasks: {len(tasks['personal'])} == 2")
    print(f"High priority work tasks: {len(tasks['work']['high_priority'])} == 3")


def error_handling_example() -> None:
    """Demonstrate error handling with GroupedList."""
    print("\nError Handling Example:")

    # Create a GroupedList
    grouped_list = GroupedList(["a", "b", "c"])
    fruits = grouped_list.create_group("fruits")
    fruits.append("apple")

    # Try to access a non-existent index
    print("Trying to access a non-existent index:")
    try:
        item = grouped_list[10]
        print(f"Item: {item}")
    except IndexError as e:
        print(f"  IndexError: {e}")

    # Try to access a non-existent group
    print("\nTrying to access a non-existent group:")
    try:
        group = grouped_list["vegetables"]
        print(f"Group: {group}")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Try to create a group with an existing name
    print("\nTrying to create a group with an existing name:")
    try:
        grouped_list.create_group("fruits")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Try to add a GroupedList to itself
    print("\nTrying to add a GroupedList to itself:")
    try:
        grouped_list.add_group(grouped_list, "self")
    except ValueError as e:
        print(f"  ValueError: {e}")

    # Proper error handling with require_group
    print("\nUsing require_group to safely get or create a group:")
    vegetables = grouped_list.require_group("vegetables")
    vegetables.append("carrot")
    print(f"Vegetables group: {grouped_list['vegetables']} == ['carrot']")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    group_operations_example()
    nested_groups_example()
    comparison_operations_example()
    practical_example()
    error_handling_example()
