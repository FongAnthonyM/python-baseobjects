# Anthony's Python Style Guide: Unit Tests

## Table of Contents

- [1 Background](#1-background)
- [2 pytest](#2-pytest)
- [3 Directory Hierarchy](#3-directory-hierarchy)
- [4 Test Structure](#4-test-structure)
  - [4.1 Test Classes](#41-test-classes)
  - [4.2 Test Methods](#42-test-methods)
  - [4.3 Main](#43-main)
- [5 Test Semantics and Syntax](#5-test-semantics-and-syntax)
  - [5.1 Assertions](#51-assertions)
  - [5.2 Fixtures](#52-fixtures)
  - [5.3 Test Doubles](#53-test-doubles)
- [6 Test Execution](#6-test-execution)


## 1 Background

Unit tests are used to verify the correctness of the code being tested to ensure that it is working as expected. 
Typically, unit tests are written to verify individual components of the code.

Unit tests follow the guidelines set forth by the general styleguide such as the code organization, file structure, 
naming conventions, docstrings, and other standard practices in:

- [Code File Layout](code_file_layout.md) - For file organization and structure
- [Syntactic Guidelines](syntactic_guidelines.md) - For naming conventions, docstrings, and code formatting
- [Semantics Guidelines](semantics_guidelines.md) - For general code organization principles

The guidelines in this document are supplemental to the general guidelines and focus on test-specific code to ensure 
consistency, maintainability, and effectiveness of the test suite across the project.


## 2 pytest

**pytest** testing framework is the preferred framework for Python projects, as it provides more features and 
flexibility than python's unittest library.

In pytest, tests can be created by defining a test function with a `test_` prefix. pytest can then run the tests using 
its Python or command line interface and display diagnostics about the tests. Additionally, the pytest API offers an 
extensive array of options for customizing the run conditions and diagnostic information of these tests. For more 
information on pytest, see the [pytest documentation](https://docs.pytest.org/en/latest/).

The pytest package has many features, and this styleguide will offer guidance on how to use them. 


## 3 Directory Hierarchy

Tests should be organized in a directory structure that mirrors the package structure. This makes it easy for users to 
find tests relevant to the specific components they're interested in. It also allows pytest to automatically discover 
tests when running the tests using the `pytest` command.

- Each major package should have its own directory under the `tests/` directory
- Subpackages should have their own subdirectories when they contain multiple components
- Additional subdirectories can be used to group tests by functionality.
- Related tests should be grouped together in the same directory
- Filenames should start with descriptive name followed by `_test` (e.g., `name_test.py`).
- Additional files can be used to contain fixtures, test doubles, test base classes, or other test-specific code.

Example:
```
tests/
  bases/                        # Tests for the bases package
    collections/                # Tests for the bases.collections subpackage
      baseobject_test.py
    basecallable_test.py
    sentinelobject_test.py
    ...
  cachingtools/                 # Tests for the cachingtools package
    caches/                     # Tests for the cachingtools.caches subpackage
    cachingobject_test.py
    ...
```


## 4 Test Structure

The purpose of test code is to not only verify that the code is working as expected, but also provide a set of tools for
testing extensions of the code. For example, a class may outline functionality that is not implemented yet or may be
changed in the future, but the test code should still verify that the class is working as expected.

In pytests, tests themselves can be organized into classes and sub-classed which can be used to parameterize tests or 
create test suites to verify different implementations of the code.

For creating documentation, follow the general docstring guidelines in [Syntactic Guidelines](syntactic_guidelines.md), 
section 2.10, with special attention to section 2.10.1.1 for test modules.


### 4.1 Test Classes
Test classes should be used to group related test methods and create test suites. Base test classes should be created to 
provide consistent testing patterns across the project.

Test classes should inherit from appropriate base test classes to ensure consistent testing patterns across the project.

Guidelines:
- Test classes should be named with a `Test` prefix followed by the name of the class being tested
- Test classes should inherit from an appropriate base test class (e.g., `ClassTest`, `BaseBaseObjectTest`)
- Test classes should include a descriptive docstring explaining what is being tested
- Test classes should contain most of their resources within their scope so the resource may be changed to suit different test variations.
  - Test involving defining classes should either be defined as inner classes or defined elsewhere and assigned to a class attribute.
  - Test involving defining functions should either be defined as inner functions or defined elsewhere and assigned to a class attribute. 
- Test classes should define a `class_` attribute that points to the class being tested such that the tested class can interchanged with other similar classes which will be tested using the same test suite.

Example:
```python
class TestBaseObject(BaseBaseObjectTest):
    """Test the BaseObject class.

    This class tests the functionality of the BaseObject class, which is the base class for all objects in the
    baseobjects package. It creates a test subclass of BaseObject to test with.
    """

    # Class Definitions #
    class BaseTestObject(BaseObject):
        """A subclass of BaseObject for testing purposes."""
        # Implementation...

    # Attributes #
    class_: Type[BaseTestObject] = BaseTestObject

    # Test methods...
```

For test method naming and organization, follow the general method guidelines in [Syntactic Guidelines](syntactic_guidelines.md) 
and [Code File Layout](code_file_layout.md), with the additional requirement that test methods should be named with a `test_` prefix 
followed by a descriptive name of what is being tested.


### 4.2 Test Methods

Test methods should be designed to test a specific aspect of the class or function being tested. Each test method should be focused, 
independent, and provide clear feedback when it fails.

Guidelines:
- Test methods should be named with a `test_` prefix followed by a descriptive name of what is being tested
- Test methods should include a descriptive docstring explaining what is being tested
- Test methods should use type hints for parameters and return values
- Test methods should be independent and not rely on the state from other tests
- Test methods should be focused on testing a single aspect of behavior
- Test methods should include assertions to verify the expected behavior
- Test methods should handle both normal and edge cases
- Test methods can use attributes provided by the test class (allows more options as a test suite)

Example:
```python
def test_deepcopy(self, test_object: 'TestBaseObject.BaseTestObject') -> None:
    """Test the deep copy behavior of BaseObject.

    This test verifies that deepcopy creates a new object with new mutable attributes
    but the same immutable attributes.

    Args:
        test_object: A fixture providing a BaseTestObject instance.
    """
    # Perform the operation being tested
    new = copy.deepcopy(test_object)

    # Assert the expected behavior
    assert new is not test_object
    assert id(new.immutable) == id(test_object.immutable)
    assert id(new.mutable) != id(test_object.mutable)
    assert new.mutable == test_object.mutable
```

When creating test methods that test similar functionality across different implementations, consider using parameterized tests
to reduce code duplication and ensure consistent testing.


### 4.3 Main

Test files should include a `__main__` block for running the tests directly. Mainly it sets the run options for pytest
for the tests in the file.

Example:
```python
# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
```


## 5 Test Semantics and Syntax

Tests should conform to the structure described in [Test Structure](#4-test-structure), but in some cases it 
may be necessary to deviate from the general structure. The following sections should be followed regardless of the test 
structure.


### 5.1 Assertions

Assertions are a base Python feature that allows for checking the state of a program at runtime and are used by pytest 
as the primary means of verifying test conditions. Assertions are discouraged in source code because they do not conform 
to Python's error handling principles. However, assertions are permitted for debugging, testing, examples, and tutorials 
because assertions are good for explaining the behavior of a program, and in these scenarios error handling 
is managed by the user rather than the program. 

Guidelines:
- Use pytest's built-in assertions rather than Python's `assert` statement when possible
- Each test should include at least one assertion
- Assertions should be specific and verify a single aspect of behavior
- Use appropriate assertion methods for the type of comparison being made
- Include descriptive error messages in assertions to make test failures more informative

Example:
```python
# Simple assertions
assert result == expected
assert instance is not None

# More complex assertions
assert id(new.immutable) == id(test_object.immutable)
assert id(new.mutable) != id(test_object.mutable)
assert unpickled.immutable == test_object.immutable
assert unpickled.mutable == test_object.mutable
assert unpickled is not test_object
```


### 5.2 Fixtures

Fixtures are a powerful feature of pytest that allow for setup and teardown of test environments.

Guidelines:
- Fixtures should be used for setting up test environments and creating test objects
- Fixtures should be defined at the appropriate scope (function, class, module, or session)
- Fixtures should include a descriptive docstring explaining their purpose and return value
- Fixtures should use type hints for parameters and return values
- Common fixtures should be defined in base test modules
- Fixtures should be organized under a `# Fixtures` comment

Example:
```python
# Fixtures
@pytest.fixture
def test_object(self) -> 'TestBaseObject.BaseTestObject':
    """Create a test object instance for use in tests.

    Returns:
        BaseTestObject: An instance of the test class.
    """
    return self.class_()

@pytest.fixture
def tmp_dir(tmpdir: Any) -> Path:
    """A pytest fixture that turns the tmpdir into a Path object.

    Args:
        tmpdir: A pytest tmpdir fixture.

    Returns:
        Path: A pathlib.Path object representing the temporary directory.
    """
    return Path(tmpdir)
```

### 5.3 Test Doubles

Test doubles (mocks, stubs, fakes, etc.) are used to isolate the code being tested from its dependencies.

Guidelines:
- Use test doubles to isolate the code being tested from its dependencies
- Use the appropriate type of test double for the situation:
  - Stubs: Return predefined values
  - Mocks: Verify interactions
  - Fakes: Simplified implementations
  - Spies: Record interactions
- Use pytest's monkeypatch fixture for patching functions and methods
- Use unittest.mock for creating mock objects
- Reset or tear down test doubles after use

Example:
```python
def test_with_mock(self, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test with a mock object.

    This test uses a mock object to verify that the correct method is called.

    Args:
        monkeypatch: A pytest fixture for patching functions and methods.
    """
    # Create a mock object
    mock = unittest.mock.Mock()

    # Patch a method to use the mock
    monkeypatch.setattr(self.class_, "some_method", mock)

    # Call the method that should use the patched method
    instance = self.class_()
    instance.method_under_test()

    # Verify the mock was called correctly
    mock.assert_called_once_with(expected_args)
```


## 6 Test Execution

Tests should be easy to run and provide clear feedback on failures.

Guidelines:
- Tests should be runnable using pytest
- Tests should be runnable individually or as part of a test suite
- Tests should provide clear error messages on failure
- Tests should clean up after themselves
- Tests should not depend on the order of execution

Running tests:
```bash
# Run all tests
pytest

# Run tests in a specific file
pytest tests/bases/test_baseobject.py

# Run a specific test
pytest tests/bases/test_baseobject.py::TestBaseObject::test_deepcopy

# Run tests with verbose output
pytest -v

# Run tests with output capturing disabled
pytest -s
```
