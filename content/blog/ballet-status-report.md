Title: Invitation to dance: a status report on the Ballet project
Date: 2020-05-22
Category: research
Tags: ballet, feature engineering, machine learning
Slug: ballet-status-report
Authors: Micah Smith
Status: draft

At MIT, we recently marked the close of one of the most turbulent academic years on record, in which academic and research activities were significantly disrupted by the emergence of the COVID-19 pandemic, which has by now, killed over 400,000 people globally and over 100,000 people in the US. As neighbors and loved ones got sick, we all asked ourselves the question, "what can I do to help?" For many of my colleagues at MIT, this mean accelerating engineering and design work on [personal protective equipment and medical devices](https://project-manus.mit.edu/) or contact tracing apps or vaccines and therapeutics. However the expertise of many others did not lend itself to these direct responses. Instead, a swarm of academic and independent data scientists took to putting their skills to use to try to predict the trajectory of new infections, identify positive cases from chest X-rays, generate heat maps from foot traffic data or satellite imagery, or aggregate signs of pre-symptomatic individuals -- with varying degrees of success and statistical rigor. <!-- TODO links -->

t@masonporter/status/1273054551583555585

What happens when hundreds or thousands of people try to collaborate on similar data science projects in real time? As we found here -- and as we have found in similar prior situations -- the result is a lot of noise. TODO

I've been following these efforts closely, especially because I've been thinking about some of these exact same issues as part of my PhD research for several years now. The project I've been working on is *Ballet*, a software framework for collaborative data science. I'm taking this moment to provide a status update on the project and inviting you to learn more about this work.

## Introduction to Ballet

While the open-source model for software development has led to successful, large-scale collaborations in most software projects, it has not been nearly as successful in data science and in particular, predictive/supervised machine learning.[^1]

I am always struck by the order of magnitude differences in the table below. It shows the number of unique contributors to projects in software engineering and data science that I identified as the largest open-source collaborations through extensive research. While there are many reasons for this disparity, I'd like to focus on two of them.

| Software engineering |   | Data science |   |
| -------------------- | - | ------------ | - |
| Linux kernel | 20,000+ | drug-spending | 20 |
| Ruby on Rails | 3,800+ | police-eis | 19 |
| kubernetes | 2,200 + | crash-model | 17 |
| tensorflow | 2,100+ | food-inspections | 8 |

The first is that it is difficult to decompose data science pipelines into small modular patches. Unlike software engineering, where a patch can be applied to introduce a new software feature or fix a bug, its less apparent how to "patch" a data science pipeline to improve its performance. This is especially challenging as many parts of the data science process are usually implemented in end-to-end scripts. Without the ability to apply modular patches, it is difficult or impossible to use version control tools to collaborative on a single project.

This leads to the second reason, which is that the primary development environment and workflow for data scientists is prototyping and exploration in computational notebooks. I love Jupyter Notebooks, and use them all of the time in my work, but [many writers](web.eecs.utk.edu/~azh/pubs/Chattopadhyay2020CHI_NotebookPainpoints.pdf) have [pointed out](https://dl.acm.org/doi/10.1145/3290605.3300500) their [drawbacks](https://dl.acm.org/doi/10.1145/3359141): difficulty managing code, sharing code and receiving feedback, replicating results, cleaning up "messes", productionizing models and analyses. And notebooks simply don't fit in traditional software engineering workflows. The telltale sign of this mismatch in a project is a directory named `notebooks/` containing notebooks each authored by a single person.

To address these challenges, I've been working on a new way to facilitate collaboration in data science projects. The first part of the approach is based on finding ways to decompose the data science process into modular patches -- standalone units of contribution -- that can be intelligently combined, representing objects like "feature", "labeling function", or "prediction task definition". Prospective contributors work in parallel to write patches and submit them to an open-source repo where our framework provides functionality to identify and merge high-quality contributions and compose the accepted patches into a single product. The second part of the approach is meeting data scientists where they are -- the notebook -- as the primary IDE. After prototyping a new feature, say, within a notebook, using our interface a data scientist can transparently submit the code that defines that feature only as a pull request to the upstream project repo without bothering themselves with any git details.

In the rest of this post I will go through many of these ideas in an end-to-end example of collaborating on a house price prediction problem.

## Collaborating on feature engineering for house price prediction

Let's take a closer look at these ideas through the case of a collaboration on feature engineering for house price prediction. Here the data is raw characteristics of houses and their selling prices in Ames, IA. This messy, real-world dataset requires significant feature engineering by experts before a usable feature matrix can be input to a learning algorithm.

<div style="text-align: center;">
<object type="image/svg+xml" data="https://gh-card.dev/repos/HDI-Project/ballet-predict-house-prices.svg?link_target=_blank"></object>
</div>

### Completed feature engineering pipeline

Let's first imagine the project has already been completed. What is the product that has been made available to the data science community? It is an end-to-end feature engineering pipeline that can be fit on existing house price data and used to extract feature values from unseen house records. The project can be pip-installed by a totally different set of developers, and the feature engineering pipeline can then be inserted into some other ML pipeline.

```python
from ballet_predict_house_prices.load_data import load_data
X_df_tr, y_df_tr = load_data(input_dir='./data/train')
X_df_te, _ = load_data(input_dir='./data/test')

from ballet_predict_house_prices.features import build
mapper = build(X_df_tr, y_df_tr).mapper_X

mapper.transform(X_df_te)
```

### One feature at a time

Well that's great. We have a robust feature engineering pipeline that can be fit on training data and applied on unseen data instances to extract feature values. Our downstream collaborators can use this as a key input to their modeling process. But how did we build this pipeline in the first place?

The key here is the insight that feature engineering can be represented as a dataflow graph over individual features. We structure code that extracts a group of feature values as an individual patch, calling these *logical features*. Individual features are represented as individual Python modules, stored in the git source, and "collected" dynamically by the Ballet framework.

As one plugin for Ballet, we create a small embedded language for feature engineering. Users are responsible for declaring one or more input columns to their feature and one or more sklearn-style transformers that sequentially operate on these columns. We supplement the many high-quality transformers available in `sklearn` and elsewhere with feature engineering primitives. This makes it easier to rewrite imperative Pandas code to be modular and robust to unseen data.

Here's how it looks. The user has requested the `Lot Area` variable from the raw dataset, which contains noisy measurements of each house's lot area. They propose to first conditionally unskew this variable by taking the log of the lot area if the skew on the training data is greater than some threshold (here at `0.75`). Then any houses that have missing lot areas are imputed with the mean of the training lot area. (If the imputation were done first, the level of skew in the training data would be artificially less as new observations would be added at the mean.)

```python
from ballet import Feature
from ballet.eng import ConditionalTransformer
import numpy as np
from sklearn.impute import SimpleImputer

input = 'Lot Area'
transformer = [
  ConditionalTransformer(
    lambda ser: ser.skew() > 0.75,
    lambda ser: np.log1p(ser)),
  SimpleImputer(strategy='mean'),
]
name = 'Lot area unskewed'
feature = Feature(input=input, transformer=transformer, name=name)
```

`Feature` objects can then be composed as part of a `FeatureEngineeringPipeline`, which in turn provides a transformer API:

```python
from ballet.pipeline import FeatureEngineeringPipeline
pipeline = FeatureEngineeringPipeline([feature1, feature2, feature3])
pipeline.fit_transform(X_df)
```

The pipeline extracts feature values more or less as follows (replacing `fit_transform` with just `transform` after training).

```python
# pseudocode
for feature in features:
  x = X_df[input]
  for transformer in feature.transformer:
    x = transformer.fit_transform(x)
  yield x
```

The Ballet [Feature Engineering Guide](https://hdi-project.github.io/ballet/feature_engineering_guide.html) provides a more full discussion.

So a feature engineering pipeline is composed of many individual features. These features are developed independently and in parallel by contributors to the project.

### Experiment and develop

As we discussed above, a development workflow that requires data scientists to clone a repo, set up a virtualenv, work on a new branch, write and run unit tests, and push code to be reviewed, is a relatively high burden compared to their desire to experiment and develop in a notebook environment. We address this by pairing every Ballet project with a cloud Jupyter Lab environment provided by [Binder](https://mybinder.org/)

![Launch binder from project repo]({files}/images/ballet-status-report/launch_binder.gif)

### Validate, validate, validate

Suppose that a prospective contributor has developed the `Lot area unskewed` feature shown above and wants to contribute it to the upstream project. Just as in typical software project, new code contributions must be thoroughly evaluated for quality before being accepted, so too must we evaluate contributions of logical features. Here, Ballet identifies analogues for unit testing and integration testing: feature testing and streaming logical feature selection.

*Feature testing* consists of two steps, a feature API check and a project structure check. Broadly, these ensure that the user-contributed feature provides the proper API and successfully deals with common error situations, such as intermediate computations producing missing or non-numeric values.

*Streaming logical feature selection* evaluates feature contributions in terms of their impact on machine learning performance. Does the feature engineering pipeline have better predictive performance with or without the proposed feature? TODO

### Submit where you code

TODO

### Automate as much as possible

TODO

## Conclusion

Interested by these ideas? The [ballet-predict-house-prices](https://github.com/HDI-Project/ballet-predict-house-prices) project welcomes new collaborators. You can also use Ballet to set up your own collaboration or [get in touch]({filename}/pages/contact.md) with me directly.

### notes

who is my intended audience?
=> data scientists who might want to collaborate

what is my argument?
=> need to convince them briefly of the benefits of collaboration in open-source and make them curious about why there have not been larger collaborations in the sense that i define. now give a high level idea of the ballet framework by making analogies with software engineering. describe one application of these ideas to feature engineering. introduce the demo for feature engineering in house price prediction. next, what is the best development workflow for this collaboration? identify issues with using low-level git commands, setting up development environment, etc: data scientists prefer to work in notebook environments instead. Bridge this gap by creating an interface that allows contribution to repos directly from a notebook environment. even further, build this on top of mybinder. result is end-to-end data science workflow + ability to contribute done in cloud.

what is my invitation?
=> check out the demo project, try to contribute a feature, use the existing pipeline in your own model. leave feedback (how) or even better complete the full survey.

## begin

quick description of ballet

quick description of ballet-predict-house-prices

description of

### Further reading

- [Ask me for a preprint]({filename}/pages/contact.md) of the full-length paper on Ballet.
- [Read about the Ballet framework](https://hdi-project.github.io/ballet/).
- In March, I attended MLSys 2020 where I presented a live demonstration of Ballet. [Check out my account of the conference]({filename}mlsys-2020.md) or [read the short paper about my demonstration]({static}/files/balletdemo_mlsys2020.pdf).
- [Join a collaboration](https://github.com/HDI-Project/ballet-predict-house-prices) in feature engineering for house price prediction.

[^1]: In predictive ML projects, the output of the project is not a software library, but rather a trained model capable of serving predictions for new datapoints.
