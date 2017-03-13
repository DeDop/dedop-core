#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEDOP_BIN="$( cd "${DIR}/../../.."  && pwd )"

open "${DEDOP_BIN}/dedop-shell.command"
