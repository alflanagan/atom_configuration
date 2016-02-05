#!/usr/bin/env python3
# vim: sw=4:ts=4:expandtab
"""A script to get the list of installed atom packages, match it to the list of
expected packages, and install any that are missing."""

import subprocess
import argparse
# pylint: disable=invalid-name

# a dict of packages installed because they are dependencies of a package in my-packages.txt
# better but difficult: get deps from package.json files
DEPENDENCIES = {}


def get_args():
    """Parses command-line arguments, returns namespace with values."""
    parser = argparse.ArgumentParser(
        description="Report or install apm packages according to my-packages.txt")
    parser.add_argument('--install', action='store_true',
                        help="Actually install missing packages (default: report only).")
    parser.add_argument('--beta', action='store_true',
                        help="Act on beta-channel atom version.")
    return parser.parse_args()


def get_installed_pkgs(apm_prog):
    """Uses `apm_prog` to get list of currently installed packages, return as a set."""
    apm_list = subprocess.Popen([apm_prog, 'list', '-ib'], stdout=subprocess.PIPE, bufsize=-1)
    results, _ = apm_list.communicate()

    installed = set()
    for spec in results.split(b'\n'):
        parts = spec.split(b"@")
        if parts[0]:
            installed.add(parts[0].decode('utf-8'))

    # remove dependencies from list
    for key in DEPENDENCIES:
        if key in installed:
            for pkg in DEPENDENCIES[key]:
                installed.discard(pkg)

    return installed


def get_wanted_packages():
    """Reads the list of desired packages from my-packages.txt file, returns a set."""
    wanted = set()
    with open('my-packages.txt', 'r') as myin:
        for line in myin:
            wanted.add(line[:-1])
    return wanted


def install_missing(apm_prog, wanted, installed):
    """Calls `apm_prog` to install each package present in set `wanted` but not in set `installed`.

    """
    to_install = wanted - installed
    if to_install:
        print("Installing {} missing packages.".format(len(to_install)))
        for pkg in wanted - installed:
            subprocess.call([apm_prog, 'install', pkg])
    else:
        print("nothing to do!")


def report_missing_packages(wanted, installed):
    """Lists to stdout packages in set `wanted` which are not in set `installed`."""
    missing = wanted - installed
    if missing:
        print("Expected packages not installed:")
        for missed in missing:
            print(missed)


def report_extra_packages(wanted, installed):
    """Lists to stdout packages in set `installed` which are not in set `wanted`."""
    extras = installed - wanted
    if extras:
        print("\nExtra packages installed locally:")
        for extra in extras:
            print(extra)


def main():
    """Driver function."""
    args = get_args()
    apm = 'apm-beta' if args.beta else 'apm'
    installed = get_installed_pkgs(apm)
    wanted = get_wanted_packages()
    report_missing_packages(wanted, installed)
    report_extra_packages(wanted, installed)
    if args.install:
        install_missing(apm, wanted, installed)


if __name__ == '__main__':
    main()
