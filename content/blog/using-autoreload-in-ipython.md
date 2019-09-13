Title: Using autoreload in IPython
Date: 2019-09-13
Category: programming
Tags: python, ipython, jupyter
Slug: using-autoreload-in-ipython
Authors: Micah Smith

Using the autoreload extension.

```
%load_ext autoreload
%aimport mymodule
%autoreload 1
```

The `autoreload` command understands three levels:

- 0 -> extension is disabled
- 1 -> reload modules that were marked with %aimport
- 2 -> reload everything

The easiest usage of autoreload is to not `aimport` anything and set `%autoreload 2`, which causes the extension to reload *all* code before any Python code is run. This *seems* excessive but I have not necessarily noticed any performance issues from doing so. Regardless, I'm often only developing one library at a time, so marking that library only with `%aimport` and using level 1 seems more explicit.

Source: <https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html>
