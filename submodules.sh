#!/usr/bin/env bash

# themes repo and render_math plugin
git submodule init
git submodule update

# Another step, for themes
cd themes
git submodule add Flex
git submodule init
git submodule update
cd ..
