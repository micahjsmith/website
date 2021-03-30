Title: Preprint of Assemblé
Date: 2021-03-30
Category: research
Tags: ballet
Slug: preprint-of-assemble
Authors: Micah Smith

I'm excited to share that we have [posted a preprint to arXiv](https://arxiv.org/abs/2103.15787) of our [paper]({filename}/pages/research.md#smith2021meeting), "Meeting in the notebook: a notebook-based environment for micro-submissions in data science collaborations." This preprint describes the design and implementation of [Assemblé](https://github.com/ballet/ballet-assemble), a development environment for data science collaborations that is targeted to [Ballet]({tag}ballet). This is joint work with Jürgen Cito and Kalyan Veeramachaneni.

A data science collaboration facilitated by Ballet focuses the effort of individual contributors in creating small modules that can be composed into a single data science pipeline, such as feature definitions that can be composed into a feature engineering pipeline. We found both in small formative studies and in larger case studies that while data science developers succeeded in creating feature definitions after a period of exploratory analysis, they then struggled to "close the loop" and extract the feature definition from their Jupyter Notebook in order to contribute it back to the upstream repository.

If you are familiar with software development processes, [this would otherwise entail](https://ballet.github.io/ballet/contributor_guide.html#local-feature-development-workflow):

1. Fork the upstream project.
1. Clone the fork locally.
1. Install the project into a new virtualenv.
1. Create a new branch to work on the new feature definition.
1. Start a new feature by creating empty source files at the right file paths (i.e. `ballet start-new-feature`)
1. Copy the feature definition from your notebook into the new source file, additionally extracting any imports/symbols defined in earlier code cells.
1. Test the new feature definition works using the command line validator (i.e. `ballet validate`).
1. Commit the changes.
1. Push the branch to the fork.
1. Create a pull request, using either a client like `hub` or via the GitHub UI.

We call this *patch contribution task*. This task is difficult to complete with high fidelity, especially for data science developers who are less familiar with this type of process.

To address this, we made the insight that data science developers *are already successfully working within the notebook environment* and that the patch contribution task can then be automated under certain conditions without forcing the use of other tools. We operationalize this by creating a development environment on top of JupyterLab, Binder, and Ballet that brings all of the pieces together to support exploratory analysis, feature definition creation, and patch contribution all within the notebook, *meeting developers where they already are*.

First, Assemblé uses Binder to allow a Ballet project to be launched from a badge in the project's README with the project source code and all dependencies already installed. Next, developers can use Ballet's interactive client to load data, explore data and existing features, create their own feature definition, and validate it from within the notebook. Then, instead of forcing developers to switch to a different set of tooling and wrestle with details of git workflows, Assemblé provides a one-click "Submit" button that allows developers to select a feature definition from code cells within their messy notebook and cause it to be automatically formulated as a well-structured pull request to the upstream shared repository.

The result of this is that data science developers can collaborate using the pull request model of open-source development without even knowing that git is being used being the scenes, as these low-level details are completely abstracted away.

<video autoplay=true loop=true muted=true width="640" height="480"
       name="Video Name" src="{static}/images/assemble-submit-feature.mov"></video>

The user interface of Assemblé is a bit bare (mainly because I'm not the best front-end developer!), so one thing we are working on is improving this experience. One example is by providing more visibility into the steps that are automated during the submission process which helps developers understand more about how Ballet works. We're also exploring two new directions for this work. The first is to meet developers in the notebook even more by exposing the pull request review process within the JupyterLab environment, for example by showing the pull request review outcomes of the feature definitions that they have submitted as well as those submitted by others, and surfacing failures and potential fixes for rejected PRs. The second is to make it even easier to identify patches to submit by allowing developers to automatically "collect" pieces of the feature definition that have been defined across cells by using automated tools such as the [gather](https://github.com/microsoft/gather) extension, which uses program slicing techniques to identify program dependencies.

Please check it out and feel free to [share any feedback]({filename}/pages/contact.md).
