#!/usr/bin/env bash

git submodule init
git submodule update

# To update Flex repo
# cd themes/Flex
# git fetch upstream --tags
# latest_tag=$(git describe --tags `git rev-list --tags --max-count=1`)
# git merge $latest_tag
