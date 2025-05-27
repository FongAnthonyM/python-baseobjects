# Anthony's Python Style Guide: Semantics Guidelines (Google Style Guide Remix)

## Table of Contents

- [1 Background](#1-background)
- [2 Semantic Guidelines](#2-semantic-guidelines)
  - [2.1 Mutable Global State](#21-mutable-global-state)
    - [2.1.1 Definition](#211-definition)
    - [2.1.2 Pros](#212-pros)
    - [2.1.3 Cons](#213-cons)
    - [2.1.4 Decision](#214-decision)
  - [2.2 Function length](#22-function-length)
  - [2.3 Nested/Local/Inner Classes and Functions](#23-nestedlocalinner-classes-and-functions)
    - [2.3.1 Definition](#231-definition)
    - [2.3.2 Pros](#232-pros)
    - [2.3.3 Cons](#233-cons)
    - [2.3.4 Decision](#234-decision)
  - [2.4 Lexical Scoping](#24-lexical-scoping)
    - [2.4.1 Definition](#241-definition)
    - [2.4.2 Pros](#242-pros)
    - [2.4.3 Cons](#243-cons)
    - [2.4.4 Decision](#244-decision)
  - [2.5 Threading](#25-threading)


## 1 Background

This document provides guidelines for the semantic aspects of Python code in the baseobjects project, based on Google's 
Python Style Guide with customizations [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
It is mostly copy-pasted from there but has some edits. This document addresses programming practices that affect code 
behavior and maintainability, including the use of mutable global state, function length, nested classes and functions, 
lexical scoping, and threading considerations. These guidelines help developers write code that is semantically sound, 
leading to more robust, maintainable, and bug-free applications.


## 2 Semantic Guidelines
### 2.1 Mutable Global State
Avoid mutable global state.

#### 2.1.1 Definition
Module-level values or class attributes that can get mutated during program execution.

#### 2.1.2 Pros
Occasionally useful.

#### 2.1.3 Cons
Breaks encapsulation: Such design can make it hard to achieve valid objectives. For example, if global state is used to 
manage a database connection, then connecting to two different databases at the same time (such as for computing 
differences during a migration) becomes difficult. Similar problems easily arise with global registries.

Has the potential to change module behavior during the import, because assignments to global variables are done when the
module is first imported.

#### 2.1.4 Decision
Avoid mutable global state.

In those rare cases where using global state is warranted, mutable global entities should be declared at the module 
level or as a class attribute and made internal by prepending an `_` to the name. If necessary, external access to 
mutable global state must be done through public functions or class methods. See Naming below. Please explain the design 
reasons why mutable global state is being used in a comment or a doc linked to from a comment.

Module-level constants are permitted and encouraged. For example: `_MAX_HOLY_HANDGRENADE_COUNT = 3` for an internal use 
constant or `SIR_LANCELOTS_FAVORITE_COLOR = "blue"` for a public API constant. Constants must be named using all caps 
with underscores. See Naming below.


### 2.2 Function length
Prefer small and focused functions.

We recognize that long functions are sometimes appropriate, so no hard limit is placed on function length. If a function 
exceeds about 40 lines, think about whether it can be broken up without harming the structure of the program.

Even if your long function works perfectly now, someone modifying it in a few months may add new behavior. This could 
result in bugs that are hard to find. Keeping your functions short and simple makes it easier for other people to read 
and modify your code.

You could find long and complicated functions when working with some code. Do not be intimidated by modifying existing 
code: if working with such a function proves to be difficult, you find that errors are hard to debug, or you want to 
use a piece of it in several different contexts, consider breaking up the function into smaller and more manageable 
pieces.


### 2.3 Nested/Local/Inner Classes and Functions
Nested local functions or classes are fine when used to close over a local variable. Inner classes are fine.

#### 2.3.1 Definition
A class can be defined inside of a method, function, or class. A function can be defined inside a method or function. 
Nested functions have read-only access to variables defined in enclosing scopes.

#### 2.3.2 Pros
Allows definition of utility classes and functions that are only used inside of a very limited scope. Commonly used for 
implementing decorators.

#### 2.3.3 Cons
Nested functions and classes cannot be directly tested. Nesting can make the outer function longer and less readable.

#### 2.3.4 Decision
They are fine with some caveats. Avoid nested functions or classes except when closing over a local value other than 
`self` or `cls`. Do not nest a function just to hide it from users of a module. Instead, prefix its name with an `_` at 
the module level so that it can still be accessed by tests.


### 2.4 Lexical Scoping
Okay to use.

#### 2.4.1 Definition
A nested Python function can refer to variables defined in enclosing functions, but cannot assign to them. Variable 
bindings are resolved using lexical scoping, that is, based on the static program text. Any assignment to a name in a 
block will cause Python to treat all references to that name as a local variable, even if the use precedes the 
assignment. If a global declaration occurs, the name is treated as a global variable.

Example:
```python
def get_adder(summand1: float) -> Callable[[float], float]:
    """Returns a function that adds numbers to a given number."""
    def adder(summand2: float) -> float:
        return summand1 + summand2

    return adder
```
#### 2.4.2 Pros
Often results in clearer, more elegant code. Especially comforting to experienced Lisp and Scheme (and Haskell and ML 
and …) programmers.

#### 2.4.3 Cons
Can lead to confusing bugs, such as this example based on PEP-0227:
```python
i = 4
def foo(x: Iterable[int]):
    def bar():
        print(i, end='')
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to foo, so this is what bar sees
        print(i, end='')
    bar()
```
So `foo([1, 2, 3])` will print `1 2 3 3`, not `1 2 3 4`.

#### 2.4.4 Decision
Okay to use.


### 2.5 Threading
Do not rely on the atomicity of built-in types.

While Python's built-in data types such as dictionaries appear to have atomic operations, there are corner cases where 
they aren't atomic (e.g. if `__hash__` or `__eq__` are implemented as Python methods) and their atomicity should not be 
relied upon. Neither should you rely on atomic variable assignment (since this in turn depends on dictionaries).

Use the queue module's Queue data type as the preferred way to communicate data between threads. Otherwise, use the 
threading module and its locking primitives. Prefer condition variables and `threading.Condition` instead of using 
lower-level locks.
