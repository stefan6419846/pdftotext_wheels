## pdftotext Wheels

This repository provides an automated way to build up-to-date wheels for the [*pdftotext*](https://github.com/jalan/pdftotext) Python package. At the moment, this is mostly targeted at Linux and GitHub Actions, but I am open for further enhancements.

### Structure

`.github` contains the GitHub Actions workflow files for building the wheels and checking for new releases. The remaining files are utilized within them to keep the workflows small enough and allow for using a different CI system to perform the relevant build actions.

The current utility files:

  * `check_for_new_package_versions.py`: Python script used to check for new package releases in an automated manner.
  * `prepare.sh`: Bash script to prepare the actual build.
  * `replace_version.py`: Python script to add the Poppler version to the package version. Used by `prepare.sh`.

### Development

All Python code inside this repository should be checked with `flake8 --max-line-length 160 .` (with the `pep8-naming` plugin enabled), all Bash code with `shellcheck prepare.sh`.

### License

All the scripts and the toolchain inside this repository are subject to the terms of the MIT license.

Please note that this does not hold true for the generated wheel files. While the Python wrapper files are subject to the MIT license as well, they link against some more shared objects before or during installation. With the manylinux approach inside this repository, all non-standard shared objects are part of the wheel itself. For this reason, the wheels probably should be considered to be under the terms of the GPL (even when the Python package data states something different), as is [Poppler](https://gitlab.freedesktop.org/poppler/poppler#history-and-gpl-licensing) itself.

Nevertheless, this should not be considered legal advice and you should review all dependencies and ensure the corresponding actions before actually using/distributing it. Consult an Attorney if required.
