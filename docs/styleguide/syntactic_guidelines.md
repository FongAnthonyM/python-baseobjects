# Anthony's Python Style Guide: Syntactic Guidelines (Google Style Guide Remix)

## Table of Contents

- [1 Background](#1-background)
- [2 Syntactic Guidelines](#2-syntactic-guidelines)
  - [2.1 Naming](#21-naming)
    - [2.1.1 Names to Avoid](#211-names-to-avoid)
    - [2.1.2 Naming Conventions](#212-naming-conventions)
    - [2.1.3 File Naming](#213-file-naming)
  - [2.2 Semicolons](#22-semicolons)
  - [2.3 Line length](#23-line-length)
  - [2.4 Statements](#24-statements)
  - [2.5 Parentheses](#25-parentheses)
  - [2.6 Indentation](#26-indentation)
    - [2.6.1 Trailing Commas in Sequences of Items](#261-trailing-commas-in-sequences-of-items)
  - [2.7 Blank Lines](#27-blank-lines)
  - [2.8 Whitespace](#28-whitespace)
  - [2.9 Type Annotations](#29-type-annotations)
    - [2.9.1 General Rules](#291-general-rules)
    - [2.9.2 Line Breaking](#292-line-breaking)
    - [2.9.3 Forward Declarations](#293-forward-declarations)
    - [2.9.4 Default Values](#294-default-values)
    - [2.9.5 NoneType](#295-nonetype)
    - [2.9.6 Type Aliases](#296-type-aliases)
    - [2.9.7 Ignoring Types](#297-ignoring-types)
    - [2.9.8 Typing Variables](#298-typing-variables)
    - [2.9.9 Tuples vs Lists](#299-tuples-vs-lists)
    - [2.9.10 Type variables](#2910-type-variables)
    - [2.9.11 String types](#2911-string-types)
    - [2.9.12 Imports For Typing](#2912-imports-for-typing)
    - [2.9.13 Conditional Imports](#2913-conditional-imports)
    - [2.9.14 Circular Dependencies](#2914-circular-dependencies)
    - [2.9.15 Generics](#2915-generics)
  - [2.10 Docstrings](#210-docstrings)
    - [2.10.1 Modules](#2101-modules)
      - [2.10.1.1 Test modules](#21011-test-modules)
    - [2.10.2 Functions and Methods](#2102-functions-and-methods)
      - [2.10.2.1 Overridden Methods](#21021-overridden-methods)
    - [2.10.3 Classes](#2103-classes)
  - [2.11 Comments](#211-comments)
    - [2.11.1 Block and Inline](#2111-block-and-inline)
    - [2.11.2 TODO Comments](#2112-todo-comments)
  - [2.12 Punctuation, Spelling, and Grammar](#212-punctuation-spelling-and-grammar)
  - [2.13 Mathematical Notation](#213-mathematical-notation)
  - [2.14 Strings](#214-strings)
    - [2.14.1 Logging](#2141-logging)
    - [2.14.2 Error Messages](#2142-error-messages)
  - [2.15 Exceptions](#215-exceptions)
  - [2.16 Comprehensions & Generator Expressions](#216-comprehensions--generator-expressions)
    - [2.16.1 Definition](#2161-definition)
    - [2.16.2 Pros](#2162-pros)
    - [2.16.3 Cons](#2163-cons)
    - [2.16.4 Decision](#2164-decision)
  - [2.17 Default Iterators and Operators](#217-default-iterators-and-operators)
  - [2.18 Generators](#218-generators)
  - [2.19 Lambda Functions](#219-lambda-functions)
    - [2.19.1 Definition](#2191-definition)
    - [2.19.2 Pros](#2192-pros)
    - [2.19.3 Cons](#2193-cons)
    - [2.19.4 Decision](#2194-decision)
  - [2.20 Conditional Expressions](#220-conditional-expressions)
    - [2.20.1 Definition](#2201-definition)
    - [2.20.2 Pros](#2202-pros)
    - [2.20.3 Cons](#2203-cons)
    - [2.20.4 Decision](#2204-decision)
  - [2.21 True/False Evaluations](#221-truefalse-evaluations)
    - [2.21.1 Definition](#2211-definition)
    - [2.21.2 Pros](#2212-pros)
    - [2.21.3 Cons](#2213-cons)
    - [2.21.4 Decision](#2214-decision)
  - [2.22 Files, Sockets, and similar Stateful Resources](#222-files-sockets-and-similar-stateful-resources)
  - [2.23 Function and Method Decorators](#223-function-and-method-decorators)
    - [2.23.1 Definition](#2231-definition)
    - [2.23.2 Pros](#2232-pros)
    - [2.23.3 Cons](#2233-cons)
    - [2.23.4 Decision](#2234-decision)
  - [2.24 Default Argument Values](#224-default-argument-values)
    - [2.24.1 Definition](#2241-definition)
    - [2.24.2 Pros](#2242-pros)
    - [2.24.3 Cons](#2243-cons)
    - [2.24.4 Decision](#2244-decision)



## 1 Background

This document provides comprehensive syntactic guidelines for Python code, based on Google's 
Python Style Guide with customizations [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
It is mostly copy-pasted from there but has some edits. This document covers naming conventions, code formatting, 
indentation, whitespace usage, type annotations, docstrings, comments, and best practices for various Python language 
features. These guidelines ensure code consistency, readability, and maintainability across the project, making it 
easier for developers to understand and contribute to the codebase.


## 2 Syntactic Guidelines
### 2.1 Naming
Names should be descriptive. This includes functions, classes, variables, attributes, files and any other type of named 
entities.

Avoid abbreviation. In particular, do not use abbreviations that are ambiguous or unfamiliar to readers outside your 
project, and do not abbreviate by deleting letters within a word.

Always use a .py filename extension. Never use dashes.

Examples:

`module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`, `function_name`, `GLOBAL_CONSTANT_NAME`, 
`global_var_name`, `instance_var_name`, `function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`, 
`send_acronym_via_https`.

#### 2.1.1 Names to Avoid
- dashes (-) in any package/module name
- names that needlessly include the type of the variable (for example: id_to_name_dict)
- single character names, except for specifically allowed cases:
  - counters or iterators (e.g. i, j, k, v, et al.)
  - e as an exception identifier in try/except statements.
  - f as a file handle in with statements
  - private type variables with no constraints (e.g. _T = TypeVar("_T"), _P = ParamSpec("_P"))
  - names that match established notation in a reference paper or algorithm (see Mathematical Notation)

Please be mindful not to abuse single-character naming. Generally speaking, descriptiveness should be proportional to 
the name's scope of visibility. For example, i might be a fine name for 5-line code block but within multiple nested 
scopes, it is likely too vague.

#### 2.1.2 Naming Conventions
"Internal" means internal to a module, or protected or private within a class.

Prepending a single underscore (`_`) has some support for protecting module variables and functions (linters will flag 
protected member access). Note that it is okay for unit tests to access protected constants from the modules under test.

Prepending a double underscore (`__` aka "dunder") to an instance variable or method effectively makes the variable or 
method private to its class (using name mangling); we discourage its use as it impacts readability and testability, and 
isn't really private. Prefer a single underscore.

Place related classes and top-level functions together in a module.

- **Packages**: Lowercase, no underscores.
- **Modules**: Lowercase, with underscores.
- **Classes**: CapWords/PascalCase.
- **Exceptions**: CapWords/PascalCase.
- **Functions**: lowercase, with underscores.
- **Global/Class Constants**: ALL_CAPS.
- **Global/Class Variables**: lowercase, with underscores.
- **Methods**: lowercase, with underscores.
- **Function/Method Parameters**: lowercase, with underscores.
- **Local Variables**: lowercase, with underscores.

Examples:

| Type | Public | Internal/Protected    |
| ---- | ------ |-----------------------|
| Packages | `lower_with_under` |                       |
| Modules | `lower_with_under` | `_lower_with_under`   |
| Classes | `CapWords` | `_CapWords`           |
| Exceptions | `CapWords` |                       |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER`    |
| Global/Class Variables | `lower_with_under` | `_lower_with_under`   |
| Instance Variables | `lower_with_under` | `_lower_with_under`   |
| Method Names | `lower_with_under()` | `_lower_with_under()` |
| Function/Method Parameters | `lower_with_under` | `_lower_with_under`   |
| Local Variables | `lower_with_under` |                       |


#### 2.1.3 File Naming
Python filenames must have a .py extension and must not contain dashes (-). If you want an executable to be accessible 
without the extension, use a symbolic link or a simple bash wrapper containing `exec "$0.py" "$@"`.

Unit test files follow PEP 8 compliant lower_with_under method names, for example, test_<method_under_test>_<state>. 
For consistency(*) with legacy modules that follow CapWords function names, underscores may appear in method names 
starting with test to separate logical components of the name. One possible pattern is test<MethodUnderTest>_<state>.



### 2.2 Semicolons
Do not terminate your lines with semicolons, and do not use semicolons to put two statements on the same line.

### 2.3 Line length
Maximum line length is 120 characters.

Explicit exceptions to the 120 character limit:
- Long import statements.
- URLs, pathnames, or long flags in comments.
- Long string module-level constants not containing whitespace that would be inconvenient to split across lines such as URLs or pathnames.
- Pylint disable comments. (e.g.: `# pylint: disable=invalid-name`)

Do not use a backslash for explicit line continuation.

Instead, make use of Python's implicit line joining inside parentheses, brackets and braces. If necessary, you can add 
an extra pair of parentheses around an expression.

Note that this rule doesn't prohibit backslash-escaped newlines within strings (see below).

Examples:

Correct:
```python
foo_bar(
    self, 
    width, 
    height, 
    color='black', 
    design=None, 
    x='foo',
    emphasis=None, 
    highlight=0,
)
```
```python
if (width == 0 and height == 0 and
    color == 'red' and emphasis == 'strong'):
```
```python
(bridge_questions.clarification_on
    .average_airspeed_of.unladen_swallow) = 'African or European?'
```
```python
with (
    very_long_first_expression_function() as spam,
    very_long_second_expression_function() as beans,
    third_thing() as eggs,
):
    place_order(eggs, beans, spam, beans)
```

Incorrect:
```python
if width == 0 and height == 0 and \
    color == 'red' and emphasis == 'strong':
```
```python
bridge_questions.clarification_on \
     .average_airspeed_of.unladen_swallow = 'African or European?'
```
```python
with very_long_first_expression_function() as spam, \
     very_long_second_expression_function() as beans, \
     third_thing() as eggs:
    place_order(eggs, beans, spam, beans)
```

When a literal string won't fit on a single line, use parentheses for implicit line joining.

```python
x = ('This will build a very long long '
     'long long long long long long string')
```

Prefer to break lines at the highest possible syntactic level. If you must break a line twice, break it at the same 
syntactic level both times.

Correct:
```python
bridgekeeper.answer(
    name="Arthur", 
    quest=questlib.find(owner="Arthur", perilous=True),
)
```
```python
answer = (a_long_line().of_chained_methods()
          .that_eventually_provides().an_answer())
```
```python
if (
    config is None
    or 'editor.language' not in config
    or config['editor.language'].use_spaces is False
):
    use_tabs()
```

Incorrect:
```python
bridgekeeper.answer(name="Arthur", quest=questlib.find(
    owner="Arthur", perilous=True))
```
```python
answer = a_long_line().of_chained_methods().that_eventually_provides(
    ).an_answer()
```
```python
if (config is None or 'editor.language' not in config or config[
    'editor.language'].use_spaces is False):
  use_tabs()
```

Within comments, put long URLs on their own line if necessary.

Correct:
```python
# See details at
# http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html
```

Correct:
```python
# See details at
# http://www.example.com/us/developer/documentation/api/content/\
# v2.0/csv_file_name_extension_full_specification.html
```

Make note of the indentation of the elements in the line continuation examples above; see the indentation section for 
explanation.

Docstring summary lines must remain within the 120 character limit.

In all other cases where a line exceeds 120 characters, and the Black or Pyink auto-formatter does not help bring the 
line below the limit, the line is allowed to exceed this maximum. Authors are encouraged to manually break the line up 
per the notes above when it is sensible.


### 2.4 Statements
Generally only one statement per line.

However, you may put the result of a test on the same line as the test only if the entire statement fits on one line. In 
particular, you can never do so with try/except since the try and except can't both fit on the same line, and you can 
only do so with an if only if there is no else.

Examples:

Correct:
```python
if foo: bar(foo)
```

Incorrect:
```python
if foo: bar(foo)
else:   baz(foo)

try:               bar(foo)
except ValueError: baz(foo)

try:
    bar(foo)
except ValueError: baz(foo)
```

### 2.5 Parentheses
Use parentheses sparingly.

It is fine, though not required, to use parentheses around tuples. Do not use them in return statements or conditional 
statements unless using parentheses for implied line continuation or to indicate a tuple.

Examples:

Correct:
```python
if foo:
    bar()
while x:
    x = bar()
if x and y:
    bar()
if not x:
    bar()
# For a 1 item tuple the ()s are more visually obvious than the comma.
onesie = (foo,)
return foo
return spam, beans
return (spam, beans)
for (x, y) in dict.items(): ...
```

Incorrect:
```python
if (x):
    bar()
if not(x):
    bar()
return (foo)
```


### 2.6 Indentation
Indent your code blocks with 4 spaces.

Never use the tab character. 

Some editors will automatically use spaces when you press the tab key. Ensure that your editor is set to use 4 spaces 
for indentation. 

Implied line continuation should align wrapped elements vertically (see line length examples), or use a hanging 4-space 
indent. Closing (round, square or curly) brackets can be placed at the end of the expression, or on separate lines, but 
then should be indented the same as the line with the corresponding opening bracket.

Examples:

Correct:
```python
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
meal = (spam,
        beans)
```
```python
# Aligned with opening delimiter in a dictionary.
foo = {
    'long_dictionary_key': value1 +
                           value2,
    ...
}
```
```python
# 2-space hanging indent; nothing on first line.
foo = long_function_name(
    var_one, var_two, var_three,
    var_four)
meal = (
    spam,
    beans)
```
```python
# 2-space hanging indent; nothing on first line,
# closing parenthesis on a new line.
foo = long_function_name(
    var_one, var_two, var_three,
    var_four
)
meal = (
    spam,
    beans,
)
```
```python
# 2-space hanging indent in a dictionary.
foo = {
    'long_dictionary_key':
        long_dictionary_value,
    ...
}
```

Incorrect:
```python
# Stuff on first line forbidden.
foo = long_function_name(var_one, var_two,
    var_three, var_four)
meal = (spam,
    beans)
```
```python
# 2-space hanging indent forbidden.
foo = long_function_name(
  var_one, var_two, var_three,
  var_four)
```
```python
# No hanging indent in a dictionary.
foo = {
    'long_dictionary_key':
    long_dictionary_value,
    ...
}
```

#### 2.6.1 Trailing Commas in Sequences of Items
Trailing commas in sequences of items are required if and only if the closing container token `]`, `)`, or `}` does not 
appear on the same line as the final element, as well as for tuples with a single element. The presence of a trailing 
comma is also used as a hint to our Python code auto-formatter Black or Pyink to direct it to auto-format the container 
of items to one item per line when the `,` after the final element is present.

Correct:
```python
golomb3 = [0, 1, 3]
golomb4 = [
    0,
    1,
    4,
    6,
]
```

Incorrect:
```python
golomb4 = [
    0,
    1,
    4,
    6,]
```


### 2.7 Blank Lines
Two blank lines between top-level definitions, be they function or class definitions. One blank line between method 
definitions and between the docstring of a class and the first method. No blank line following a def line. Use single 
blank lines as you judge appropriate within functions or methods.

Blank lines need not be anchored to the definition. For example, related comments immediately preceding function, class, 
and method definitions can make sense. Consider if your comment might be more useful as part of the docstring.


### 2.8 Whitespace
Follow standard typographic rules for the use of spaces around punctuation.

No whitespace inside parentheses, brackets or braces.

Correct:
```python
spam(ham[1], {'eggs': 2}, [])
```

Incorrect:
```python
spam( ham[ 1 ], { 'eggs': 2 }, [ ] )
```

No whitespace before a comma, semicolon, or colon. Do use whitespace after a comma, semicolon, or colon, except at the 
end of the line.

Correct:
```python
if x == 4:
     print(x, y)
 x, y = y, x
```

Incorrect
```python
if x == 4 :
     print(x , y)
 x , y = y , x
```

No whitespace before the open paren/bracket that starts an argument list, indexing or slicing.

Correct:
```python
spam(1)
```

Incorrect:
```python
spam (1)
```

Correct:
```python
dict['key'] = list[index]
```

Incorrect:
```python
dict ['key'] = list [index]
```

No trailing whitespace.

Surround binary operators with a single space on either side for assignment (`=`), comparisons (`==`, `<`, `>`, `!=`, 
`<>`, `<=`, `>=`, `in`, `not in`, `is`, `is not`), and Booleans (`and`, `or`, `not`). Use your better judgment for the 
insertion of spaces around arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`).

Correct:
```python
x == 1
```

Incorrect:
```python
x<1
```

Never use spaces around `=` when passing keyword arguments or defining a default parameter value, with one exception: 
when a type annotation is present, do use spaces around the `=` for the default parameter value.

Correct:
```python
def complex(real, imag=0.0): return Magic(r=real, i=imag)
def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)
```

Incorrect:
```python
def complex(real, imag = 0.0): return Magic(r = real, i = imag)
def complex(real, imag: float=0.0): return Magic(r = real, i = imag)
```

Don't use spaces to vertically align tokens on consecutive lines, since it becomes a maintenance burden (applies to `:`, 
`#`, `=`, etc.):

Correct:
```python
foo = 1000  # comment
long_name = 2  # comment that should not be aligned

dictionary = {
    'foo': 1,
    'long_name': 2,
}
```

Incorrect:
```python
foo       = 1000  # comment
long_name = 2     # comment that should not be aligned

dictionary = {
    'foo'      : 1,
    'long_name': 2,
}
```


### 2.9 Type Annotations
Aannotate Python code with type hints. Type-check the code at build time with a type checking tool like pytype. In most 
cases, when feasible, type annotations are in source files. For third-party or extension modules, annotations can be in 
stub .pyi files.

Type annotations (or "type hints") are for function or method arguments and return values:

```python
def func(a: int) -> list[int]:
```

You can also declare the type of a variable using similar syntax:

```python
a: SomeType = some_func()
```

#### 2.9.1 General Rules
Annotating `self` or `cls` is generally not necessary. `Self` can be used if it is necessary for proper type 
information, e.g.

If any other variable or a returned type should not be expressed, use `Any`.

```python
from typing import Self

class BaseClass:
  @classmethod
  def create(cls) -> Self:
    ...

  def difference(self, other: Self) -> float:
    ...
```

#### 2.9.2 Line Breaking
Try to follow the existing indentation rules.

After annotating, many function signatures will become "one parameter per line". To ensure the return type is also given 
its own line, a comma can be placed after the last parameter.

```python
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
  ...
```

Always prefer breaking between variables, and not, for example, between variable names and type annotations. However, if 
everything fits on the same line, go for it.

```python
def my_method(self, first_var: int) -> int:
  ...
```

If the combination of the function name, the last parameter, and the return type is too long, indent by 4 in a new line. 
When using line breaks, prefer putting each parameter and the return type on their own lines and aligning the closing 
parenthesis with the def:

Correct:
```python
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
  ...
```

Optionally, the return type may be put on the same line as the last parameter:

```python
# Okay:
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
  ...
```

pylint allows you to move the closing parenthesis to a new line and align with the opening one, but this is less 
readable.

Incorrect:
```python
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
  ...
```

As in the examples above, prefer not to break types. However, sometimes they are too long to be on a single line (try to 
keep sub-types unbroken).

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
  ...
```

If a single name and type is too long, consider using an alias for the type. The last resort is to break after the colon 
and indent by 4.

Correct:
```python
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
  ...
```

Incorrect:
```python
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
  ...
```

#### 2.9.3 Forward Declarations
If you need to use a class name (from the same module) that is not yet defined – for example, if you need the class name 
inside the declaration of that class, or if you use a class that is defined later in the code – either use `from 
__future__ import annotations` or use a string for the class name.

Correct:
```python
from __future__ import annotations

class MyClass:
  def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:

class OtherClass:
  ...
```

Incorrect:
```python
class MyClass:
  def __init__(self, stack: Sequence["MyClass"], item: "OtherClass") -> None:

class OtherClass:
  ...
```

#### 2.9.4 Default Values
As per PEP-008, use spaces around the `=` only for arguments that have both a type annotation and a default value.

Correct:
```python
def func(a: int = 0) -> int:
  ...
```

Incorrect:
```python
def func(a:int=0) -> int:
  ...
```

#### 2.9.5 NoneType

In the Python type system, `NoneType` is a "first class" type, and for typing purposes, `None` is an alias for 
`NoneType`. If an argument can be `None`, it has to be declared! You can use `|` union type expressions (recommended in 
new Python 3.10+ code), or the older `Optional` and `Union` syntaxes.

Use explicit `X | None` instead of implicit. Earlier versions of type checkers allowed `a: str = None` to be interpreted 
as `a: str | None = None`, but that is no longer the preferred behavior.

Correct:
```python
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
  ...
def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
  ...
```

Incorrect:
```python
def nullable_union(a: Union[None, str]) -> str:
  ...
def implicit_optional(a: str = None) -> str:
  ...
```

#### 2.9.6 Type Aliases
You can declare aliases of complex types. The name of an alias should be CapWorded. If the alias is used only in this 
module, it should be _Private.

Note that the `: TypeAlias` annotation is only supported in versions 3.10+.

```python
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

#### 2.9.7 Ignoring Types
You can disable type checking on a line with the special comment `# type: ignore`.

pytype has a disable option for specific errors (similar to lint):

```python
# pytype: disable=attribute-error
```

#### 2.9.8 Typing Variables
**Annotated Assignments**

If an internal variable has a type that is hard or impossible to infer, specify its type with an annotated assignment - 
use a colon and type between the variable name and value (the same as is done with function arguments that have a 
default value):

```python
a: Foo = SomeUndecoratedFunction()
```

**Type Comments**

Though you may see them remaining in the codebase (they were necessary before Python 3.6), do not add any more uses of a 
`# type: <type name>` comment on the end of the line:

```python
a = SomeUndecoratedFunction()  # type: Foo
```


#### 2.9.9 Tuples vs Lists

Typed lists can only contain objects of a single type. Typed tuples can either have a single repeated type or a set 
number of elements with different types. The latter is commonly used as the return type from a function.

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```


#### 2.9.10 Type variables

The Python type system has generics. A type variable, such as `TypeVar` and `ParamSpec`, is a common way to use them.

Example:

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
_P = ParamSpec("_P")
_T = TypeVar("_T")
...
def next(l: list[_T]) -> _T:
  return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
  def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
    print("Function was called")
    return f(*args, **kwargs)
  return inner
```

A `TypeVar` can be constrained:

```python
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
  return a + b
```

A common predefined type variable in the typing module is `AnyStr`. Use it for multiple annotations that can be `bytes` 
or `str` and must all be the same type.

```python
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
  if len(x) <= 42:
    return x
  raise ValueError()
```

A type variable must have a descriptive name, unless it meets all of the following criteria:

- not externally visible
- not constrained

Correct:
```python
_T = TypeVar("_T")
_P = ParamSpec("_P")
AddableType = TypeVar("AddableType", int, float, str)
AnyFunction = TypeVar("AnyFunction", bound=Callable)
```

Incorrect:
```python
T = TypeVar("T")
P = ParamSpec("P")
_T = TypeVar("_T", int, float, str)
_F = TypeVar("_F", bound=Callable)
```


#### 2.9.11 String types

Do not use `typing.Text` in new code. It's only for Python 2/3 compatibility.

Use `str` for string/text data. For code that deals with binary data, use `bytes`.

```python
def deals_with_text_data(x: str) -> str:
  ...
def deals_with_binary_data(x: bytes) -> bytes:
  ...
```

If all the string types of a function are always the same, for example if the return type is the same as the argument 
type in the code above, use `AnyStr`.


#### 2.9.12 Imports For Typing

For symbols (including types, functions, and constants) from the typing or collections.abc modules used to support 
static analysis and type checking, always import the symbol itself. This keeps common annotations more concise and 
matches typing practices used around the world. You are explicitly allowed to import multiple specific symbols on one 
line from the typing and collections.abc modules. For example:

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```

Given that this way of importing adds items to the local namespace, names in typing or collections.abc should be treated 
similarly to keywords, and not be defined in your Python code, typed or not. If there is a collision between a type and 
an existing name in a module, import it using `import x as y`.

```python
from typing import Any as AnyType
```

When annotating function signatures, prefer abstract container types like `collections.abc.Sequence` over concrete types 
like `list`. If you need to use a concrete type (for example, a tuple of typed elements), prefer built-in types like 
`tuple` over the parametric type aliases from the typing module (e.g., `typing.Tuple`).

```python
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) ->
    List[Tuple[float, float]]:
  ...
```

```python
from collections.abc import Sequence

def transform_coordinates(original: Sequence[tuple[float, float]]) ->
    Sequence[tuple[float, float]]:
  ...
```


#### 2.9.13 Conditional Imports

Use conditional imports only in exceptional cases where the additional imports needed for type checking must be avoided 
at runtime. This pattern is discouraged; alternatives such as refactoring the code to allow top-level imports should be 
preferred.

Imports that are needed only for type annotations can be placed within an `if TYPE_CHECKING:` block.

Conditionally imported types need to be referenced as strings, to be forward compatible with Python 3.6 where the 
annotation expressions are actually evaluated.

Only entities that are used solely for typing should be defined here; this includes aliases. Otherwise it will be a 
runtime error, as the module will not be imported at runtime.

The block should be right after all the normal imports.

There should be no empty lines in the typing imports list.

Sort this list as if it were a regular imports list.

```python
import typing
if typing.TYPE_CHECKING:
  import sketch
def f(x: "sketch.Sketch"): ...
```


#### 2.9.14 Circular Dependencies

Circular dependencies that are caused by typing are code smells. Such code is a good candidate for refactoring. Although 
technically it is possible to keep circular dependencies, various build systems will not let you do so because each 
module has to depend on the other.

Replace modules that create circular dependency imports with `Any`. Set an alias with a meaningful name, and use the 
real type name from this module (any attribute of `Any` is `Any`). Alias definitions should be separated from the last 
import by one line.

```python
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: "some_mod.SomeType") -> None:
  ...
```


#### 2.9.15 Generics

When annotating, prefer to specify type parameters for generic types in a parameter list; otherwise, the generics' 
parameters will be assumed to be `Any`.

Correct:
```python
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
  ...
```

Incorrect:
```python
# This is interpreted as get_names(employee_ids: Sequence[Any]) -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
  ...
```

If the best type parameter for a generic is `Any`, make it explicit, but remember that in many cases `TypeVar` might be 
more appropriate:

Correct:
```python
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```

Incorrect:
```python
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```


### 2.10 Docstrings
Be sure to use the right style for module, function, method docstrings and inline comments.

Python uses docstrings to document code. A docstring is a string that is the first statement in a package, module, class 
or function. These strings can be extracted automatically through the `__doc__` member of the object and are used by 
pydoc. (Try running pydoc on your module to see how it looks.) Always use the three-double-quote `"""` format for 
docstrings (per PEP 257). A docstring should be organized as a summary line (one physical line not exceeding 120 
characters) terminated by a period, question mark, or exclamation point. When writing more (encouraged), this must be 
followed by a blank line, followed by the rest of the docstring starting at the same cursor position as the first quote 
of the first line. There are more formatting guidelines for docstrings below.

#### 2.10.1 Modules
Every file should contain license boilerplate. Choose the appropriate boilerplate for the license used by the project 
(for example, Apache 2.0, BSD, LGPL, GPL).

Files should start with a docstring describing the contents and usage of the module.

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an overall description of the module or program.
Optionally, it may also contain a brief description of exported classes and functions and/or usage examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

##### 2.10.1.1 Test modules
Module-level docstrings for test files are not required. They should be included only when there is additional 
information that can be provided.

Examples include some specifics on how the test should be run, an explanation of an unusual setup pattern, dependency on 
the external environment, and so on.

```python
"""This blaze test uses golden files.

You can update those files by running `blaze run //foo/bar:foo_test -- --update_golden_files` from the `google3`
directory.
"""
```

Docstrings that do not provide any new information should not be used.

```python
"""Tests for foo.bar."""
```

#### 2.10.2 Functions and Methods
In this section, "function" means a method, function, generator, or property.

A docstring is mandatory for every function that has one or more of the following properties:

- being part of the public API
- nontrivial size
- non-obvious logic

A docstring should give enough information to write a call to the function without reading the function's code. The 
docstring should describe the function's calling syntax and its semantics, but generally not its implementation details, 
unless those details are relevant to how the function is to be used. For example, a function that mutates one of its 
arguments as a side effect should note that in its docstring. Otherwise, subtle but important details of a function's 
implementation that are not relevant to the caller are better expressed as comments alongside the code than within the 
function's docstring.

The docstring may be descriptive-style (`"""Fetches rows from a Bigtable."""`). The docstring for a `@property` data 
descriptor should use the same style as the docstring for an attribute or a function argument 
(`"""The Bigtable path."""`, rather than `"""Returns the Bigtable path."""`).

Certain aspects of a function should be documented in special sections, listed below. Each section begins with a heading 
line, which ends with a colon. All sections other than the heading should maintain a hanging indent of two or four 
spaces (be consistent within a file). These sections can be omitted in cases where the function's name and signature are 
informative enough that it can be aptly described using a one-line docstring.

**Args:**
List each parameter by name. A description should follow the name, and be separated by a colon followed by either a 
space or newline. If the description is too long to fit on a single 120-character line, use a hanging indent of 2 or 4 
spaces more than the parameter name (be consistent with the rest of the docstrings in the file). The description should 
include required type(s) if the code does not contain a corresponding type annotation. If a function accepts `*foo` 
(variable length argument lists) and/or `**bar` (arbitrary keyword arguments), they should be listed as `*foo` and 
`**bar`.

**Returns:** (or **Yields:** for generators)
Describe the semantics of the return value, including any type information that the type annotation does not provide. If 
the function only returns None, this section is not required. It may also be omitted if the docstring starts with 
"Return", "Returns", "Yield", or "Yields" (e.g. `"""Returns row from Bigtable as a tuple of strings."""`) and the 
opening sentence is sufficient to describe the return value. Do not imitate older 'NumPy style' (example), which 
frequently documented a tuple return value as if it were multiple return values with individual names (never mentioning 
the tuple). Instead, describe such a return value as: "Returns: A tuple (mat_a, mat_b), where mat_a is …, and …". The 
auxiliary names in the docstring need not necessarily correspond to any internal names used in the function body (as 
those are not part of the API). If the function uses yield (is a generator), the Yields: section should document the 
object returned by next(), instead of the generator object itself that the call evaluates to.

**Raises:**
List all exceptions that are relevant to the interface followed by a description. Use a similar exception name + colon + 
space or newline and hanging indent style as described in Args:. You should not document exceptions that get raised if 
the API specified in the docstring is violated (because this would paradoxically make behavior under violation of the 
API part of the API).

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance represented by table_handle. String keys will be
    UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table row to fetch. String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be returned.

    Returns:
        A dict mapping keys to the corresponding table row data fetched. Each row is represented as a tuple of strings. 
        For example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is missing from the dictionary, then that row 
        was not found in the table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

Similarly, this variation on Args: with a line break is also allowed:

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance represented by table_handle. String keys will be
    UTF-8 encoded.

    Args:
      table_handle:
        An open smalltable.Table instance.
      keys:
        A sequence of strings representing the key of each table row to fetch. String keys will be UTF-8 encoded.
      require_all_keys:
        If True only rows with values set for all keys will be returned.

    Returns:
      A dict mapping keys to the corresponding table row data fetched. Each row is represented as a tuple of strings. 
      For example:

      {b'Serak': ('Rigel VII', 'Preparer'),
       b'Zim': ('Irk', 'Invader'),
       b'Lrrr': ('Omicron Persei 8', 'Emperor')}

      Returned keys are always bytes.  If a key from the keys argument is missing from the dictionary, then that row was
      not found in the table (and require_all_keys must have been False).

    Raises:
      IOError: An error occurred accessing the smalltable.
    """
```

##### 2.10.2.1 Overridden Methods
A method that overrides a method from a base class does not need a docstring if it is explicitly decorated with 
`@override` (from typing_extensions or typing modules), unless the overriding method's behavior materially refines the 
base method's contract, or details need to be provided (e.g., documenting additional side effects), in which case a 
docstring with at least those differences is required on the overriding method.

```python
from typing_extensions import override

class Parent:
    def do_something(self):
        """Parent method, includes docstring."""

# Child class, method annotated with override.
class Child(Parent):
    @override
    def do_something(self):
        pass

# Child class, but without @override decorator, a docstring is required.
class Child(Parent):
    def do_something(self):
        pass

# Docstring is trivial, @override is sufficient to indicate that docs can be found in the base class.
class Child(Parent):
    @override
    def do_something(self):
        """See base class."""
```

#### 2.10.3 Classes
Classes should have a docstring below the class definition describing the class. All attributes, excluding 
properties, should be documented here in an Attributes section and follow the same formatting as a function's Args 
section.

```python
class ExampleClass:
    """An example class.

    This example class outlines how a class should be formatted and structured. It provides examples of how attributes, 
    methods, and docstrings should be implemented. Furthermore, it demonstrates the class's implementation structure. 
    Particularly, the grouping of attributes and methods into different sections.   

    Attributes:
        _protected: A protected attribute.
        integer: An integer to track.  
        floating_point: A floating point number to track.
    """
    # Class Attributes #
    class_attribute = ClassVar[int] = 10

    # Class Methods #
    @classmethod
    def class_method(cls) -> None:
        """Prints the class attribute."""
        print(cls.class_attribute)

    # Attributes #
    _protected: bool
    integer: int
    floating_point: float = 1.0

    # Properties #
    @property
    def floating_point_inverse(self) -> float:
        """The inverse of the floating point number."""
        return 1 / self.floating_point

    # Magic Methods #
    # Construction/Destruction #
    def __init__(self, is_protected: bool = True):
        """Initializes the instance based on spam preference.

        Args:
            is_protected: Determines if the attribute is protected.
        """
        self._protected = is_protected
```

All class docstrings should start with a one-line summary that describes what the class instance represents. This 
implies that subclasses of Exception should also describe what the exception represents, and not the context in which it 
might occur. The class docstring should not repeat unnecessary information, such as that the class is a class.

Correct:
```python
class CheeseShopAddress:
    """The address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """No more cheese is available."""
```

Incorrect:
```python
class CheeseShopAddress:
    """Class that describes the address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """Raised when no more cheese is available."""
```


### 2.11 Comments
Comments should be used to outline sections of code and explain tricky parts of the code.

### 2.11.1 Block and Inline
In general, operations can be grouped together into sections based on their purpose. Comments can be used to outline 
these sections and explain the purpose of the code.

Comments Guidelines:
- Comments start with the `#` character and are followed by a space before the text of the comment.
- The start of code sections should have a title comment defining the purpose of that section.
- Complicated sections should get a few lines of comments before the operations. 
- Describe what the section is trying to accomplish and it is achieving that.
- Try not to describe what each line of code is doing.
- Non-obvious ones get comments at the end of the line.
- In-line comments should start at least 2 spaces away from the code they are commenting on.

Good Example:
```python
# Find Location in the Array
# We use a weighted dictionary search to find out where i is in the array. We extrapolate position based on the largest 
# num in the array and the array size and then do binary search to get the exact number.
if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```
Bad Example:
```python
# Now go through the b array and make sure whenever x occurs the next element is x+1
for i, v in enum(b):
    if v == x:
        b[i + 1] = x + 1 
```

#### 2.11.2 TODO Comments
Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect.

A TODO comment begins with the word TODO in all caps, a following colon, and a link to a resource that contains the 
context, ideally a bug reference. A bug reference is preferable because bugs are tracked and have follow-up comments. 
Follow this piece of context with an explanatory string introduced with a hyphen `-`. The purpose is to have a 
consistent TODO format that can be searched to find out how to get more details.

```python
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.
```

Avoid adding TODOs that refer to an individual or team as the context:

```python
# TODO: @yourusername - File an issue and use a '*' for repetition.
```

If your TODO is of the form "At a future date do something" make sure that you either include a very specific date 
("Fix by November 2009") or a very specific event ("Remove this code when all clients can handle XML responses.") that 
future code maintainers will comprehend. Issues are ideal for tracking this.


### 2.12 Punctuation, Spelling, and Grammar
Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.

Comments should be as readable as narrative text, with proper capitalization and punctuation. In many cases, complete 
sentences are more readable than sentence fragments. Shorter comments, such as comments at the end of a line of code, 
can sometimes be less formal, but you should be consistent with your style.


### 2.13 Mathematical Notation
For mathematically-heavy code, short variable names that would otherwise violate the style guide are preferred when they 
match established notation in a reference paper or algorithm.

When using names based on established notation:

- Cite the source of all naming conventions, preferably with a hyperlink to academic resource itself, in a comment or docstring. If the source is not accessible, clearly document the naming conventions.
- Prefer PEP8-compliant descriptive_names for public APIs, which are much more likely to be encountered out of context.
- Use a narrowly-scoped `pylint: disable=invalid-name` directive to silence warnings. For just a few variables, use the directive as an endline comment for each one; for more, apply the directive at the beginning of a block.


### 2.14 Strings
Use an f-string, the % operator, or the format method for formatting strings, even when the parameters are all strings. 
Use your best judgment to decide between string formatting options. A single join with + is okay but do not format with 
+.

Correct:
```python
x = f"name: {name}; score: {n}"
x = "%s, %s!" % (imperative, expletive)
x = "{}, {}".format(first, second)
x = "name: %s; score: %d" % (name, n)
x = "name: %(name)s; score: %(score)d" % {"name":name, "score":n}
x = "name: {}; score: {}".format(name, n)
x = a + b
```

Incorrect:
```python
x = first + ', ' + second
x = "name: " + name + '; score: ' + str(n)
```

Avoid using the `+` and `+=` operators to accumulate a string within a loop. In some conditions, accumulating a string 
with addition can lead to quadratic rather than linear running time. Although common accumulations of this sort may be 
optimized on CPython, that is an implementation detail. The conditions under which an optimization applies are not easy 
to predict and may change. Instead, add each substring to a list and `''.join` the list after the loop terminates, or 
write each substring to an `io.StringIO` buffer. These techniques consistently have amortized-linear run-time 
complexity.

Correct:
```python
items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)
```

Incorrect:
```python
employee_table = '<table>'
for last_name, first_name in employee_list:
    employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
employee_table += '</table>'
```

Be consistent with your choice of string quote character within a file. Pick `'` or `"` and stick with it. It is okay to 
use the other quote character on a string to avoid the need to backslash-escape quote characters within the string.
Typically, double quotes `"` should be used for strings and `'` should be used for single characters.

Correct:
```python
Python('Why are you hiding your eyes?')
Gollum("I'm scared of lint errors.")
Narrator('"Good!" thought a happy Python reviewer.')
Character('I')
```

Incorrect:
```python
Python("Why are you hiding your eyes?")
Gollum('The lint. It burns. It burns us.')
Gollum("Always the great lint. Watching. Watching."
Character("I")
```

Prefer `"""` for multi-line strings rather than `'''`. Projects may choose to use `'''` for all non-docstring multi-line 
strings if and only if they also use `'` for regular strings. Docstrings must use `"""` regardless.

Multi-line strings do not flow with the indentation of the rest of the program. If you need to avoid embedding extra 
space in the string, use either concatenated single-line strings or a multi-line string with `textwrap.dedent()` to 
remove the initial space on each line:

Correct:
```python
long_string = """This is fine if your use case can accept
    extraneous leading spaces."""
```
```python
long_string = ("And this is fine if you cannot accept\n" +
               "extraneous leading spaces.")
```
```python
long_string = ("And this too is fine if you cannot accept\n"
               "extraneous leading spaces.")
```
```python
import textwrap

long_string = textwrap.dedent("""\
    This is also fine, because textwrap.dedent()
    will collapse common leading spaces in each line.""")
```

Incorrect:
```python
long_string = """This is pretty ugly.
Don't do this.
"""
```

Note that using a backslash here does not violate the prohibition against explicit line continuation; in this case, the 
backslash is escaping a newline in a string literal.

#### 2.14.1 Logging
For logging functions that expect a pattern-string (with %-placeholders) as their first argument: Always call them with 
a string literal (not an f-string!) as their first argument with pattern-parameters as subsequent arguments. Some 
logging implementations collect the unexpanded pattern-string as a queryable field. It also prevents spending time 
rendering a message that no logger is configured to output.

Correct:
```python
import tensorflow as tf
logger = tf.get_logger()
logger.info('TensorFlow Version is: %s', tf.__version__)
```
```python
import os
from absl import logging

logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
  logging.error('Cannot write to home directory, $HOME=%r', homedir)
```

Incorrect:
```python
import os
from absl import logging

logging.info('Current $PAGER is:')
logging.info(os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
  logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

#### 2.14.2 Error Messages
Error messages (such as: message strings on exceptions like ValueError, or messages shown to the user) should follow 
three guidelines:

1. The message needs to precisely match the actual error condition.
2. Interpolated pieces need to always be clearly identifiable as such.
3. They should allow simple automated processing (e.g. grepping).

Correct:
```python
if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p}')

try:
    os.rmdir(workdir)
except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r', error, workdir)
```

Incorrect:
```python
if p < 0 or p > 1:  # PROBLEM: also false for float('nan')!
    raise ValueError(f'Not a probability: {p}')

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: Message makes an assumption that might not be true:
    # Deletion might have failed for some other reason, misleading
    # whoever has to debug this.
    logging.warning('Directory already was deleted: %s', workdir)

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: The message is harder to grep for than necessary, and
    # not universally non-confusing for all possible values of `workdir`.
    # Imagine someone calling a library function with such code
    # using a name such as workdir = 'deleted'. The warning would read:
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```


### 2.15 Exceptions
Exceptions must follow certain conditions:

Make use of built-in exception classes when it makes sense. For example, raise a ValueError to indicate a programming 
mistake like a violated precondition, such as may happen when validating function arguments.

Do not use assert statements in place of conditionals or validating preconditions. They must not be critical to the 
application logic. A litmus test would be that the assert could be removed without breaking the code. assert 
conditionals are not guaranteed to be evaluated. For pytest based tests, assert is okay and expected to verify 
expectations.

Examples:

Correct:
```python
def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
        minimum: A port value greater or equal to 1024.

    Returns:
        The new minimum port.

    Raises:
        ConnectionError: If no available port is found.
    """
    if minimum < 1024:
      # Note that this raising of ValueError is not mentioned in the doc
      # string's "Raises:" section because it is not appropriate to
      # guarantee this specific behavioral reaction to API misuse.
      raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
    port = self._find_next_open_port(minimum)
    if port is None:
        raise ConnectionError(
            f'Could not connect to service on port {minimum} or higher.')
    # The code does not depend on the result of this assert.
    assert port >= minimum, (f'Unexpected port {port} when minimum was {minimum}.')
    return port
```

Incorrect:
```python
def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
        minimum: A port value greater or equal to 1024.

    Returns:
        The new minimum port.
    """
    assert minimum >= 1024, 'Minimum port must be at least 1024.'
    # The following code depends on the previous assert.
    port = self._find_next_open_port(minimum)
    assert port is not None
    # The type checking of the return statement relies on the assert.
    return port
```

Libraries or packages may define their own exceptions. When doing so they must inherit from an existing exception class. 
Exception names should end in Error and should not introduce repetition (foo.FooError).

Never use catch-all `except:` statements, or catch `Exception` or `StandardError`, unless you are:
- re-raising the exception, or
- creating an isolation point in the program where exceptions are not propagated but are recorded and suppressed instead, such as protecting a thread from crashing by guarding its outermost block.

Python is very tolerant in this regard and `except:` will really catch everything including misspelled names, sys.exit()
calls, Ctrl+C interrupts, unittest failures and all kinds of other exceptions that you simply don't want to catch.

Minimize the amount of code in a try/except block. The larger the body of the try, the more likely that an exception 
will be raised by a line of code that you didn't expect to raise an exception. In those cases, the try/except block 
hides a real error.

Use the `finally` clause to execute code whether or not an exception is raised in the try block. This is often useful 
for cleanup, i.e., closing a file.


### 2.16 Comprehensions & Generator Expressions
Okay to use for simple cases.

#### 2.16.1 Definition
List, Dict, and Set comprehensions as well as generator expressions provide a concise and efficient way to create 
container types and iterators without resorting to the use of traditional loops, `map()`, `filter()`, or `lambda`.

#### 2.16.2 Pros
Simple comprehensions can be clearer and simpler than other dict, list, or set creation techniques. Generator 
expressions can be very efficient, since they avoid the creation of a list entirely.

#### 2.16.3 Cons
Complicated comprehensions or generator expressions can be hard to read.

#### 2.16.4 Decision
Comprehensions are allowed, however multiple for clauses or filter expressions are not permitted. Optimize for 
readability, not conciseness.

Examples:

Correct:
```python
result = [mapping_expr for value in iterable if filter_expr]
```
```python    
result = [
    is_valid(metric={'key': value})
    for value in interesting_iterable
    if a_longer_filter_expression(value)
]
```
```python    
descriptive_name = [
    transform({'key': key, 'value': value}, color='black')
    for key, value in generate_iterable(some_input)
    if complicated_condition_is_met(key, value)
]
```
```python    
result = []
for x in range(10):
    for y in range(5):
        if x * y > 10:
            result.append((x, y))
```
```python    
return {
    x: complicated_transform(x)
    for x in long_generator_function(parameter)
    if x is not None
}
```
```python    
return (x**2 for x in range(10))
```
```python    
unique_names = {user.name for user in users if user is not None}
```

Incorrect:
```python
result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]
```
```python    
return (
    (x, y, z)
    for x in range(5)
    for y in range(5)
    if x != y
    for z in range(5)
    if y != z
)
```


### 2.17 Default Iterators and Operators
Use default iterators and operators for types that support them, like lists, dictionaries, and files. The built-in types 
define iterator methods, too. Prefer these methods to methods that return lists, except that you should not mutate a 
container while iterating over it.

Examples:

Correct:
```python
for key in adict: ...
if obj in alist: ...
for line in afile: ...
for k, v in adict.items(): ...
```

Incorrect:
```python
for key in adict.keys(): ...
for line in afile.readlines(): ...
```

### 2.18 Generators
Use "Yields:" rather than "Returns:" in the docstring for generator functions.

If the generator manages an expensive resource, make sure to force the clean up.

A good way to do the clean up is by wrapping the generator with a context manager PEP-0533.


### 2.19 Lambda Functions
Okay for one-liners. Prefer generator expressions over map() or filter() with a lambda.

#### 2.19.1 Definition
Lambdas define anonymous functions in an expression, as opposed to a statement.

#### 3.8 Pros
Convenient.

#### 3.8 Cons
Harder to read and debug than local functions. The lack of names means stack traces are difficult to understand. 
Expressiveness is limited because the function may only contain an expression.

#### 3.8 Decision
Lambdas are allowed. If the code inside the lambda function spans multiple lines or is longer than 120 chars, it might 
be better to define it as a regular nested function.

For common operations like multiplication, use the functions from the operator module instead of lambda functions. For 
example, prefer `operator.mul` to `lambda x, y: x * y`.


### 3.8 Conditional Expressions
Okay for simple cases.

#### 2.11.1 Definition
Conditional expressions (sometimes called a "ternary operator") are mechanisms that provide a shorter syntax for if 
statements. For example: `x = 1 if cond else 2`.

#### 2.11.2 Pros
Shorter and more convenient than an if statement.

#### 2.11.3 Cons
May be harder to read than an if statement. The condition may be difficult to locate if the expression is long.

#### 2.11.4 Decision
Okay to use for simple cases. Each portion must fit on one line: true-expression, if-expression, else-expression. Use a 
complete if statement when things get more complicated.

Examples:

Correct:
```python
one_line = 'yes' if predicate(value) else 'no'
```
```python    
slightly_split = ('yes' if predicate(value)
                  else 'no, nein, nyet')
```
```python    
the_longest_ternary_style_that_can_be_done = (
    'yes, true, affirmative, confirmed, correct'
    if predicate(value)
    else 'no, false, negative, nay'
)
```

Incorrect:
```python
# No:
bad_line_breaking = ('yes' if predicate(value) else
                     'no')
```
```python    
portion_too_long = ('yes'
                    if some_long_module.some_long_predicate_function(
                        really_long_variable_name)
                    else 'no, false, negative, nay')
```


### 2.14 True/False Evaluations
Use the "implicit" false if at all possible (with a few caveats).

#### 2.14.1 Definition
Python evaluates certain values as False when in a boolean context. A quick "rule of thumb" is that all "empty" values 
are considered false, so 0, None, [], {}, '' all evaluate as false in a boolean context.

#### 2.14.2 Pros
Conditions using Python booleans are easier to read and less error-prone. In most cases, they're also faster.

#### 2.14.3 Cons
May look strange to C/C++ developers.

#### 2.14.4 Decision
Use the "implicit" false if possible, e.g., `if foo:` rather than `if foo != []:`. There are a few caveats that you 
should keep in mind though:

Always use `if foo is None:` (or `is not None`) to check for a None value. E.g., when testing whether a variable or 
argument that defaults to None was set to some other value. The other value might be a value that's false in a boolean 
context!

Never compare a boolean variable to False using `==`. Use `if not x:` instead. If you need to distinguish False from 
None then chain the expressions, such as `if not x and x is not None:`.

For sequences (strings, lists, tuples), use the fact that empty sequences are false, so `if seq:` and `if not seq:` are 
preferable to `if len(seq):` and `if not len(seq):` respectively.

When handling integers, implicit false may involve more risk than benefit (i.e., accidentally handling None as 0). You 
may compare a value which is known to be an integer (and is not the result of len()) against the integer 0.

Examples:

Correct:
```python
if not users:
    print('no users')
```
```python
if i % 10 == 0:
    self.handle_multiple_of_ten()
```
```python    
def f(x=None):
    if x is None:
        x = []
```

Incorrect:
```python
if len(users) == 0:
    print('no users')
```
```python    
if not i % 10:
    self.handle_multiple_of_ten()
```
```python    
def f(x=None):
    x = x or []
```
Note that '0' (i.e., 0 as string) evaluates to true.

Note that Numpy arrays may raise an exception in an implicit boolean context. Prefer the .size attribute when testing 
emptiness of a np.array (e.g. `if not users.size`).


### 3.11 Files, Sockets, and similar Stateful Resources
Explicitly close files and sockets when done with them. This rule naturally extends to closeable resources that 
internally use sockets, such as database connections, and also other resources that need to be closed down in a similar 
fashion. To name only a few examples, this also includes mmap mappings, h5py File objects, and matplotlib.pyplot figure 
windows.

Leaving files, sockets or other such stateful objects open unnecessarily has many downsides:

- They may consume limited system resources, such as file descriptors. Code that deals with many such objects may exhaust those resources unnecessarily if they're not returned to the system promptly after use.
- Holding files open may prevent other actions such as moving or deleting them, or unmounting a filesystem.
- Files and sockets that are shared throughout a program may inadvertently be read from or written to after logically being closed. If they are actually closed, attempts to read or write from them will raise exceptions, making the problem known sooner.

Furthermore, while files and sockets (and some similarly behaving resources) are automatically closed when the object is 
destructed, coupling the lifetime of the object to the state of the resource is poor practice:

- There are no guarantees as to when the runtime will actually invoke the `__del__` method. Different Python implementations use different memory management techniques, such as delayed garbage collection, which may increase the object's lifetime arbitrarily and indefinitely.
- Unexpected references to the file, e.g. in globals or exception tracebacks, may keep it around longer than intended.
- Relying on finalizers to do automatic cleanup that has observable side effects has been rediscovered over and over again to lead to major problems, across many decades and multiple languages (see e.g. this article for Java).

The preferred way to manage files and similar resources is using the `with` statement:

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```

For file-like objects that do not support the `with` statement, use `contextlib.closing()`:

```python
import contextlib

with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

In rare cases where context-based resource management is infeasible, code documentation must explain clearly how 
resource lifetime is managed.


### 2.17 Function and Method Decorators
Use decorators judiciously when there is a clear advantage. Avoid `staticmethod` and limit use of `classmethod`.

#### 2.17.1 Definition
Decorators for Functions and Methods (a.k.a "the @ notation"). One common decorator is `@property`, used for converting 
ordinary methods into dynamically computed attributes. However, the decorator syntax allows for user-defined decorators 
as well. Specifically, for some function my_decorator, this:

```python
class C:
    @my_decorator
    def method(self):
        # method body ...
```

is equivalent to:

```python
class C:
    def method(self):
        # method body ...
    method = my_decorator(method)
```

#### 2.17.2 Pros
Elegantly specifies some transformation on a method; the transformation might eliminate some repetitive code, enforce 
invariants, etc.

#### 2.17.3 Cons
Decorators can perform arbitrary operations on a function's arguments or return values, resulting in surprising implicit 
behavior. Additionally, decorators execute at object definition time. For module-level objects (classes, module 
functions, …) this happens at import time. Failures in decorator code are pretty much impossible to recover from.

#### 2.17.4 Decision
Use decorators judiciously when there is a clear advantage. Decorators should follow the same import and naming 
guidelines as functions. A decorator docstring should clearly state that the function is a decorator. Write unit tests 
for decorators.

Avoid external dependencies in the decorator itself (e.g. don't rely on files, sockets, database connections, etc.), 
since they might not be available when the decorator runs (at import time, perhaps from pydoc or other tools). A 
decorator that is called with valid parameters should (as much as possible) be guaranteed to succeed in all cases.

Decorators are a special case of "top-level code" - see main for more discussion.


### 2.12 Default Argument Values
Okay in most cases.

#### 2.12.1 Definition
You can specify values for variables at the end of a function's parameter list, e.g., `def foo(a, b=0):`. If foo is 
called with only one argument, b is set to 0. If it is called with two arguments, b has the value of the second argument.

#### 2.12.2 Pros
Often you have a function that uses lots of default values, but on rare occasions you want to override the defaults. 
Default argument values provide an easy way to do this, without having to define lots of functions for the rare 
exceptions. As Python does not support overloaded methods/functions, default arguments are an easy way of "faking" the 
overloading behavior.

#### 2.12.3 Cons
Default arguments are evaluated once at module load time. This may cause problems if the argument is a mutable object 
such as a list or a dictionary. If the function modifies the object (e.g., by appending an item to a list), the default 
value is modified.

#### 2.12.4 Decision
Okay to use with the following caveat:
Do not use mutable objects as default values in the function or method definition.

Examples:

Correct:
```python
def foo(a, b=None):
    if b is None:
        b = []
```
```python
def foo(a, b: Sequence | None = None):
    if b is None:
        b = []
```
```python
def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable.
    ...
```

Incorrect:
```python
def foo(a, b=[]):
    ...
```
```python
def foo(a, b=time.time()):  # Is `b` supposed to represent when this module was loaded?
    ...
```
```python
def foo(a, b=_FOO.value):  # sys.argv has not yet been parsed...
    ...
```
```python
def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code.
    ...
```
