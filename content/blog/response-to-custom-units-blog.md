Title: Julia and Python code comparison blogs
Date: 2017-10-31
Category: programming
Tags: julia, python
Slug: julia-python-code-comparison-blogs
Authors: Micah Smith
Status: draft

I frequently see blog posts from Julia language users and evangelists that
compare a Julia solution to some programming problem to a Python solution to that same
problem. My impression is that these posts aim to demonstrate how a fundamental problem that
one encounters when using Python or some other language can be solved easily and naturally
in Julia. I find these posts relatively unhelpful.

Take as example this recent post by Erik Engheim entitled [Defining Custom Units in Julia
and Python](https://medium.com/@Jernfrost/defining-custom-units-in-julia-and-python-513c34a4c971).
The author identifies his problem as doing calculations with quantities in different units,
and then explores how he would solve this in both Python and Julia for the problem of doing
calculations on values measuring temperature in different units. It's a well-written
piece, but misses hitting home its key point in several ways.

### Suboptimal Python solution

The author shows a Python solution, critiques it, and then later shows how Julia addresses
those issues. But it seems to me like most of the problems with the Python solution are
specific to his implementation.

To be sure, in advance, the author acknowledges that
> not being as good with Python as with Julia, this might not be the most optimal way of
> solving the problem.

Let's take a look. He starts by defining two classes, `Celsius` and `Kelvin`, that both
separately inherit from the top-level `object`. Immediately, by not using the most basic
abstractions in object-oriented programming, the author starts running into problems. For
example, the existing implementations use

```
class Celsius(object):
    def __init__(self, temp):
        super(Celsius, self).__init__()
        if type(temp) == float or type(temp) == int:
            self.value = temp
        else:
            self.value = temp.to_celsius().value

    def __repr__(self):
        return "Celsius({0})".format(self.value)

    # ... more stuff ...

class Kelvin(object):
    def __init__(self, temp):
        super(Kelvin, self).__init__()
        if type(temp) == float or type(temp) == int:
            self.value = temp
        else:
            self.value = temp.to_kelvin().value

    def __repr__(self):
        return "Kelvin({0})".format(self.value)

    # ... more stuff ...
```

Instead, it is natural to define an abstract parent class, `Temperature`, which greatly
simplifies things. In particular, we no longer need to reimplement the constructor and the
`__repr__` function for each subclass. 

```
class Temperature(object):
    def __init__(self, temp):
        self.temp = temp

    def __repr__(self):
        return "{classname}({value})".format(
            classname=self.__class__.__name__,
            value=self.value,
        )

class Celsius(Temperature):
    pass

class Kelvin(Temperature):
    pass
```

Next, if we make a design decision to use Kelvin as a common temperature for all
conversions, then we no longer need to implement add and subtract separately for each
subclass. Any new temperature unit can provide methods to convert to and from Kelvin, all
arithmetic can take place in Kelvin, and the result can be converted back into the original
unit.

I begin to doubt a useful comparison to Python whenever the core tenets of OOP are violated
this much.

### Losing the main point

The power of multiple dispatch in Julia allows one to define new types that can be operated
on naturally, as mathematical quantities. One can define promotions between pairs of types
and This is convincing to me as someone who has worked
with Julia extensively, but the author gets bogged down in the weeds. 

> My python solution is 60 lines of source code while the Julia version is almost half at 32
> lines, despite offering more functionality.

These "lines of code" comparisons are mostly useless at this scale of toy examples, in my
opinion. And especially unhelpful if the Python solution is artificially long due to
suboptimal design.
