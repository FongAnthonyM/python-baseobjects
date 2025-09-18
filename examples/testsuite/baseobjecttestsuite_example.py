#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""baseobjecttestsuite_example.py
An example of how to use BaseObjectTestSuite to test custom objects.

This example demonstrates:
1. Creating a concrete implementation of BaseObject
2. Creating a test suite for the custom object
3. Implementing the required abstract test methods
4. Running tests on the custom object
5. Extending the test suite with additional tests
"""


# Imports #
# Standard Libraries #
import copy
import pickle
from typing import Any, Dict, List, Optional

# Third-Party Packages #
import pytest
from baseobjects.bases import BaseObject
from baseobjects.testsuite.bases import BaseObjectTestSuite

# Local Packages #


# Definitions #
# Classes #
class Person(BaseObject):
    """A simple person class that inherits from BaseObject.
    
    This class demonstrates a basic implementation of BaseObject for testing.
    """
    
    def __init__(self, name: str, age: int, email: Optional[str] = None) -> None:
        """Initialize a person with a name, age, and optional email.
        
        Args:
            name: The person's name.
            age: The person's age.
            email: The person's email address (optional).
        """
        self.name = name
        self.age = age
        self.email = email
        self.friends = []  # Mutable attribute for testing deep copy
        self.id = id(self)  # Immutable attribute for testing deep copy
    
    def add_friend(self, friend: 'Person') -> None:
        """Add a friend to this person's friend list.
        
        Args:
            friend: The person to add as a friend.
        """
        self.friends.append(friend)
    
    def get_info(self) -> str:
        """Get a string representation of the person's information.
        
        Returns:
            A string with the person's information.
        """
        info = f"{self.name}, {self.age} years old"
        if self.email:
            info += f", Email: {self.email}"
        return info
    
    def has_friend(self, name: str) -> bool:
        """Check if this person has a friend with the given name.
        
        Args:
            name: The name to check for.
            
        Returns:
            True if a friend with the given name exists, False otherwise.
        """
        return any(friend.name == name for friend in self.friends)


class Employee(Person):
    """An employee class that extends Person.
    
    This class demonstrates inheritance from a BaseObject subclass.
    """
    
    def __init__(self, name: str, age: int, email: Optional[str], 
                 employee_id: str, department: str, salary: float) -> None:
        """Initialize an employee with personal and employment information.
        
        Args:
            name: The employee's name.
            age: The employee's age.
            email: The employee's email address.
            employee_id: The employee's ID.
            department: The employee's department.
            salary: The employee's salary.
        """
        super().__init__(name, age, email)
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
    
    def get_info(self) -> str:
        """Get a string representation of the employee's information.
        
        Returns:
            A string with the employee's information.
        """
        return f"{super().get_info()}, ID: {self.employee_id}, Department: {self.department}"


class PersonTestSuite(BaseObjectTestSuite):
    """Test suite for the Person class and its subclasses."""
    
    # Class Attributes #
    TestClass = Person
    
    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> Person:
        """Create a test person object.
        
        Returns:
            A Person instance for testing.
        """
        return Person("Test Person", 30, "test@example.com")
    
    @pytest.fixture
    def test_employee(self) -> Employee:
        """Create a test employee object.
        
        Returns:
            An Employee instance for testing.
        """
        return Employee("Test Employee", 35, "employee@example.com", "E12345", "Engineering", 75000.0)
    
    @pytest.fixture
    def friend_object(self) -> Person:
        """Create a friend object for testing relationships.
        
        Returns:
            A Person instance to use as a friend.
        """
        return Person("Test Friend", 28, "friend@example.com")
    
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test creating an instance of the Person class.
        
        Args:
            *args: Positional arguments for the constructor.
            **kwargs: Keyword arguments for the constructor.
        """
        # Create default arguments if none provided
        if not args and not kwargs:
            args = ("Test Person", 30, "test@example.com")
        
        # Create instance
        instance = self.TestClass(*args, **kwargs)
        
        # Verify instance
        assert isinstance(instance, self.TestClass)
        assert instance.name == args[0]
        assert instance.age == args[1]
        if len(args) > 2:
            assert instance.email == args[2]
    
    def test_copy(self, test_object: Person) -> None:
        """Test the copy behavior of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
        """
        # Add a friend to test mutable attribute copying
        friend = Person("Friend", 25)
        test_object.add_friend(friend)
        
        # Copy object
        obj_copy = copy.copy(test_object)
        
        # Verify copy
        assert obj_copy is not test_object
        assert obj_copy.name == test_object.name
        assert obj_copy.age == test_object.age
        assert obj_copy.email == test_object.email
        assert obj_copy.friends is test_object.friends  # Shallow copy, same object
        assert id(obj_copy) != id(test_object)  # Different objects
        assert obj_copy.id == test_object.id  # Same id value (copied)
    
    def test_copy_method(self, test_object: Person) -> None:
        """Test the copy method of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
        """
        # Add a friend to test mutable attribute copying
        friend = Person("Friend", 25)
        test_object.add_friend(friend)
        
        # Copy object using method
        obj_copy = test_object.copy()
        
        # Verify copy
        assert obj_copy is not test_object
        assert obj_copy.name == test_object.name
        assert obj_copy.age == test_object.age
        assert obj_copy.email == test_object.email
        assert obj_copy.friends is test_object.friends  # Shallow copy, same object
        assert id(obj_copy) != id(test_object)  # Different objects
        assert obj_copy.id == test_object.id  # Same id value (copied)
    
    def test_deepcopy(self, test_object: Person, memo: dict = None) -> None:
        """Test the deep copy behavior of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
            memo: A memo dictionary for deepcopy.
        """
        # Add a friend to test mutable attribute copying
        friend = Person("Friend", 25)
        test_object.add_friend(friend)
        
        # Deep copy object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        
        # Verify deep copy
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.name == test_object.name
        assert obj_deepcopy.age == test_object.age
        assert obj_deepcopy.email == test_object.email
        assert obj_deepcopy.friends is not test_object.friends  # Deep copy, different object
        assert len(obj_deepcopy.friends) == len(test_object.friends)  # Same number of friends
        assert obj_deepcopy.friends[0] is not test_object.friends[0]  # Deep copy of friend objects
        assert obj_deepcopy.friends[0].name == test_object.friends[0].name  # Same friend data
        assert id(obj_deepcopy) != id(test_object)  # Different objects
        assert obj_deepcopy.id == test_object.id  # Same id value (copied)
    
    def test_deepcopy_method(self, test_object: Person, memo: dict = None) -> None:
        """Test the deepcopy method of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
            memo: A memo dictionary for deepcopy.
        """
        # Add a friend to test mutable attribute copying
        friend = Person("Friend", 25)
        test_object.add_friend(friend)
        
        # Deep copy object using method
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)
        
        # Verify deep copy
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.name == test_object.name
        assert obj_deepcopy.age == test_object.age
        assert obj_deepcopy.email == test_object.email
        assert obj_deepcopy.friends is not test_object.friends  # Deep copy, different object
        assert len(obj_deepcopy.friends) == len(test_object.friends)  # Same number of friends
        assert obj_deepcopy.friends[0] is not test_object.friends[0]  # Deep copy of friend objects
        assert obj_deepcopy.friends[0].name == test_object.friends[0].name  # Same friend data
        assert id(obj_deepcopy) != id(test_object)  # Different objects
        assert obj_deepcopy.id == test_object.id  # Same id value (copied)
    
    def test_pickling(self, test_object: Person) -> None:
        """Test pickling and unpickling of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
        """
        # Add a friend to test mutable attribute pickling
        friend = Person("Friend", 25)
        test_object.add_friend(friend)
        
        # Pickle and unpickle object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)
        
        # Verify unpickled object
        assert unpickled is not test_object
        assert unpickled.name == test_object.name
        assert unpickled.age == test_object.age
        assert unpickled.email == test_object.email
        assert unpickled.friends is not test_object.friends  # Different object
        assert len(unpickled.friends) == len(test_object.friends)  # Same number of friends
        assert unpickled.friends[0] is not test_object.friends[0]  # Different friend objects
        assert unpickled.friends[0].name == test_object.friends[0].name  # Same friend data
        assert id(unpickled) != id(test_object)  # Different objects
        assert unpickled.id == test_object.id  # Same id value
    
    def test_get_info(self, test_object: Person) -> None:
        """Test the get_info method of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
        """
        # Get info
        info = test_object.get_info()
        
        # Verify info
        expected = f"{test_object.name}, {test_object.age} years old, Email: {test_object.email}"
        assert info == expected
    
    def test_add_friend(self, test_object: Person, friend_object: Person) -> None:
        """Test the add_friend method of the Person class.
        
        Args:
            test_object: A fixture providing a test Person instance.
            friend_object: A fixture providing a friend Person instance.
        """
        # Add friend
        test_object.add_friend(friend_object)
        
        # Verify friend was added
        assert len(test_object.friends) == 1
        assert test_object.friends[0] is friend_object
        assert test_object.has_friend(friend_object.name)
    
    def test_employee_get_info(self, test_employee: Employee) -> None:
        """Test the get_info method of the Employee class.
        
        Args:
            test_employee: A fixture providing a test Employee instance.
        """
        # Get info
        info = test_employee.get_info()
        
        # Verify info
        expected = (f"{test_employee.name}, {test_employee.age} years old, "
                   f"Email: {test_employee.email}, ID: {test_employee.employee_id}, "
                   f"Department: {test_employee.department}")
        assert info == expected


# Functions #
# Example Sections #
def test_suite_overview():
    """Demonstrates the basic structure and usage of the test suite."""
    print("Test Suite Overview:\n")
    
    # Create test suite instance
    print("Creating a test suite instance...")
    test_suite = PersonTestSuite()
    
    # Show test class
    print(f"Test class: {test_suite.TestClass.__name__}")
    
    # List available test methods
    print("\nAvailable test methods:")
    test_methods = [method for method in dir(test_suite) if method.startswith("test_") and callable(getattr(test_suite, method))]
    for method in test_methods:
        print(f"  - {method}")
    
    # Create test objects
    print("\nCreating test objects...")
    person = Person("John Doe", 35, "john@example.com")
    employee = Employee("Jane Smith", 42, "jane@example.com", "E54321", "Marketing", 85000.0)
    
    print(f"Person: {person.get_info()}")
    print(f"Employee: {employee.get_info()}")
    
    print("\nNote: In a real test environment, these tests would be run using pytest.")
    print("The test suite provides fixtures and test methods that pytest uses to run the tests.")
    print()


def testing_object_copying():
    """Demonstrates testing object copying functionality."""
    print("Testing Object Copying:\n")
    
    # Create test objects
    print("Creating test objects...")
    person = Person("John Doe", 35, "john@example.com")
    friend = Person("Jane Smith", 32, "jane@example.com")
    person.add_friend(friend)
    
    print(f"Original person: {person.get_info()}")
    print(f"Friend: {friend.get_info()}")
    print(f"Person has {len(person.friends)} friend(s)")
    
    # Test shallow copy
    print("\nTesting shallow copy...")
    person_copy = copy.copy(person)
    print(f"Copy is same object as original: {person_copy is person} == False")
    print(f"Copy's friends list is same object as original's: {person_copy.friends is person.friends} == True")
    
    # Modify the friend list in the copy
    print("\nModifying the friend list in the copy...")
    new_friend = Person("Bob Johnson", 40, "bob@example.com")
    person_copy.add_friend(new_friend)
    
    print(f"Original person has {len(person.friends)} friend(s) == 2")
    print(f"Copy has {len(person_copy.friends)} friend(s) == 2")
    print("This demonstrates that changes to mutable attributes in a shallow copy affect the original.")
    
    # Test deep copy
    print("\nTesting deep copy...")
    person = Person("John Doe", 35, "john@example.com")
    friend = Person("Jane Smith", 32, "jane@example.com")
    person.add_friend(friend)
    
    person_deepcopy = copy.deepcopy(person)
    print(f"Deepcopy is same object as original: {person_deepcopy is person} == False")
    print(f"Deepcopy's friends list is same object as original's: {person_deepcopy.friends is person.friends} == False")
    
    # Modify the friend list in the deepcopy
    print("\nModifying the friend list in the deepcopy...")
    new_friend = Person("Bob Johnson", 40, "bob@example.com")
    person_deepcopy.add_friend(new_friend)
    
    print(f"Original person has {len(person.friends)} friend(s) == 1")
    print(f"Deepcopy has {len(person_deepcopy.friends)} friend(s) == 2")
    print("This demonstrates that changes to mutable attributes in a deep copy don't affect the original.")
    print()


def testing_object_pickling():
    """Demonstrates testing object pickling functionality."""
    print("Testing Object Pickling:\n")
    
    # Create test objects
    print("Creating test objects...")
    person = Person("John Doe", 35, "john@example.com")
    friend = Person("Jane Smith", 32, "jane@example.com")
    person.add_friend(friend)
    
    print(f"Original person: {person.get_info()}")
    print(f"Friend: {friend.get_info()}")
    
    # Pickle and unpickle
    print("\nPickling and unpickling the person object...")
    pickled = pickle.dumps(person)
    unpickled = pickle.loads(pickled)
    
    print(f"Unpickled is same object as original: {unpickled is person} == False")
    print(f"Unpickled's friends list is same object as original's: {unpickled.friends is person.friends} == False")
    print(f"Unpickled person: {unpickled.get_info()}")
    print(f"Unpickled has {len(unpickled.friends)} friend(s)")
    print(f"Unpickled friend: {unpickled.friends[0].get_info()}")
    
    print("\nThis demonstrates that pickling creates a complete serialized copy of the object")
    print("that can be restored with all its attributes and relationships intact.")
    print()


def running_tests_manually():
    """Demonstrates how to run tests manually without pytest."""
    print("Running Tests Manually:\n")
    
    # Create test suite instance
    test_suite = PersonTestSuite()
    
    # Create test objects
    person = Person("Test Person", 30, "test@example.com")
    employee = Employee("Test Employee", 35, "employee@example.com", "E12345", "Engineering", 75000.0)
    friend = Person("Test Friend", 28, "friend@example.com")
    
    # Run tests manually
    print("Running test_instance_creation...")
    test_suite.test_instance_creation("Manual Test", 40, "manual@example.com")
    print("✓ test_instance_creation passed")
    
    print("\nRunning test_copy...")
    test_suite.test_copy(person)
    print("✓ test_copy passed")
    
    print("\nRunning test_copy_method...")
    test_suite.test_copy_method(person)
    print("✓ test_copy_method passed")
    
    print("\nRunning test_deepcopy...")
    test_suite.test_deepcopy(person)
    print("✓ test_deepcopy passed")
    
    print("\nRunning test_deepcopy_method...")
    test_suite.test_deepcopy_method(person)
    print("✓ test_deepcopy_method passed")
    
    print("\nRunning test_pickling...")
    test_suite.test_pickling(person)
    print("✓ test_pickling passed")
    
    print("\nRunning test_get_info...")
    test_suite.test_get_info(person)
    print("✓ test_get_info passed")
    
    print("\nRunning test_add_friend...")
    test_suite.test_add_friend(person, friend)
    print("✓ test_add_friend passed")
    
    print("\nRunning test_employee_get_info...")
    test_suite.test_employee_get_info(employee)
    print("✓ test_employee_get_info passed")
    
    print("\nNote: In a real test environment, these tests would be run using pytest,")
    print("which provides better test discovery, reporting, and fixtures management.")
    print()


def extending_test_suite():
    """Demonstrates how to extend the test suite with additional tests."""
    print("Extending Test Suite:\n")
    
    # Define an extended test suite
    class ExtendedPersonTestSuite(PersonTestSuite):
        """Extended test suite with additional tests."""
        
        def test_age_update(self, test_object: Person) -> None:
            """Test updating the age of a person.
            
            Args:
                test_object: A fixture providing a test Person instance.
            """
            # Original age
            original_age = test_object.age
            
            # Update age
            new_age = original_age + 1
            test_object.age = new_age
            
            # Verify age update
            assert test_object.age == new_age
            assert test_object.age != original_age
        
        def test_multiple_friends(self, test_object: Person) -> None:
            """Test adding multiple friends to a person.
            
            Args:
                test_object: A fixture providing a test Person instance.
            """
            # Create friends
            friend1 = Person("Friend 1", 25)
            friend2 = Person("Friend 2", 30)
            friend3 = Person("Friend 3", 35)
            
            # Add friends
            test_object.add_friend(friend1)
            test_object.add_friend(friend2)
            test_object.add_friend(friend3)
            
            # Verify friends were added
            assert len(test_object.friends) == 3
            assert test_object.has_friend("Friend 1")
            assert test_object.has_friend("Friend 2")
            assert test_object.has_friend("Friend 3")
    
    # Create extended test suite instance
    print("Creating an extended test suite instance...")
    extended_test_suite = ExtendedPersonTestSuite()
    
    # List available test methods
    print("\nAvailable test methods (including extended ones):")
    test_methods = [method for method in dir(extended_test_suite) if method.startswith("test_") and callable(getattr(extended_test_suite, method))]
    for method in test_methods:
        print(f"  - {method}")
    
    # Create test object
    person = Person("Extended Test Person", 45, "extended@example.com")
    
    # Run extended tests manually
    print("\nRunning extended tests...")
    print("Running test_age_update...")
    extended_test_suite.test_age_update(person)
    print("✓ test_age_update passed")
    
    print("\nRunning test_multiple_friends...")
    # Reset person for this test
    person = Person("Extended Test Person", 45, "extended@example.com")
    extended_test_suite.test_multiple_friends(person)
    print("✓ test_multiple_friends passed")
    
    print("\nNote: The extended test suite inherits all test methods from the base test suite,")
    print("while adding new test methods specific to the extended functionality.")
    print()


# Main #
if __name__ == "__main__":
    # Demonstrate test suite overview
    test_suite_overview()
    
    # Demonstrate testing object copying
    testing_object_copying()
    
    # Demonstrate testing object pickling
    testing_object_pickling()
    
    # Demonstrate running tests manually
    running_tests_manually()
    
    # Demonstrate extending the test suite
    extending_test_suite()