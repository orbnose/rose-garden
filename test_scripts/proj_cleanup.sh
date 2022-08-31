#!/bin/bash

#deactivate django venv
deactivate

#get the rosegarden test environment parent directory
parentdirfile="/tmp/rg_test_parent_dir.dat"
if [ ! -f "$parentdirfile" ]; then
    echo "The rosegarden test environment parent directory could not be found."
    return
else
    parentdir=$(cat "$parentdirfile")
fi

#clean up
rm -r rgTestLibrary
rm $parentdirfile
