#!/usr/bin/env bash

# themes repo and render_math plugin
git submodule init
git submodule update

# Another step, for themes
cd themes
git submodule init Flex
git submodule update
cd ..
