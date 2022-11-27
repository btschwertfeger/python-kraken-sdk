#!/bin/bash

# remove trailing whitespaces
# find $1 -type f -name '*.py' -exec sed -i '' 's/[[:space:]]*$//' {} \+

# run pylint
pylint --rcfile=.pylintrc $1 