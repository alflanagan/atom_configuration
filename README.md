# Atom Configuration

Scripts/source for configuration of the atom editor (https://atom.io)

Given my love/hate relationship with [GNU Emacs](https://www.gnu.org/software/emacs/), I've been looking for something with the power and programmability of Emacs without all the historical cruft Emacs just can't seem to move beyond. Github's [Atom editor](https://atom.io) is the closest thing I've found, and seems to be getting the kind of popular attention needed to develop a good selection of add-on packages.

On the minus side, the scripting language is Javascript. The language is improving, but it's not Lisp.

I was including a list of the add-on packages I use with descriptions, but it's too darn long and changes too often.

Needed: setup to store portable configuration settings in a file, merge them with local config.json.

## Files of Interest

* `atom_setup.py` - Allows me to install a list of packages automatically, and tag packages to be installed only if I specify the tag on the command line. Run to see the available commands.
* `atom-setup.ps1` - A port of `atom_setup.py` to Powershell script. Almost works.
* `config.template.cson` - A set of configuration settings that are "recommended". So far, the only (safe) way to activate them is to copy them to the actual `~/.atom/config.cson` file.
* `init.coffee` - my setup file
* `keymap.cson` - my keyboard mappings. Many are set up to arbitrate disputes between packages that want to use the same keys.
* `my-packages.txt` - master list of packages which i would like installed on whatever system I'm using.
* `my-windows-packages.txt` - same as `my-packages.txt` except for ommision of a few packages not needed in a Windows environment. TODO: merge package files, with some sort of tag for 'everywhere but Windows systems'.
* `toolbar.cson` - settings for the flex tool bar, provides buttons for some commands I use a lot but don't bother remembering the keys for.
* `windows_setup.md` - some notes on setting up automatic configuration on Windows systems, because of course they're different.
