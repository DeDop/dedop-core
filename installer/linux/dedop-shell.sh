#!/bin/bash

DEDOP_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo
echo Welcome to the DeDop Shell. Type "dedop -h" to get help.
echo

source "${DEDOP_HOME}/python/bin/activate" "${DEDOP_HOME}/python"
exec /bin/bash --norc -i

