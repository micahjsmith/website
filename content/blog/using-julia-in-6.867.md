Title: Why I'm bailing on Julia for machine learning
Date: 2016-11-04
Category: programming
Tags: julia, python, ml
Slug: why-im-bailing-on-julia-for-machine-learning
Authors: Micah Smith

I'm bailing on Julia for machine learning — just for my one class, that is. Don't worry
~too much~!

I'm taking graduate machine learning (6.867) this semester at MIT. There are three homework
assignments in the course that are structured as mini-projects, in which students
implement canonical algorithms from scratch and then use them to analyze datasets or
explore the effects of hyperparameters. "Official support" — in the sense of skeleton code,
plotting routines, and TA assistance — is provided for MATLAB and Python only. Working in
Julia (or another language) is allowed, but *the going is solo*.

After sticking with Julia for the first two assignments, I'm bailing for
the rest of the semester.  Although Julia is great-looking, fun to write, and
performant as ever, there were a lot of challenges I ran into in using existing
functionality within my assignments. Specifically, I found the stats/ML packages pale in
comparison to `sklearn` in terms of functionality and ease of use. While it was great to use
Julia to implement my own algorithms, it turned out to be a real hassle to tie in with
existing functionality.

As one of several small issues, here's the trouble I went through just to use
pre-existing functionality to fit a logistic regression model.

### Logistic regression case study

What's the quickest way to fit a logistic regression model for classification? A quick
[search](http://lmgtfy.com/?q=logistic+regression+julia) brings up the
[JuliaStats](juliastats.github.io) page (as my first result, at least) with a variety of
packages listed. From the descriptions, it seems like our candidates for logistic regression
solvers are *GLM.jl* and *RegERMs.jl.* The next search results are for *Regression.jl* and a
couple DIY logistic regression examples.

Let's assess our options:

- *GLM.jl*: Has most of the goods, but as we'll see, it didn't have all the features I needed
    for my assignment.
- *RegERMs.jl*: Doesn't even load on Julia 0.5, last commit over a year ago.
```
julia> Pkg.add("RegERMs")
ERROR: unsatisfiable package requirements detected: no feasible version could be found
for package: Optim
```
- *Regression.jl*: Doesn't even load on Julia 0.5, last commit over a year ago.
```
julia> using Regression
ERROR: LoadError: LoadError: LoadError: UndefVarError: FloatingPoint not defined
```

So *GLM.jl* is our only option. And at this, a new Julia user might be lucky to even find it.
It's not immediate from the JuliaStats blurb that *GLM.jl* can be used for logistic regression,
and there's no mention of "logistic" neither in the documentation nor in the repo itself
besides a comment in a test case. (An astute user, of course, may note that `LogitLink` is
relevant, and will likely be aware of the features of the popular R package.)

But it's not too bad to fit a logistic regression model using *GLM.jl*:
```
using GLM, DataFrames
df = DataFrame(x = rand(10,1), y = rand([0,1], 10))
model = fit(GeneralizedLinearModel, y ~ x, df, Binomial(), LogitLink())
```

Note as well that the DIY logistic regression attempts that rank highly in search results (like
[here](http://stackoverflow.com/questions/32703119/logistic-regression-in-julia-using-optim-jl)
and [here](http://int8.io/logstic-regression-with-gradient-descent-in-julia/)) are not super
helpful for the purposes of quickly fitting a model, but are typical of the content that
comes up in results for Julia queries.

### Adding L1/L2 regularization

In one of the 6.867 assignments, we are asked to apply logistic regression with L1/L2
regularization. *GLM.jl* doesn't provide this functionality and the other seeming possibilities
were non-functional *RegERMs.jl*. I was out of luck. I switched to `sklearn` for the rest of
the problem.

```
import numpy as np
from sklearn.linear_model import LogisticRegression
X = np.random.rand(10,1)
Y = np.random.rand(10).round()
model = LogisticRegression(penalty='l1')
model.fit(X, Y)
```

After later investigation, I did realize that *GLMNet.jl*, which wraps the `glmnet` Fortran library,
would have done the job, with sufficient user effort. 

### The pieces are there, the whole is missing

We were able to fit our logistic regression classifier after a fair amount of digging. But
this digging shouldn't be necessary. It should have been easier to find a logistic
regression *that works* from the JuliaStats landing page, given that this is a pretty
standard learning algorithm. And inconsistencies within the JuliaStats organization seem to
be a fair problem. A user might start by using *GLM.jl*. But to add regularization to the
loss function requires to switch to a different package, with a slightly different API so
that the old code can't be dropped in. The
["interface"](http://statsbasejl.readthedocs.io/en/latest/statmodels.html) in StatsBase.jl
isn't totally implemented in some of these more niche packages (*GLMNet.jl*, *Lasso.jl*), or isn't
particularly followed at all, especially when the package wraps some underlying library
(*LIBSVM.jl*).

Then, we have the entirely different entity that is [JuliaML](juliaml.github.io). Here, we
have a design and API that seem to be in direct competition with JuliaStats
(*StatsBase.jl*/*MLBase.jl* vs *LearnBase.jl*, *Distances.jl* vs *LossFunctions.jl*,
*RegERMs.jl* vs *MLRisk.jl*, etc.). I wasn't sure how to even start using it, let alone
attempt to theoretically combine *LossFunctions.jl*, *StochasticOptimization.jl*, and
*MLMetrics.jl* into something resembling an end-to-end model. I can't quite figure out what
space JuliaML is trying to fit.

Overall, I think that JuliaStats is doing a very good job and is *almost there*. Packages
like *StatsBase.jl*, *DataFrames.jl*, and *Distributions.jl* are really great to use. Certainly,
the obvious response to the difficulties I had above is that more community support is
needed. Can't argue with that.

### Conclusion

Julia has been perfectly suited for quickly coding up ML algorithms from scratch and really
getting my hands dirty. But when I wanted to quickly and easily drop in robust community
packages, I found that the functionality wasn't there.

I'll be using the Python ecosystem for the next assignment, in which we implement neural
nets/backprop. If I find myself having to bust out `sklearn` more regularly, I better figure
out how to use it fluidly.
