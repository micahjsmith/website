Title: Pipenv install with all the flags, explained
Date: 2020-11-19
Category: programming
Tags: python, pipenv, docker
Slug: pipenv-install-with-all-the-flags-explained
Authors: Micah Smith

A common pattern of using [pipenv](pipenv.pypa.io/) in containers is to install as follows:

```Dockerfile
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    pipenv --clear
```

What is going on here, exactly? How does one understand the intersection of the flags given to pipenv? What gets installed, and from where? This has been confusing to me and others, according to various threads on the internet ([1], [2], [3]).

### Explanation

Here is my understanding after really digging into this.

1. [`--system`](https://pipenv.pypa.io/en/latest/advanced/#deploying-system-dependencies): this flag means that dependencies will be installed to the system Python; no virtual environment will be created.
2. [`--deploy`](https://pipenv.pypa.io/en/latest/advanced/#using-pipenv-for-deployments): According to the documentation, "This will fail a build if the Pipfile.lock is out–of–date, instead of generating a new one." The important thing to note is that this step is really simple. Pipenv computes the hash of `Pipfile`. It then looks up the hash from `Pipfile.lock` and compares the two. If they are the same, then pipenv concludes that `Pipfile.lock` is up-to-date. That's the end of the impact of this flag.
    - If you look under the covers at `Pipfile.lock`, you can see it stores the hash of the `Pipfile` that it was generated from in the `_meta` section, like so:

        ```
        {
            "_meta": {
                "hash": {
                    "sha256": "dd9ca1ebdc0969e8187e275e07342277f4d7fc45b3fca7250b70f100891f94fa"
                },
        ```

3. `--ignore-pipfile`: This causes pipenv to, not surprisingly, ignore `Pipfile` and instead install what is directly specified in `Pipfile.lock`. However, the default behavior of this is to use the same mechanism as above to see whether the `Pipfile.lock` is out of date, and if so, to re-lock the `Pipfile.lock`. In conjunction with `--deploy`, this behavior is moot because that flag will already cause the install to fail if the files are out-of-date, and now there is no circumstance in which the lockfile will be re-locked.

So we have the following stylized algorithm for this install:

```text
if hash(Pipfile) != computed hash stored in Pipfile.lock
    fail
else
    for each specific dependency in Pipfile.lock
        install the dependency using the system Python
```

To fully understand the behavior of any code, there is often no substitute for reading the source directly. The function to understand is [do_init][4] in `pipenv/core.py` which is responsible for the behavior of `pipenv install` when no packages are specified at the command line. Note that both `do_install` and `do_sync` call `do_init` for the heavy lifting.

### Comparison with sync

Others have noted that this behavior is similar to `pipenv sync`. Previously, there was no support for `pipenv sync --system` (in a failure of symmetry) but a recent pipenv update did introduce this feature (PR [#4441](https://github.com/pypa/pipenv/pull/4441) included in pipenv [2020.11.4](https://pipenv.pypa.io/en/latest/changelog/#id11)).

So as of today, what is the difference between `pipenv sync --system` and `pipenv install --system --deploy --ignore-pipfile`? The differences appear to be that if the `Pipfile` exists, and if it is out-of-date, the install will fail in the latter case. If there is no Pipfile at all, then the `--deploy` flag will cause the `pipenv install` command to fail. So they are identical unless (1) Pipfile is missing or (2) Pipfile is out of date.

When would you want to use `pipenv sync` instead? Well, conversely, when you are concerned about `Pipfile` and `Pipfile.lock` being out-of-date? I'd say that any test or CI job should fail if they are out-of-date. You can imagine that one test checks whether they are out-of-date and fails if so, and all remaining test and build jobs use the `Pipfile.lock` only with `pipenv sync`. This seems like it could be simpler but I still think this is less robust as it introduces a dependency on this first test, and could result in errors where a job is failing actually due to the need to re-lock `Pipfile.lock` but is displaying mysterious behavior in the meantime. Whereas I might use `pipenv sync` in development if I have been making manual changes to my `Pipfile` but now want to restore my virtualenv to a previous change or ignore the changes to my `Pipfile`.

### The rest of the Dockerfile

Using pipenv and Docker together to create minimal images is something I've been working with a fair amount and plan to write another post about.

Some quick notes on the snippet above:

- You almost certainly want to copy `Pipfile` and `Pipfile.lock` to the image as a first step to take advantage of Docker's build caching.
- Make sure you upgrade pip before issuing any pip commands -- this will help you avoid the long tail of really frustrating installation issues.
- Use `pipenv --clear` to conveniently clear the cache of pip, pipenv, and pip-tools. You almost certainly want to clear these build caches if you want to produce small images. And this is easier than providing `pip install --no-cache-dir` with every invocation of pip, and knocks out all of the cache clearing in one place.
- By chaining all of the installation commands in one `RUN` line you avoid generating multiple layers, reducing the size of your final image.

[1]: https://github.com/pypa/pipenv/issues/3150
[2]: https://stackoverflow.com/questions/52922688/pipenv-sync-and-pipenv-install-system-ignore-pipfile-in-docker-environment
[3]: https://github.com/pypa/pipenv/issues/2227
[4]: https://github.com/pypa/pipenv/blob/dc377ef2d2b38b09bcf6f71ac7aa919e5ecad128/pipenv/core.py#L1199
