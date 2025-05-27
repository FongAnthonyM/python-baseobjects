# Anthony's Python Style Guide: Examples

## Table of Contents

- [1 Background](#1-background)
- [2 Directory Hierarchy](#2-directory-hierarchy)
- [3 Example-Specific File Structure Guidelines](#3-example-specific-file-structure-guidelines)
  - [3.1 Example-Specific File Header](#31-example-specific-file-header)
  - [3.2 Main Section for Examples](#32-main-section-for-examples)
- [4 Example-Specific Documentation](#4-example-specific-documentation)
  - [4.1 Print Statements](#41-print-statements)
  - [4.2 Error Handling](#42-error-handling)
- [5 Example Content Guidelines](#5-example-content-guidelines)
  - [5.1 Self-Contained Examples](#51-self-contained-examples)
  - [5.2 Progressive Complexity](#52-progressive-complexity)
  - [5.3 Real-World Scenarios](#53-real-world-scenarios)
  - [5.4 Edge Cases](#54-edge-cases)
- [6 Example Styles](#6-example-styles)
  - [6.1 Cookbook Style](#61-cookbook-style)
  - [6.2 Compare and Contrast](#62-compare-and-contrast)
  - [6.3 Step-by-Step Transformation](#63-step-by-step-transformation)
  - [6.4 Annotated Examples](#64-annotated-examples)
  - [6.5 Interactive Examples](#65-interactive-examples)
  - [6.6 Error-Driven Learning](#66-error-driven-learning)
  - [6.7 Incremental Complexity](#67-incremental-complexity)
  - [6.8 Visual Learning](#68-visual-learning)
  - [6.9 Example Styles Conclusions](#69-example-styles-conclusions)
- [7 Example-Specific Best Practices](#7-example-specific-best-practices)
- [8 Testing Examples](#8-testing-examples)


## 1 Background

Examples are crucial for helping users understand how to use a library or framework. They provide practical 
demonstrations of the library's functionality and serve as reference implementations for common use cases. Well-crafted 
examples can significantly reduce the learning curve for new users and serve as a quick reference for experienced users.

Examples are supplementary to the library's documentation. While tutorials and reference guides provide a conceptual 
overview of the library and are meant to educate users on its features and usage, examples provide more in-depth 
explanations and demonstrations on how to use the library in real-world scenarios. Additionally, examples are written in 
Python files rather than Jupyter notebooks, so it is easier to implement their content into other projects.

This document provides guidelines specific to creating effective examples for Python packages. It focuses on 
example-specific considerations while referencing other style guides for general Python coding practices:

- For general Python code style and syntax, refer to [Syntactic Guidelines](syntactic_guidelines.md)
- For file structure and organization, refer to [Code and File Layout](code_file_layout.md)
- For semantic aspects of code, refer to [Semantics Guidelines](semantics_guidelines.md)

The Examples Guidelines is built upon these foundational documents, adding specific guidance for creating educational 
and demonstrative code examples.


## 2 Directory Hierarchy

Examples should be organized in a directory structure that mirrors the package structure. This makes it easy for users 
to find examples relevant to the specific components they're interested in.

- Each major package should have its own directory under the `examples/` directory
- Subpackages should have their own subdirectories when they contain multiple components
- Related examples should be grouped together in the same directory
- Filenames should start with descriptive name followed by `_example` (e.g., `name_example.py`).
- Use the format `<component_name>_example.py` for individual component examples
- For examples that demonstrate multiple components working together, use a descriptive name that indicates the functionality being demonstrated, e.g., `caching_with_sentinel_example.py`
- Use lowercase with underscores for file names (snake_case)

Example:
```
examples/
  bases/                          # Examples for the bases package
    collections/                  # Examples for the bases.collections subpackage
      baseobject_example.py
    basecallable_example.py
    sentinelobject_example.py
    ...
    cachingtools/                 # Examples for the cachingtools package
      caches/                     # Examples for the cachingtools.caches subpackage
      cachingobject_example.py
      ...
```


## 3 Example-Specific File Structure Guidelines

Example files should follow the general Python file layout guidelines as described in [Code and File Layout](code_file_layout.md), 
with some additional example-specific considerations outlined below.


### 3.1 Example-Specific File Header

In addition to the standard file header requirements, example files should include a docstring that clearly explains:

1. What the example demonstrates
2. A numbered list of key concepts or features being demonstrated

Example:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" sentinelobject_example.py
An example of how to create and use SentinelObject.

This example demonstrates:
1. Creating custom sentinel objects
2. Using sentinel objects as markers
3. Using sentinel objects in dictionaries
4. Comparing sentinel objects
"""
```

For general file header guidelines, imports organization, and definitions structure, refer to the [Code and File Layout](code_file_layout.md) document.


### 3.2 Main Section for Examples

The main section in example files is particularly important as it demonstrates the usage of the defined classes and functions:

1. Include a `if __name__ == "__main__":` block
2. Organize demonstrations in a logical sequence, from basic to advanced
3. Use print statements to explain what's happening and show results
4. Include comments to explain the purpose of each demonstration

Example:
```python
# Main #
if __name__ == "__main__":
    # Create a data processor with some sample data
    print("Creating a data processor...")
    processor = DataProcessor({
        "item1": 10,
        "item2": "Hello",
        "item3": [1, 2, 3]
    })

    # Demonstrate basic caching
    print("\nDemonstrating basic caching with timed_cache...")
    print("First call (not cached):")
    result1 = processor.process_data("item1")
    print(f"Result: {result1}")

    # More demonstrations...
```


## 4 Example-Specific Documentation

For general code style, docstrings, and comments guidelines, refer to the [Syntactic Guidelines](syntactic_guidelines.md)
document, particularly sections 2.10 (Docstrings) and 2.11 (Comments). The following sections cover documentation 
aspects specific to example files.


### 4.1 Print Statements

Print statements in examples serve as a narrative to guide the user through the demonstration:

1. Use print statements to indicate what's being demonstrated
2. Print input values and results to show the effect of operations
3. Use descriptive messages that explain what's happening
4. Format output to make it easy to read and understand

Example:

```python
print("\nDemonstrating LRU cache with maxsize=2...")
print("Processing item1:")
advanced1 = processor.advanced_process("item1", 2)
print(f"Result: {advanced1}")
```

### 4.2 Error Handling

Examples should demonstrate proper error handling:

1. Show how to handle common exceptions
2. Demonstrate best practices for error recovery
3. Include examples of input validation and error prevention

Example:

```python
try:
    result = processor.process_data(user_input)
    print(f"Result: {result}")
except KeyError:
    print(f"Error: Key '{user_input}' not found in data")
except Exception as e:
    print(f"Unexpected error: {e}")
```


## 5 Example Content Guidelines
### 5.1 Self-Contained Examples

Examples should be self-contained and runnable without external dependencies:

1. Include all necessary imports
2. Generate sample data within the example
3. Avoid reliance on external files or services
4. If external resources are necessary, provide clear instructions or mock the data

Example:

```python
# Generate sample data
data = {
    "item1": 10,
    "item2": "Hello",
    "item3": [1, 2, 3]
}

# Use the generated data in the example
processor = DataProcessor(data)
```

### 5.2 Progressive Complexity

Structure examples to progress from simple to complex:

1. Start with basic usage that demonstrates core functionality
2. Gradually introduce more advanced features
3. Build on previous concepts to show how components work together
4. End with complex, real-world scenarios that showcase the full power of the library

Example:

```python
# Basic usage
print("Basic usage:")
result = processor.process_data("item1")

# Advanced usage
print("\nAdvanced usage:")
advanced_result = processor.advanced_process("item1", factor=2)

# Complex scenario
print("\nComplex scenario:")
# Demonstrate multiple components working together
```

### 5.3 Real-World Scenarios

Include examples that demonstrate real-world use cases:

1. Show how the library solves common problems
2. Demonstrate integration with other libraries or systems
3. Include scenarios that users are likely to encounter
4. Provide context for why certain approaches are beneficial

Example:

```python
# Real-world scenario: Caching expensive API calls
print("\nScenario: Caching expensive API calls")
api_client = APIClient()
cached_api = CachedAPIClient(api_client)

# First call (not cached)
print("First call (not cached):")
result1 = cached_api.get_data("endpoint1")

# Second call (cached)
print("\nSecond call (cached):")
result2 = cached_api.get_data("endpoint1")
```

### 5.4 Edge Cases

Include examples that demonstrate how to handle edge cases:

1. Show how the library behaves with unusual inputs
2. Demonstrate error handling for invalid inputs
3. Include examples of boundary conditions
4. Show how to handle resource constraints or performance issues

Example:

```python
# Edge case: Empty input
print("\nEdge case: Empty input")
result = processor.process_data("")

# Edge case: Very large input
print("\nEdge case: Very large input")
large_key = "x" * 1000
result = processor.process_data(large_key)
```

## 6 Example Styles

Different example styles can be used to enhance the learning experience for users. Each style has its own strengths and 
is suitable for different learning objectives. The following sections provide an overview of the different styles and 
examples that demonstrate them.

### 6.1 Cookbook Style

Provides practical, ready-to-use code snippets for common tasks.
   - Format as problem-solution pairs
   - Include brief explanations of why the solution works
   - Focus on practical utility over theoretical understanding

```python
# Problem: How to efficiently filter a dictionary by value
# Solution:
data = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered = {k: v for k, v in data.items() if v > 2}
print(f"Filtered dictionary: {filtered}")  # Output: Filtered dictionary: {'c': 3, 'd': 4}
```

### 6.2 Compare and Contrast

Shows multiple approaches to solving the same problem, highlighting trade-offs.
   - Present at least two different implementations
   - Explain the advantages and disadvantages of each approach
   - Include performance considerations when relevant

```python
# Approach 1: Using a for loop (more readable)
print("Approach 1: Using a for loop")
result1 = []
for item in data:
    if process_condition(item):
        result1.append(transform(item))
print(f"Result: {result1}")

# Approach 2: Using a list comprehension (more concise)
print("\nApproach 2: Using a list comprehension")
result2 = [transform(item) for item in data if process_condition(item)]
print(f"Result: {result2}")
```

### 6.3 Step-by-Step Transformation

Shows the evolution of data through a series of operations.
   - Start with initial data
   - Apply transformations one at a time
   - Show intermediate results after each step

```python
# Initial data
data = [1, 2, 3, 4, 5]
print(f"Initial data: {data}")

# Step 1: Square each number
squared = [x**2 for x in data]
print(f"After squaring: {squared}")

# Step 2: Filter out values less than 10
filtered = [x for x in squared if x >= 10]
print(f"After filtering: {filtered}")

# Step 3: Calculate the sum
total = sum(filtered)
print(f"Final result (sum): {total}")
```

### 6.4 Annotated Examples

Code examples with detailed comments explaining each line or block.
   - Add comments that explain not just what the code does, but why
   - Highlight important concepts or patterns
   - Use consistent comment style throughout

```python
# Create a processor with caching capabilities
processor = DataProcessor(
    cache_enabled=True,  # Enable caching for better performance
    max_cache_size=100,  # Limit cache size to prevent memory issues
    ttl=3600  # Set time-to-live for cache entries (in seconds)
)

# Process data with automatic caching
# The first call will be slow as it computes the result
result1 = processor.process("example_key")  
print(f"First call result: {result1}")

# The second call will be fast as it retrieves from cache
result2 = processor.process("example_key")  
print(f"Second call result: {result2}")
```

### 6.5 Interactive Examples

Examples that encourage users to modify parameters and observe different outcomes.
   - Provide a base example that works
   - Suggest modifications for users to try
   - Explain expected outcomes for different modifications

```python
# Base example - try modifying the parameters!
def calculate_result(x, y, operation="add"):
    """Calculate result based on operation.

    Try changing:
    - x and y to different numbers
    - operation to "subtract", "multiply", or "divide"
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        return x / y if y != 0 else "Error: Division by zero"

# Example usage
x, y = 10, 5
operation = "add"  # Try changing this!
result = calculate_result(x, y, operation)
print(f"{x} {operation} {y} = {result}")
```

### 6.6 Error-Driven Learning

Examples that intentionally show common errors and how to fix them.
   - Show incorrect code first
   - Explain why it's wrong and what error it produces
   - Provide the corrected version

```python
# INCORRECT: This will raise a KeyError
print("Incorrect approach:")
try:
    data = {"a": 1, "b": 2}
    value = data["c"]  # KeyError: 'c'
    print(f"Value: {value}")
except KeyError as e:
    print(f"Error: {e}")

# CORRECT: Using get() method with a default value
print("\nCorrect approach:")
data = {"a": 1, "b": 2}
value = data.get("c", 0)  # Returns 0 if key doesn't exist
print(f"Value: {value}")
```

### 6.7 Incremental Complexity

Start with a minimal example and gradually add features.
   - Begin with the simplest possible implementation
   - Add complexity one feature at a time
   - Explain each addition and its purpose

```python
# Stage 1: Basic implementation
print("Stage 1: Basic implementation")
cache = {}
result1 = cache.get("key", None)
if result1 is None:
    result1 = expensive_computation("key")
    cache["key"] = result1
print(f"Result: {result1}")

# Stage 2: Add timeout functionality
print("\nStage 2: Add timeout functionality")
cache_with_time = {}
current_time = time.time()
key = "example_key"
result2 = None

# Check if key exists and is not expired
if key in cache_with_time:
    timestamp, value = cache_with_time[key]
    if current_time - timestamp < 3600:  # 1 hour timeout
        result2 = value

# If not in cache or expired, compute and store
if result2 is None:
    result2 = expensive_computation(key)
    cache_with_time[key] = (current_time, result2)

print(f"Result: {result2}")
```

### 6.8 Visual Learning

Use ASCII art, tables, or other visual representations to illustrate concepts.
   - Use visual elements to clarify complex relationships or structures
   - Ensure visuals are readable in monospace font
   - Include explanatory text alongside visuals

```python
# Example of a binary tree structure
"""
Binary Tree:
       A
     /   \
    B     C
   / \   / \
  D   E F   G

Traversal order:
- In-order: D, B, E, A, F, C, G
- Pre-order: A, B, D, E, C, F, G
- Post-order: D, E, B, F, G, C, A
"""

# Implementation of a simple binary tree
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Create the tree structure shown above
root = Node("A")
root.left = Node("B")
root.right = Node("C")
root.left.left = Node("D")
root.left.right = Node("E")
root.right.left = Node("F")
root.right.right = Node("G")
```

### 6.9 Example Styles Conclusions
When creating examples, consider which style or combination of styles will best help users understand the concept being 
demonstrated. Different styles are more effective for different types of learning objectives:

- Use **Cookbook Style** for practical, task-oriented learning
- Use **Compare and Contrast** to develop critical thinking about implementation choices
- Use **Step-by-Step Transformation** to show data flow and processing pipelines
- Use **Annotated Examples** for detailed understanding of complex code
- Use **Interactive Examples** to encourage experimentation and active learning
- Use **Error-Driven Learning** to help users avoid common pitfalls
- Use **Incremental Complexity** for building comprehensive understanding of complex features
- Use **Visual Learning** for concepts that benefit from spatial or structural representation

For this style guide, primarily a mixture of Step-by-Step Transformation, Annotated Examples, Interactive Examples, and 
Incremental Complexity are suggested because other sections of the project should cover the goals of the other styles.  


## 7 Example-Specific Best Practices

For general code readability, performance, and maintainability guidelines, refer to the 
[Syntactic Guidelines](syntactic_guidelines.md) and [Semantics Guidelines](semantics_guidelines.md) documents. The 
following are best practices specific to example files:

- **Educational Focus**: Examples should prioritize clarity and educational value over code optimization. Sometimes a slightly less efficient approach may be more instructive.
- **Comparative Approaches**: When relevant, show both basic/simple approaches and more advanced/efficient approaches to demonstrate the benefits of different techniques:
```python
# Basic approach (for clarity)
print("\nBasic approach:")
for key in data:
    result = processor.process_data(key)
    print(f"{key}: {result}")

# Advanced approach (for efficiency)
print("\nAdvanced approach:")
keys = list(data.keys())
results = [processor.process_data(key) for key in keys]
for key, result in zip(keys, results):
    print(f"{key}: {result}")
```
- **Explicit Constants**: Use named constants for values that might be referenced multiple times or that have special meaning:
```python
# Constants
CACHE_LIFETIME = 5  # seconds
MAX_CACHE_SIZE = 100  # items

# Use constants instead of hardcoded values
processor.set_lifetimes(CACHE_LIFETIME)
processor.set_maxsize(MAX_CACHE_SIZE)
```

- **Self-Contained**: Examples should be runnable without requiring external files or dependencies beyond the library itself.
- **Progressive Disclosure**: Structure examples to start with basic concepts and gradually introduce more complex features.
- **Tests as Inspiration**: If there are unit tests, use them as a reference but do not copy them exactly. The examples should 
  educate the user on how to use key aspects of the module and how they can use it to create new programs, not just 
  test it.

## 8 Testing Examples

Examples should be tested to ensure they work as expected:

1. Run each example to verify it produces the expected output
2. Test examples with different Python versions if the library supports multiple versions
3. Verify that examples work with the latest version of the library
4. Include comments about expected output or behavior

Example:

```python
# This should print:
# Result: Processed: 10
result = processor.process_data("item1")
print(f"Result: {result}")
```

By following these guidelines, you can create examples that effectively demonstrate the functionality of your library and help users understand how to use it in their own projects.
