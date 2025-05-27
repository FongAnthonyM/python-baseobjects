# Anthony's Python Style Guide: Code and File Layout

## Table of Contents

- [1 Background](#1-background)
- [2 General Python File Layout](#2-general-python-file-layout)
  - [2.1 Shebang Line](#21-shebang-line)
  - [2.2 Future Imports](#22-future-imports)
  - [2.3 Header Section](#23-header-section)
  - [2.4 Imports](#24-imports)
  - [2.5 Definitions Section](#25-definitions-section)
    - [2.5.1 Constants](#251-constants)
    - [2.5.2 Functions](#252-functions)
    - [2.5.3 Classes](#253-classes)
      - [2.5.3.1 Static Methods](#2531-static-methods)
      - [2.5.3.2 Class Attributes](#2532-class-attributes)
      - [2.5.3.3 Class Magic Methods](#2533-class-magic-methods)
      - [2.5.3.4 Class Methods](#2534-class-methods)
      - [2.5.3.5 Attributes](#2535-attributes)
      - [2.5.3.6 Properties](#2536-properties)
      - [2.5.3.7 Magic Methods](#2537-magic-methods)
        - [2.5.3.7.1 Class Magic Method Subcategories](#25371-magic-method-subcategories)
      - [2.5.3.8 Instance Methods](#2538-instance-methods)
        - [2.5.3.8.1 Instance Method Subcategories](#25381-instance-method-subcategories)
      - [2.5.3.9 Getters and Setters](#2539-getters-and-setters)
      - [2.5.3.10 Additional Definitions](#25310-additional-definitions)
  - [2.6 Main](#26-main)
- [3 \_\_init__.py File Layout](#3-\_\_init__py-file-layout)


## 1 Background

This document provides comprehensive guidelines for organizing Python code in a file. It details the standard structure 
and layout that all Python files should follow, including the ordering of sections like shebang lines, module 
docstrings, imports, and definitions. The guidelines cover how to organize constants, functions, and classes, with 
special attention to class structure and the organization of methods within classes. Following these guidelines ensures 
consistency across the codebase, making it easier to navigate, understand, and maintain the project's source code.


## 2 General Python File Layout
Each Python file, except for internal files, must follow this structure:

1. Shebang Line (If applicable)
2. Module Docstring
3. Future Imports
4. Header Section
5. Imports Section 
6. Definitions section with constants, functions, classes, etc.
7. Main Section

Finally, there is always a blank line at the end of the file.


### 2.1 Shebang Line
Most .py files do not need to start with a `#!` line. Start the main file of a program with `#!/usr/bin/env python3` (to 
support virtualenvs) or `#!/usr/bin/python3` per PEP-394.

This line is used by the kernel to find the Python interpreter, but is ignored by Python when importing modules. It is 
only necessary on a file intended to be executed directly.


### 2.2 Future Imports
New language version semantic changes may be gated behind a special future import to enable them on a per-file basis 
within earlier runtimes.

Use of `from __future__ import` statements is encouraged. It allows a given source file to start using more modern 
Python syntax features today. Once you no longer need to run on a version where the features are hidden behind a 
`__future__` import, feel free to remove those lines.

In code that may execute on versions as old as 3.5 rather than >= 3.7, import:

```python
from __future__ import generator_stop
```

For more information read the Python future statement definitions documentation.

Please don't remove these imports until you are confident the code is only ever used in a sufficiently modern 
environment. Even if you do not currently use the feature a specific future import enables in your code today, keeping 
it in place in the file prevents later modifications of the code from inadvertently depending on the older behavior.

Use other `from __future__ import` statements as you see fit.


### 2.3 Header Section
The header section contains metadata about the file and the package. This section must be included in all Python files.

Guidelines:
- The Header section must have the header comment: `# Header #`
- The Header section must include the package name as `__package_name__`
- The Header section must include author information as `__author__`
- The Header section must include credits as `__credits__`
  - Credits must be a list of strings or the contributors' names.
- The Header section must include copyright information as `__copyright__`
- The Header section must include license information as `__license__`
- The Header section must include version information as `__version__`

Example:
```python
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"
```


### 2.4 Imports
In general, python files must be short, so the imported items must be easily trackable. Also, with trackback tools, 
it is straightforward to find which definition is used.

Guidelines:
- Imports are always put at the top of the file, just after any module comments and docstrings and before module globals and constants.
- The Imports section must have the header comment: `# Imports #`
- Import must be grouped, in order, by standard library, third party, and project modules.
  - The standard library import group must have the header comment: `# Standard Libraries #`
  - The third party import group must have the header comment: `# Third Party Libraries #`
  - The project import group must have the header comment: `# Project Libraries #`
- There must be one blank line between each import group.
- Within each grouping, imports must be sorted lexicographically, ignoring case, according to each module's full package path
- Imports must be grouped from most generic to least generic.
- Package and module imports must be on separate lines.
- Preferably,`from x import y` must be used individual types, classes, or functions. 
- Avoid wildcard imports (`from module import *`). Except when a module's `__init__.py` is importing all items from a sub-module.
- For conflicts, import the parent module/package then call the item from that module/package.
- For some conflicts, if a normally lower case class name conflicts, it can be imported as a camel case variant. (e.g., `from datetime import tzinfo as TZInfo`)
- Use `from x import y as z` in any of the following circumstances:
  - Two modules named y are to be imported.
  - y conflicts with a top-level name defined in the current module.
  - y conflicts with a common parameter name that is part of the public API (e.g., features).
  - y is an inconveniently long name.
  - y is too generic in the context of your code (e.g., from storage.file_system import options as fs_options).
- Use `import y as z` only when z is a standard abbreviation (e.g., `import numpy as np`).

Exemptions:
- Symbols from the following modules are used to support static analysis and type checking:
  - typing module
  - collections.abc module
  - typing_extensions module
- Redirects from the six.moves module.

Examples:

Correct:
```python
# Imports #
# Standard Libraries #
from collections.abc import Mapping, Sequence
import os
import sys
from typing import Any, List, Optional, NewType

# Third-Party Packages #
import numpy as np
import pandas as pd

# Local Packages #
from ..bases import BaseObject
from .utils import helper_function
```

Incorrect:
```python
import os, sys
```


### 2.5 Definitions Section
The definitions section is a section of code that defines constants, functions, classes, etc. If there are no 
definitions, the section may be omitted.

The definitions section must have the header comment: `# Definitions #`

Definitions should be organized into the following subsections with the recommended order:
1. Constants
2. Functions
3. Classes
4. Additional Definitions

However, the definition subsections may be organized in any order that makes sense for the code and may be omitted if 
there are no definitions in that section. 

#### 2.5.1 Constants
Constants are values that must not be changed during program execution. They are typically defined at the module level.

Guidelines:
- The Constants section must have the header comment: `# Constants #`
- Constants must be named using ALL_CAPS_WITH_UNDERSCORES
- Constants must be placed before function and class definitions
- Constants must have a clear, descriptive name that indicates their purpose
- Complex constants must have a comment explaining their purpose or derivation

Example:
```python
# Constants #
EXCEL_INIT_DATE = datetime(1899, 12, 30)  # The initial date of Excel's date system
```

#### 2.5.2 Functions
Functions are reusable blocks of code that perform specific tasks. They must be defined at the module level.

Guidelines:
- Functions must be placed after constants and before class definitions
- The Functions section must have the header comment: `# Functions #`
- Each function must have a descriptive docstring that explains its purpose, parameters, and return values (See Syntactic Guidelines)
- Function names must use snake_case (lowercase with underscores)
- Function parameters must have type hints
- Function return values must have type hints
- Functions must be organized by functionality
- Related functions must be grouped together
- Decorator functions must be placed before the functions they decorate

Example:
```python
# Functions #
@singledispatch
def excel_date_to_datetime(timestamp: int | float | str | bytes, tzinfo: tzinfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")
```

#### 2.5.3 Classes
Classes are blueprints for creating objects that encapsulate data and behavior. They must be defined at the module level.

Guidelines:
- Classes must be placed after constants and functions
- The Classes section must have the header comment: `# Classes #`
- Class names must use CamelCase (capitalize first letter of each word)
- Each class must have a descriptive docstring that explains its purpose (See Syntactic Guidelines)
- Classes must follow a consistent internal organization (see subsections below)
- Related classes must be grouped together
- Base classes must be defined before derived classes

Example:
```python
# Classes #
class BaseObject(ABC):
    """An abstract class that implements some basic functions that all objects must have."""

    # Class structure follows...
```

Classes must follow a consistent internal organization with the following sections:
1. Docstring
2. Static Methods
3. Class Attributes
4. Class Magic Methods
5. Class Methods
6. Attributes
7. Properties
8. Magic Methods
9. Instance Methods

However, the only required section is the docstring. All other sections may be omitted if they are not needed.

The docstring standards and best practices are described in the Syntactic Guidelines document.

##### 2.5.3.1 Static Methods
Static methods are methods that don't operate on instance data and don't require an instance of the class to be called.

Guidelines:
- Must be defined at the beginning of the class, before class attributes
- Must be grouped under a comment: `# Static Methods #`
- Must be decorated with `@staticmethod`
- Names must use snake_case (lowercase with underscores)
- Must have a descriptive docstring that explains their purpose, parameters, and return values
- Must have type hints for parameters and return values

Example:
```python
# Static Methods #
@staticmethod
def create_from_data(data: dict) -> "MyClass":
    """Creates a new instance from a data dictionary.

    Args:
        data: Dictionary containing initialization data.

    Returns:
        A new instance of MyClass.
    """
    return MyClass(**data)
```

##### 2.5.3.2 Class Attributes
Class attributes are variables that are shared by all instances of a class. They are defined at the class level.

Guidelines:
- Must be defined after static methods and before class magic methods
- Must be grouped under a comment: `# Class Attributes #`
- Must use snake_case (lowercase with underscores)
- Must have type hints
- Must bee type hinted with `ClassVar` (This what distinguishes class attributes from instance attributes)
- Private class attributes must be prefixed with an underscore
- Must be organized by related functionality

Example:
```python
# Class Attributes #
method_type: ClassVar[type[DynamicMethod]] = singlekwargdispatchmethod
_bind_method: ClassVar[str] = "bind_method_dispatcher"

_kwarg: ClassVar[str | None] = None
_parse_method: ClassVar[str] = "parse_first"
```

##### 2.5.3.3 Class Magic Methods
Class magic methods are special methods that are invoked by Python's syntax rather than by explicit method calls. They 
are defined at the class level and operate on the class itself rather than instances.

Guidelines:
- Must be defined after class attributes and before class methods
- Must be grouped under a comment: `# Class Magic Methods #`
- Must be prefixed and suffixed with double underscores (e.g., `__new__`)
- Must have descriptive docstrings that explain their purpose, parameters, and return values
- Must have type hints for parameters and return values
- Must be organized by functionality (e.g., Construction/Destruction)

Example:
```python
# Class Magic Methods #
def __new__(cls, *args: Any, **kwargs: Any) -> Any:
    """Creates a new instance of the class.

    Args:
        *args: Arguments for initialization.
        **kwargs: Keyword arguments for initialization.

    Returns:
        A new instance of the class.
    """
    return super().__new__(cls)
```

##### 2.5.3.4 Class Methods
Class methods are methods that operate on the class itself rather than instances. They receive the class as their first argument (conventionally named `cls`).

Guidelines:
- Must be defined after class magic methods and before instance attributes
- Must be grouped under a comment: `# Class Methods #`
- Must be decorated with `@classmethod`
- Names must use snake_case (lowercase with underscores)
- Must have descriptive docstrings that explain their purpose, parameters, and return values
- Must have type hints for parameters and return values
- Must be organized by functionality

Example:
```python
# Class Methods #
@classmethod
def from_dict(cls, data: dict) -> "MyClass":
    """Creates a new instance from a dictionary.

    Args:
        data: Dictionary containing initialization data.

    Returns:
        A new instance of the class.
    """
    return cls(**data)
```

##### 2.5.3.5 Attributes
Instance attributes are variables that are specific to each instance of a class. They are typically defined in class 
scope and can be initialized in the `__init__` or `construct` methods.

Guidelines:
- Must be defined after class methods and before properties
- Must be grouped under a comment: `# Attributes #` in the class definition scope (They are defined outside of `__init__`)
- All instance attributes must be defined in this section at the class definition scope
- Must use snake_case (lowercase with underscores)
- Private/Protected instance attributes must be prefixed with an underscore
- Must have type hints
- Must NOT be type hinted with `ClassVar` (This what distinguishes instance attributes from class attributes)
- Must be documented in the class docstring (Check Dostrings in Syntactic Guidelines for more information)
- Should be organized by related functionality
- Can be initialized in the `__init__` method but not necessary

Example:
```python
# Attributes #
parse: MethodMultiplexer
dispatcher: AnyCallable | None = None
_initialized: bool

def __init__(self, *args: Any, **kwargs: Any) -> None:
    # Attributes #
    self.parse: MethodMultiplexer = MethodMultiplexer(instance=self, select=self._parse_method)
    self._initialized: bool = False

    # Parent Initialization #
    super().__init__(*args, **kwargs)
```

##### 2.5.3.6 Properties
Properties may be used to control getting or setting attributes that require trivial computations or logic. Property 
implementations must match the general expectations of regular attribute access: that they are cheap, straightforward, 
and unsurprising.

Properties are allowed, but, like operator overloading, must only be used when necessary and match the expectations of 
typical attribute access; follow the getters and setters rules otherwise.

For example, using a property to simply both get and set an internal attribute isn't allowed: there is no computation 
occurring, so the property is unnecessary (make the attribute public instead). In comparison, using a property to 
control attribute access or to calculate a trivially derived value is allowed: the logic is simple and unsurprising.

Properties must be created with the `@property` decorator. Manually implementing a property descriptor is considered 
a power feature.

Inheritance with properties can be non-obvious. Do not use properties to implement computations a subclass may ever want 
to override and extend.

##### 2.5.3.7 Magic Methods
Magic methods (also known as dunder methods) are special methods that are invoked by Python's syntax rather than by explicit method calls. They are defined at the instance level.

Guidelines:
- Must be defined after properties and before instance methods
- Must be grouped under a comment: `# Magic Methods #`
- Must be prefixed and suffixed with double underscores (e.g., `__str__`)
- Must have descriptive docstrings that explain their purpose, parameters, and return values (see Syntactic Guidelines)
- Must have type hints for parameters and return values
- Must be organized by functionality (e.g., Construction/Destruction, Comparison, etc.)

Example:
```python
# Magic Methods #
# Construction/Destruction
def __init__(self, *args: Any, **kwargs: Any) -> None:
    """Initialize the object.

    Args:
        *args: Arguments for initialization.
        **kwargs: Keyword arguments for initialization.
    """
    super().__init__(*args, **kwargs)

def __copy__(self) -> Any:
    """The copy magic method (shallow).

    Returns:
        A shallow copy of this object.
    """
    return self.copy()
```

###### 2.5.3.7.1 Magic Method Subcategories
Magic methods should be organized into subcategories based on their functionality. This helps improve code readability 
and organization. Each subcategory should be preceded by a comment indicating the subcategory name.

Common magic method subcategories include:

- **Construction/Destruction**: Methods related to object creation and cleanup
  - `__new__`, `__init__`, `__del__`, `__copy__`, `__deepcopy__`

- **Container Methods**: Methods that implement container-like behavior
  - `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__contains__`

- **Representation**: Methods that provide string representations of the object
  - `__repr__`, `__str__`, `__format__`

- **Type Conversion**: Methods that handle type conversion
  - `__bool__`, `__int__`, `__float__`, `__complex__`, `__bytes__`

- **Comparison**: Methods that implement comparison operations
  - `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`

- **Arithmetic**: Methods that implement arithmetic operations
  - `__add__`, `__sub__`, `__mul__`, `__matmul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__pow__`
  - `__radd__`, `__rsub__`, `__rmul__`, `__rmatmul__`, `__rtruediv__`, `__rfloordiv__`, `__rmod__`, `__rpow__`
  - `__iadd__`, `__isub__`, `__imul__`, `__imatmul__`, `__itruediv__`, `__ifloordiv__`, `__imod__`, `__ipow__`

- **Attribute Access**: Methods that control attribute access
  - `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__dir__`

- **Descriptor Protocol**: Methods that implement the descriptor protocol
  - `__get__`, `__set__`, `__delete__`

- **Context Management**: Methods that implement the context manager protocol
  - `__enter__`, `__exit__`

Example:
```python
# Magic Methods #
# Construction/Destruction
def __init__(self, *args: Any, **kwargs: Any) -> None:
    """Initialize the object."""
    pass

def __copy__(self) -> "MyClass":
    """Create a shallow copy of this object."""
    return MyClass(self.data)

# Container Methods
def __len__(self) -> int:
    """Return the number of items in this container."""
    return len(self.data)

def __getitem__(self, key: Any) -> Any:
    """Get an item by key."""
    return self.data[key]

# Representation
def __repr__(self) -> str:
    """Return a string representation of this object."""
    return f"{self.__class__.__name__}({self.data!r})"

# Comparison
def __eq__(self, other: Any) -> bool:
    """Check if this object is equal to another object."""
    if not isinstance(other, self.__class__):
        return NotImplemented
    return self.data == other.data
```

##### 2.5.3.8 Instance Methods
Instance methods are methods that operate on instance data and require an instance of the class to be called. They 
receive the instance as their first argument (conventionally named `self`).

Guidelines:
- Must be defined after magic methods and before getters and setters
- Must be grouped under a comment: `# Instance Methods #`
- Names must use snake_case (lowercase with underscores)
- Must have descriptive docstrings that explain their purpose, parameters, and return values (see Syntactic Guidelines)
- Must have type hints for parameters and return values
- Must be organized by functionality (e.g., Constructors/Destructors, Setters, Parsers, etc.)
- Related methods must be grouped together with subcategory comments

Example:
```python
# Instance Methods #
# Constructors
def construct(self, *args: Any, **kwargs: Any) -> None:
    """Constructs this object.

    Args:
        *args: Arguments for inheritance.
        **kwargs: Keyword arguments for inheritance.
    """
    pass

# Setters
def set_kwarg(self, kwarg: str | None) -> None:
    """Sets the name of the kwarg for dispatching.

    Args:
        kwarg: The name of the kwarg or None for checking the first kwarg.
    """
    self._kwarg = kwarg
```

###### 2.5.3.8.1 Instance Method Subcategories
Instance methods should be organized into subcategories based on their functionality. This helps improve code 
readability and organization. Each subcategory should be preceded by a comment indicating the subcategory name.

Common instance method subcategories include:

- **Constructors/Destructors**: Methods related to object construction and cleanup
  - `construct`, `initialize`, `setup`, `cleanup`, `dispose`

- **Setters**: Methods that set object attributes or state
  - `set_*`, `update_*`, `configure_*`

- **Getters**: Methods that retrieve object attributes or state
  - `get_*`, `retrieve_*`, `find_*`

- **Parameter Parsers**: Methods that parse or validate input parameters
  - `parse_*`, `validate_*`, `check_*`

- **Binding**: Methods related to binding functions or methods
  - `bind_*`, `unbind_*`, `rebind_*`

- **Method Dispatching**: Methods that handle method dispatching or routing
  - `dispatch_*`, `route_*`, `handle_*`

- **Conversion**: Methods that convert between different formats or types
  - `to_*`, `from_*`, `as_*`, `convert_*`

- **Validation**: Methods that validate object state or data
  - `validate_*`, `is_valid_*`, `check_*`

- **Utility**: Helper methods that provide common functionality
  - `utility_*`, `helper_*`, `format_*`

- **Operations**: Methods that perform specific operations on the object
  - `calculate_*`, `compute_*`, `process_*`

Example:
```python
# Instance Methods #
# Constructors
def construct(self, *args: Any, **kwargs: Any) -> None:
    """Construct this object with the given arguments."""
    self.data = {}
    self.initialize(*args, **kwargs)

def initialize(self, data: dict | None = None) -> None:
    """Initialize this object with the given data."""
    if data:
        self.data.update(data)

# Parameter Parsers
def parse_input(self, input_data: Any) -> dict:
    """Parse the input data into a dictionary format."""
    if isinstance(input_data, dict):
        return input_data
    elif isinstance(input_data, str):
        return {"text": input_data}
    else:
        return {"value": input_data}

# Setters
def set_option(self, name: str, value: Any) -> None:
    """Set an option with the given name and value."""
    self.data[name] = value

# Method Dispatching
def dispatch_call(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
    """Dispatch a call to the method with the given name."""
    method = getattr(self, method_name, None)
    if method is None:
        raise AttributeError(f"No method named {method_name}")
    return method(*args, **kwargs)
```

##### 2.5.3.9 Getters and Setters
Getter and setter methods (also called accessors and mutators) are a type of method which must be used when they 
provide a meaningful role or behavior for getting or setting a variable's value.

In particular, they must be used when getting or setting the variable is complex or the cost is significant, either 
currently or in a reasonable future.

If, for example, a pair of getters/setters simply read and write an internal attribute, the internal attribute must be 
made public instead. By comparison, if setting a variable means some state is invalidated or rebuilt, it must be a 
setter function. The function invocation hints that a potentially non-trivial operation is occurring. Alternatively, 
properties may be an option when simple logic is needed, or refactoring to no longer need getters and setters.

Getters and setters must follow the Naming guidelines, such as `get_foo()` and `set_foo()`.

If the past behavior allowed access through a property, do not bind the new getter/setter functions to the property. Any 
code still attempting to access the variable by the old method must break visibly, so they are made aware of the 
change in complexity.

##### 2.5.3.10 Additional Definitions
In some cases, there is other code that is not part of the class, function, or module structure. Those can be defined 
at the end of the definitions section.

For example, a class may have a circular reference. In that case, the reference may be defined in a definition section 
called: `# Circular References #`. 

Alternatively, a class or function may need to be registered to an object which is not defined in the same file. In 
that case, the registration may be defined in a definitions section called: `# Registration #`.


### 2.6 Main
In Python, pydoc as well as unit tests require modules to be importable. If a file is meant to be used as an executable, 
its main functionality must be in a `main()` function, and your code must always check if `__name__ == '__main__'` 
before executing your main program, so that it is not executed when the module is imported.

When using absl, use app.run:

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

Otherwise, use:

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

All code at the top level will be executed when the module is imported. Be careful not to call functions, create 
objects, or perform other operations that must not be executed when the file is being pydoced.


## 3 \_\_init__.py File Layout
The `__init__.py` file is a special file in Python that marks a directory as a Python package. It can be empty or 
contain code to initialize the package.

Guidelines:
- Must follow the same general structure as other Python files
- Must include a module docstring that describes the package
- Must include the Header section with package metadata
- Must import and expose the public API of the package
- Can use wildcard imports (`from .submodule import *`) to expose all public members from submodules
- Must be kept simple and focused on package initialization
- Must not contain implementation details
- Can contain logic to handle package imports (i.e., try catch import block)

Example:
```python
"""__init__.py
baseobjects provides several base classes and tools.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .bases import *
from .functions import *
from .composition import *

```
