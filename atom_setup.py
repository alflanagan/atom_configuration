#!/usr/bin/env python3
# vim: sw=4:ts=4:expandtab
"""Compare installed Atom packages to a list of expected packages.

Optionally installs missing packages.
"""

import subprocess
import argparse
import platform
import os

# pylint: disable=invalid-name

# a dict of packages installed because they are dependencies of a package in my-packages.txt
# better but difficult: get deps from package.json files
DEPENDENCIES = {
    "linter": {"linter-ui-default"},
    "linter-ui-default": {"intentions", "busy-signal"},
    "pythonic-atom": {
        "linter", "linter-ui-default", "linter-pycodestyle", "minimap",
        "minimap-linter", "MagicPython", "python-tools", "python-yapf",
        "autocomplete-python", "hyperclick", "script", "atom-isort"
    }
}


def get_args():
    """Parse command-line arguments, return namespace with values."""
    desc = "Report or install apm packages according to my-packages.txt"
    if platform.system() == "Windows":
        desc = "Report or install apm packages according to my-windows-packages.txt"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--install',
        action='store_true',
        help="Actually install missing packages (default: report only).")
    parser.add_argument(
        '--beta',
        action='store_true',
        help="Act on beta-channel atom version.")
    return parser.parse_args()


def get_installed_pkgs(apm_prog):
    """Use `apm_prog` to get list of currently installed packages, return as a set."""
    apm_list = subprocess.Popen(
        [apm_prog, 'list', '-ib'], stdout=subprocess.PIPE, bufsize=-1)
    results, _ = apm_list.communicate()

    installed = set()
    for spec in results.split(b'\n'):
        parts = spec.split(b"@")
        if parts[0]:
            installed.add(parts[0].decode('utf-8'))

    # remove dependencies from list
    for key in DEPENDENCIES:
        for pkg in DEPENDENCIES[key]:
            installed.discard(pkg)

    return installed


def get_wanted_packages():
    """Read the list of desired packages from my-packages.txt file, return a set."""
    wanted = set()
    fname = "my-packages.txt"
    if platform.system() == "Windows":
        fname = "my-windows-packages.txt"
    with open(fname, 'r') as myin:
        for line in myin:
            pkgname = line[:-1]
            wanted.add(pkgname)
            if pkgname in DEPENDENCIES:
                for pkg in DEPENDENCIES[pkgname]:
                    wanted.add(pkgname)
    return wanted


def install_missing(apm_prog, wanted, installed):
    """Install each package present in set `wanted` but not in set `installed`."""
    to_install = wanted - installed
    if to_install:
        print("Installing {} missing packages.".format(len(to_install)))
        for pkg in wanted - installed:
            subprocess.call([apm_prog, 'install', pkg])
    else:
        print("nothing to do!")


def report_missing_packages(wanted, installed):
    """List to stdout packages in set `wanted` which are not in set `installed`."""
    missing = wanted - installed
    if missing:
        print("Expected packages not installed:")
        for missed in missing:
            print(missed)


def report_extra_packages(wanted, installed):
    """List to stdout packages in set `installed` which are not in set `wanted`."""
    extras = installed - wanted
    if extras:
        print("\nExtra packages installed locally:")
        for extra in extras:
            print(extra)


def main():
    """Driver function."""
    args = get_args()
    apm = 'apm-beta' if args.beta else 'apm'
    if platform.system() == 'Windows':
        apm = os.path.join(os.getenv("LOCALAPPDATA"), r'atom\bin\apm.cmd')
    installed = get_installed_pkgs(apm)
    wanted = get_wanted_packages()
    report_missing_packages(wanted, installed)
    report_extra_packages(wanted, installed)
    if args.install:
        install_missing(apm, wanted, installed)


if __name__ == '__main__':
    main()
