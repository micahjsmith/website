Title: Dataclasses and mutable defaults
Date: 2020-01-14 
Category: programming
Tags: pythong
Slug: dataclasses-mutable-defaults
Authors: Micah Smith

One common Python gotcha is the use of mutable objects as defaults for function keyword
arguments. There are approximately one billion questions on SO about this or [nice
discussions](https://pythonconquerstheuniverse.wordpress.com/2012/02/15/mutable-default-arguments/)
elsewhere. I came across a nice feature in Python's dataclasses library that addresses a
similar problem.

### Mutable defaults are bad

As a reminder, in this example, every invocation of foo without a parameter for `d`
provided by the caller would modify the *same* default dictionary (equivalent to the second
example). 

```python
# this...
def foo(d={}):
    ...

# is equivalent to this
default = {}  # this is a global object!
def foo(d=default):
    ...
```

You always want to instead use a value like `None` and check in the function or method body
whether a default needs to be supplied, and document the function's behavior accordingly as
it cannot be inferred from the type signatures.

```python
# better
def foo(d=None):
    """Does foo

    Args:
        d (dict): some parameter. Defaults to {}.
    """
    if d is None:
        d = {}
    ...
```

### Named tuples

A similar gotcha is using mutable defaults for named tuples.

```python
from typing import Dict, NamedTuple

class Foo(NamedTuple):
    d: Dict = {}  # no
```

Again, every instance of `Foo` that uses the default value will share a reference to a
single underlying object. Instead, set the default to `None` and require consumers to check
whether `d is None`.

### Dataclasses

[Dataclasses](https://docs.python.org/3/library/dataclasses.html) are like named tuples, but better in every way. One feature I recently
discovered is the [ability to use a default
factory](https://docs.python.org/3/library/dataclasses.html#dataclasses.field) to avoid this issue.

```python
from dataclasses import dataclass, field

@dataclass
class Foo:
    d: Dict = field(default_factory=dict)
```

With this paradigm, every time a default needs to be supplied for `d`, the factory function
will be called, creating a new dictionary object each time and side-stepping the gotcha.
Additionally, consumers of `Foo` can always assume that `d` is a dict and simplify their
code accordingly.
