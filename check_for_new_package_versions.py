#!/usr/bin/env python

import sys
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup


FREETYPE_URL = "https://gitlab.freedesktop.org/freetype/freetype/-/tags?format=atom"
POPPLER_URL = "https://gitlab.freedesktop.org/poppler/poppler/-/tags?format=atom"
PDFTOTEXT_URL = "https://github.com/jalan/pdftotext/releases.atom"


def fetch_latest_freetype_release():
    soup = BeautifulSoup(requests.get(FREETYPE_URL).content, features="xml")
    entry = soup.find("entry")
    version = entry.find("title").text

    assert version, version
    assert version.startswith('VER-'), version
    version = version.split('VER-')[1]
    assert version, version
    version = version.replace('-', '.')
    return version


def fetch_latest_poppler_release():
    soup = BeautifulSoup(requests.get(POPPLER_URL).content, features="xml")
    entry = soup.find("entry")
    version = entry.find("summary").text

    assert version, version
    return version


def fetch_latest_pdftotext_release():
    soup = BeautifulSoup(requests.get(PDFTOTEXT_URL).content, features="xml")
    entry = soup.find("entry")
    version = entry.find("title").text

    assert version, version
    return version


def get_all_workflow_files():
    return Path(".github/workflows").glob("*.yml")


def check_workflow(workflow_path, latest_freetype_release, latest_poppler_release, latest_pdftotext_release):
    with open(workflow_path) as fd:
        content = yaml.safe_load(fd)
    env = content.get("env")
    if not env:
        return True

    def check(name, latest_version, identifier):
        current_version = env.get(name)
        if not current_version:
            return True
        if current_version != latest_version:
            print(f"{identifier} version {latest_version} is available for {workflow_path} (currently: {current_version}).")
            return False
        return True

    are_valid = check(name="FREETYPE_VERSION", latest_version=latest_freetype_release, identifier="FreeType")
    are_valid &= check(name="POPPLER_VERSION", latest_version=latest_poppler_release, identifier="Poppler")
    are_valid &= check(name="PDFTOTEXT_VERSION", latest_version=latest_pdftotext_release, identifier="pdftotext")
    return are_valid


def main():
    latest_freetype_release = fetch_latest_freetype_release()
    latest_poppler_release = fetch_latest_poppler_release()
    latest_pdftotext_release = fetch_latest_pdftotext_release()
    print(f"Latest versions: FreeType {latest_freetype_release}, Poppler {latest_poppler_release}, pdftotext {latest_pdftotext_release}")
    are_valid = True
    for workflow_path in get_all_workflow_files():
        are_valid &= check_workflow(
            workflow_path=workflow_path,
            latest_freetype_release=latest_freetype_release,
            latest_poppler_release=latest_poppler_release,
            latest_pdftotext_release=latest_pdftotext_release,
        )
    if not are_valid:
        sys.exit(5)


if __name__ == "__main__":
    main()
