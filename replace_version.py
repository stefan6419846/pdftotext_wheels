#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path


def main(path: str):
    path = Path(path)
    content = path.read_bytes()
    matches = list(re.finditer(br'version=\"(?P<version>.*)\",\n', content))
    assert len(matches) == 1, matches
    match = matches[0]
    index_start, index_end = match.start(), match.end()
    version = match.group('version').decode('utf-8')
    poppler_version = os.getenv('POPPLER_VERSION', None)
    assert poppler_version, 'POPPLER_VERSION is empty'
    # Adhere to PEP440.
    new_content = (
        content[:index_start] +
        f'version="{version}+poppler{poppler_version}",\n'.encode('utf-8') +
        content[index_end:]
    )
    path.write_bytes(new_content)


if __name__ == '__main__':
    main(path=sys.argv[1])
