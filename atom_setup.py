#!/usr/bin/env python3
# vim:ts=4:sw=4:expandtab:
"""A script to get the list of installed atom packages, match it to the list of
expected packages, and install any that are missing."""

import subprocess
import argparse
# pylint: disable=invalid-name

# a dict of packages installed because they are dependencies of a package in my-packages.txt
# better but difficult: get deps from package.json files
DEPENDENCIES = {"nuclide-installer":
                ("nuclide-clang-atom", "nuclide-blame-ui", "nuclide-diagnostics-ui",
                 "nuclide-debugger-atom", "nuclide-debugger-hhvm", "nuclide-arcanist",
                 "nuclide-diagnostics-store", "nuclide-debugger-lldb", "nuclide-blame-provider-hg",
                 "nuclide-diff-view", "nuclide-blame", "nuclide-code-format", "nuclide-buck-files")}


def get_args():
    """Parses command-line arguments, returns namespace with values."""
    parser = argparse.ArgumentParser(
        description="Report or install apm packages according to my-packages.txt")
    parser.add_argument('--install', action='store_true',
                        help="Actually install missing packages (default: report only).")
    return parser.parse_args()


def get_installed_pkgs():
    apm_list = subprocess.Popen(['apm', 'list', '-ib'], stdout=subprocess.PIPE, bufsize=-1)
    results, _ = apm_list.communicate()

    installed = set()
    for spec in results.split(b'\n'):
        parts = spec.split(b"@")
        if parts[0]:
            installed.add(parts[0].decode('utf-8'))
    return installed


def get_wanted_packages():
    wanted = set()
    with open('my-packages.txt', 'r') as myin:
        for line in myin:
            wanted.add(line[:-1])
    for key in DEPENDENCIES:
        if key in wanted:
            for pkg_name in DEPENDENCIES[key]:
                wanted.add(pkg_name)
    return wanted


def install_missing(wanted, installed):
    to_install = wanted - installed
    if to_install:
        print("Installing {} missing packages.".format(len(to_install)))
        for pkg in wanted - installed:
            subprocess.call(['apm', 'install', pkg])
    else:
        print("nothing to do!")


def report_missing_packages(wanted, installed):
    missing = wanted - installed
    if missing:
        print("Expected packages not installed:")
        for missed in missing:
            print(missed)


def report_extra_packages(wanted, installed):
    extras = installed - wanted
    if extras:
        print("\nExtra packages installed locally:")
        for extra in extras:
            print(extra)


def main():
    args = get_args()
    installed = get_installed_pkgs()
    wanted = get_wanted_packages()
    report_missing_packages(wanted, installed)
    report_extra_packages(wanted, installed)
    if args.install:
        install_missing(wanted, installed)


if __name__ == '__main__':
    main()
