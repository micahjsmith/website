Title: research
Slug: research
Template: bibliography
Order: 01

Below is my (mostly) complete bibliography with links to articles, presentations, posters, videos, and suggested citations. Make sure to check my [blog](/blog) as well for additional informal discussion of some of this research.

## Projects

### Collaborative data science development

While the open-source model for software development has led to successful, large-scale collaborations in building software applications, chess engines, and scientific analyses, data science has not benefited from this development paradigm. In part, this is due to the divide between the development processes used by software engineers and those used by data scientists.

*Ballet* tries to address this disparity. It is a lightweight software framework that supports collaborative data science development by composing a data science pipeline from a collection of modular patches that can be written in parallel. Ballet provides the underlying functionality to support interactive development, test and merge high-quality contributions, and compose the accepted contributions into a single product.

I've led development of the core [Ballet](https://github.com/HDI-Project/ballet) framework, the [Assemblé](https://github.com/HDI-Project/ballet-assemble/) development environment, the Ballet [Bot](https://github.com/HDI-Project/ballet-bot), and a bunch of other software.

We've evaluated Ballet in an extensive case study analysis of a personal income prediction project, and describe our ideas for collaborative data science development, the design of the framework, and the results of this evaluation in [our preprint](#smith2020enabling).

### Frameworks for AutoML

In our experience developing and deploying ML systems in my research group, we realized that every project used a different set of libraries depending on the task at hand that fit together more or less poorly. To address this, we redesign our systems building approach to one based on the concepts ML primitives, ML pipelines, and AutoML components. The resulting software framework is used for everything from [our entry](https://github.com/MLBazaar/AutoBazaar) to DARPA's [Data-Driven Discovery of Models program](https://www.darpa.mil/program/data-driven-discovery-of-models) to [unsupervised time-series anomaly detection in satellite telemetry](https://github.com/signals-dev/Orion) to [ML on electronic health records](https://github.com/DAI-Lab/Cardea). I designed the [BTB](https://github.com/MLBazaar/BTB) library for model selection and hyperparameter tuning which has also been contributed to by many folks in the Data to AI Lab. We describe the framework, some of the ML and AutoML systems we have built with it, and a thorough evaluation in [this paper](#smith2020machine).

### Systems for AutoML

I am a developer on the [ATM](https://hdi-project.github.io/ATM/) project, a full-fledged open-source system for joint model selection and hyperparameter tuning for classification. ATM is one of the first projects from the research community that went beyond the creation of libraries for model selection or hyperparameter tuning to create a system with a database backend designed for ease of use and high performance. On top of this, we collaborated with the [VisLab](http://vis.cse.ust.hk/) at HKUST to create a frontend for ATM that allows users to monitor and control an ongoing AutoML search process. This led to the [ATMSeer](https://dai.lids.mit.edu/projects/atmseer/) system which we describe in [this paper](#wang2019atmseer).
