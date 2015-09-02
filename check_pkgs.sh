#!/usr/bin/env dash

TMPFILE=$(mktemp)
trap "rm $TMPFILE" EXIT

apm list --bare --installed | cut -d@ -f1 | sort > ${TMPFILE}
XTRA_PKGS=$(diff -w my-packages.txt ${TMPFILE} | grep '^>' | cut -c 2-)
if [ ! -z "${XTRA_PKGS}" ]; then
    echo "Packages installed not in my-packages.txt: ${XTRA_PKGS}"
fi
MSG_PKGS=$(diff -w my-packages.txt ${TMPFILE} | grep '^<' | cut -c 2-)
if [ ! -z "${MSG_PKGS}" ]; then
    echo "Packages expected but not found: ${MSG_PKGS}"
fi
