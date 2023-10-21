#!/usr/bin/env bash

# Create build directory.
mkdir build
cd build || exit 1
build_dir=$( pwd )

# Download FreeType and unpack it.
wget "https://download.savannah.gnu.org/releases/freetype/freetype-${FREETYPE_VERSION}.tar.gz" -O freetype.tar.gz
tar -xvf freetype.tar.gz

# Build FreeType.
cd freetype-* || exit 1
./configure
make
make install

cd "${build_dir}" || exit 1

# Download poppler and unpack it.
wget "https://gitlab.freedesktop.org/poppler/poppler/-/archive/poppler-${POPPLER_VERSION}/poppler-poppler-${POPPLER_VERSION}.tar.gz" -O poppler.tar.gz
tar -xvf poppler.tar.gz

# Build poppler.
cd poppler* || exit 1
mkdir build
cd build || exit 1
cmake -DENABLE_BOOST=OFF -DENABLE_GPGME=OFF -DENABLE_LIBTIFF=OFF ..
make
make install

cd "${build_dir}" || exit 1

# Get package source. Unpack to this directory.
wget "https://github.com/jalan/pdftotext/archive/${PDFTOTEXT_VERSION}.tar.gz" -O pdftotext.tar.gz
tar --strip-components=1 -xvzf pdftotext.tar.gz

# Adapt version.
echo "Adding poppler version to package version ..."
/opt/python/cp310-cp310/bin/python ../replace_version.py "$(realpath setup.py)"
