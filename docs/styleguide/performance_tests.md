# Anthony's Python Style Guide: Performance Tests

## Table of Contents

- [1 Background](#1-background)
- [2 Directory Hierarchy](#2-directory-hierarchy)
- [3 Performance Test Structure](#3-performance-test-structure)
  - [3.1 Base Performance Classes](#31-base-performance-classes)
  - [3.2 Performance Test Classes](#32-performance-test-classes)
  - [3.3 Test Methods](#33-test-methods)
- [4 Performance Test Semantics and Syntax](#4-performance-test-semantics-and-syntax)
- [5 Common Patterns](#5-common-patterns)
  - [5.1 Comparing with Standard Library](#51-comparing-with-standard-library)
  - [5.2 Comparing Implementation Variants](#52-comparing-implementation-variants)
  - [5.3 Measuring Overhead](#53-measuring-overhead)


## 1 Background

Performance testing is a critical aspect of software development that ensures code not only functions correctly but also 
executes efficiently. These tests help identify performance regressions, validate optimizations, and ensure that 
implementations meet performance requirements.

The performance tests in this guide are designed around the unit testing framework described in 
[Unit Tests](unit_tests.md) as test performance should be tested against individual components of the code similar to 
unit tests.

Unlike unit tests that verify functional correctness, performance tests measure execution time, memory usage, and other 
performance metrics. They often compare the performance of custom implementations against standard library equivalents 
or previous versions to ensure that optimizations are effective and that new features don't introduce performance 
regressions.

Performance tests are not required for all modules and classes, but they should be created for any that may have a 
significant performance impact.

This document focuses on performance test-specific aspects. For general code organization, file structure, naming 
conventions, docstrings, and other standard practices, please refer to:

- [Code File Layout](code_file_layout.md) - For file organization and structure
- [Syntactic Guidelines](syntactic_guidelines.md) - For naming conventions, docstrings, and code formatting
- [Semantics Guidelines](semantics_guidelines.md) - For general code organization principles
- [Unit Tests](unit_tests.md) - For general testing practices and patterns


### 2 Directory Hierarchy

Performance tests should follow a specific directory structure to separate them from regular unit tests:

- Each module should have a corresponding `performance` directory in the `tests` directory
- Performance tests for a module should be placed in the corresponding `performance` directory
- Filenames should start with descriptive name followed by `_performance` (e.g., `name_performance.py`).
- Additional files can be used to contain fixtures, test doubles, performance base classes, or other performance-specific code.

Example:
```
tests/
  bases/                            # Tests for the bases package
    performance/                    # Performance tests for the bases package
      baseobject_performance.py
      basecallable_performance.py
      ...
  cachingtools/
    performance/
      ...
```


## 3 Performance Test Structure

The purpose of performance tests is to not only measure the performance of individual components of the code, but also 
provide a set of tools for measuring the performance of extensions to the code.


### 3.1 Base Performance Classes

The baseobjects package provides base classes for performance testing that should be used as the foundation for all 
performance tests. These classes provide common functionality and ensure consistency across performance tests.

- `PerformanceTest`: The abstract base class for all performance tests
- `ClassPerformanceTest`: For testing class performance
- `BaseBaseObjectPerformanceTest`: For testing BaseObject subclasses

Example:
```python
class PerformanceTest(abc.ABC):
    """Default performance tests that all classes should pass.

    This is an abstract base class that defines the interface for all performance test classes.

    Attributes:
        timeit_runs: The number of runs to use for timeit measurements.
        speed_tolerance: The maximum percentage of time a new implementation can take compared to the old one.
        _base_time: The time it takes to run a simple function call for a baseline of 100 million iterations.
        call_speed: The baseline speed of a simple function call in microseconds.
    """
    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Calculate the baseline speed of a simple function call in microseconds
    _base_time: float = timeit.timeit(lambda: None, number=10000000)
    call_speed: float = _base_time / 10000000 * 1000000
```


### 3.2 Performance Test Classes

Performance test classes should inherit from the appropriate base performance class and follow the general test class 
guidelines in [Unit Testing Guidelines](unit_tests.md), section 2.1, with the following additional requirements 
specific to performance testing:

- Test classes should define comparison objects that match the functionality of the test objects but use standard library or alternative implementations
- Test classes should define performance-specific attributes like `timeit_runs` and `speed_tolerance`

Example:
```python
class TestBaseObject(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseObject class.

    This class tests the performance of the BaseObject class, which is the base class for all objects in the baseobjects
    package. It creates a test subclass of BaseObject to test with.
    """
    # Class Definitions #
    class BaseTestObject(BaseObject):
        """A subclass of BaseObject for testing purposes."""
        # Implementation...

    class NormalObject(object):
        """A normal Python object for comparison with BaseObject."""
        # Implementation...

    # Attributes #
    class_: Type[BaseTestObject] = BaseTestObject
    timeit_runs: int = 100000
    speed_tolerance: int = 150
```


### 3.3 Test Methods

Performance test methods should follow the general test method guidelines in [Unit Testing Guidelines](unit_tests.md), with the 
following additional requirements specific to performance testing:

- Test methods should be focused on measuring a specific performance aspect (speed, memory usage, etc.)
- Test methods should include performance-specific assertions that verify metrics meet requirements
- Test methods should include detailed performance reporting for analysis
- Assert that the percentage comparison is below the threshold
- Use different thresholds for different types of operations if necessary

Example:
```python
def test_copy_speed(self, test_object: "TestBaseObject.BaseTestObject") -> None:
    """Test the performance of the copy method of BaseObject.

    This test compares the speed of BaseObject.copy() with the standard copy.copy() function.

    Args:
        test_object: A fixture providing a BaseTestObject instance.
    """
    normal = self.NormalObject()

    def normal_copy() -> None:
        copy.copy(normal)

    # Calculate the mean time in microseconds for the new implementation
    new_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
    mean_new = new_time / self.timeit_runs * 1000000

    # Calculate the mean time in microseconds for the old implementation
    old_time = timeit.timeit(normal_copy, number=self.timeit_runs)
    mean_old = old_time / self.timeit_runs * 1000000
    percent = (mean_new / mean_old) * 100

    # Print the performance comparison
    print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
    assert percent < self.speed_tolerance
```


## 4 Performance Test Semantics and Syntax

Performance tests should conform to the structure described in [Performance Test Structure](#3-performance-test-structure), 
but in some cases it may be necessary to deviate from the general structure. The following sections should be followed 
regardless of the test structure.


### 4.1 Benchmarking

Performance tests should use the `timeit` module for benchmarking. The following guidelines should be followed:

- Use the `timeit` module for measuring execution time
- Use a sufficient number of iterations to get reliable measurements (defined in `timeit_runs`)
- Report times in microseconds for better readability
- Calculate and report the percentage comparison between implementations


### 4.2 Comparison Methodology

Performance tests should compare the performance of custom implementations against standard library equivalents or other reference implementations:

- Define functions that perform equivalent operations using different implementations
- Ensure that the compared operations are truly equivalent
- Use the same input data for all implementations
- Isolate the specific operation being tested

Example:
```python
def normal_copy() -> None:
    copy.copy(normal)

# vs.

test_object.copy()
```

### 4.3 Measurement and Reporting

Performance measurements should be accurate, consistent, and informative:

- Use the `timeit` module with a sufficient number of iterations
- Calculate mean execution time per operation
- Convert times to microseconds for better readability
- Calculate and report the percentage comparison between implementations
- Print detailed performance information for debugging

Example:
```python
# Calculate the mean time in microseconds for the new implementation
new_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
mean_new = new_time / self.timeit_runs * 1000000

# Calculate the mean time in microseconds for the old implementation
old_time = timeit.timeit(normal_copy, number=self.timeit_runs)
mean_old = old_time / self.timeit_runs * 1000000
percent = (mean_new / mean_old) * 100

# Print the performance comparison
print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
```

## 5 Common Patterns
### 5.1 Comparing with Standard Library

A common pattern is to compare the performance of custom implementations against standard library equivalents:

```python
def test_copy_speed(self, test_object):
    """Test the performance of the copy method of BaseObject."""
    normal = self.NormalObject()

    def normal_copy():
        copy.copy(normal)

    # Compare custom implementation with standard library
    new_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
    old_time = timeit.timeit(normal_copy, number=self.timeit_runs)
    # ...
```

### 5.2 Comparing Implementation Variants

Another pattern is to compare different implementation variants:

```python
def test_copy_vs_dunder_copy(self, test_object):
    """Test the performance difference between copy() and __copy__() methods."""
    # Compare two different implementations
    copy_time = timeit.timeit(test_object.copy, number=self.timeit_runs)
    dunder_time = timeit.timeit(test_object.__copy__, number=self.timeit_runs)
    # ...
```

### 5.3 Measuring Overhead

Performance tests can also measure the overhead of additional functionality:

```python
def test_attribute_access_speed(self, test_object):
    """Test the performance of attribute access in BaseObject."""
    normal = self.NormalObject()

    def access_base_attr():
        _ = test_object.immutable
        _ = test_object.mutable

    def access_normal_attr():
        _ = normal.immutable
        _ = normal.mutable

    # Measure overhead of BaseObject attribute access
    base_time = timeit.timeit(access_base_attr, number=self.timeit_runs)
    normal_time = timeit.timeit(access_normal_attr, number=self.timeit_runs)
    # ...
```

By following these guidelines, you can create effective performance tests that help ensure the efficiency and reliability of your code.
