#!/usr/bin/env python3

"""A script to get the list of installed atom packages, match it to the list of
expected packages, and install any that are missing."""
import subprocess
# pylint: disable=invalid-name
apm_list = subprocess.Popen(['apm', 'list', '-ib'], stdout=subprocess.PIPE, bufsize=-1)
results, _ = apm_list.communicate()

installed = set()
for spec in results.split(b'\n'):
    parts = spec.split(b"@")
    if parts[0]:
        installed.add(parts[0].decode('utf-8'))

# print("Installed pkgs:")
# for pkg in installed:
#     print(pkg)
#
wanted = set()
with open('my-packages.txt', 'r') as myin:
    for line in myin:
        wanted.add(line[:-1])

to_install = wanted - installed
if to_install:
    print("Installing {} missing packages.".format(len(to_install)))
    for pkg in wanted - installed:
        subprocess.call(['apm', 'install', pkg])
else:
    print("nothing to do!")

extras = installed - wanted
if extras:
    print("\nExtra packages installed locally:")
    for extra in extras:
        print(extra)
