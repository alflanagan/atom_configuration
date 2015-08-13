#!/usr/bin/env bash

#TODO: compare apm list with my-packages.txt, only install missing
# which apm should do, but oh well
apm install --packages-file my-packages.txt
TMPFILE=$(mktemp)
apm list --bare --installed | cut -d@ -f1 | sort > ${TMPFILE}
PKGS=$(diff -w my-packages.txt ${TMPFILE} | grep '^>' | cut -c 2-)
if [[ ! -z ${PKGS} ]]; then
    echo "Packages installed not in my-packages.txt: ${PKGS}"
fi
rm ${TMPFILE}
