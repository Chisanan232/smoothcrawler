#!/usr/bin/env bash

set -ex
runtime_os=$1

declare -a init_tests
declare -a components_tests
declare -a appintegration_tests

getalltests() {
    declare -a testpatharray=( $(ls -F $1 | grep -v '/$' | grep -v '__init__.py' | grep -v 'test_config.py' | grep -v -E '^_[a-z_]{1,64}.py' | grep -v '__pycache__'))

    declare -a alltestpaths
    for (( i = 0; i < ${#testpatharray[@]}; i++ )) ; do
        alltestpaths[$i]=$1${testpatharray[$i]}
    done

    if echo $1 | grep -q "components";
    then
        components_tests=${alltestpaths[@]}
    elif echo $1 | grep -q "appintegration";
    then
        appintegration_tests=${alltestpaths[@]}
    else
        init_tests=${alltestpaths[@]}
    fi
}

init_path=test/unit_test/
components_path=test/unit_test/components/
appintegration_path=test/unit_test/appintegration/

getalltests $init_path
getalltests $components_path
getalltests $appintegration_path

dest=( "${init_tests[@]} ${components_tests[@]} ${appintegration_tests[@]}" )


if echo $runtime_os | grep -q "windows";
then
    printf "${dest[@]}" | jq -R .
elif echo $runtime_os | grep -q "unix";
then
    printf '%s\n' "${dest[@]}" | jq -R . | jq -cs .
else
    printf 'error' | jq -R .
fi
