#!/bin/bash

DEDOP_BIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEDOP_HOME="$( cd "${DEDOP_BIN}/.."  && pwd )"

reset
echo
echo Welcome to the DeDop Shell. Type "dedop -h" to get help.
echo

source "${DEDOP_BIN}/activate" "${DEDOP_HOME}"
unset PROMPT_COMMAND
export PS1="\[\033[1;34m\](DeDop)\[\033[0m\] $ "
exec /bin/bash --norc -i
