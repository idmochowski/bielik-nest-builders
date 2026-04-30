#!/usr/bin/env python3
"""Regenerate the embedded slide JSON in presentation.html from individual slide files.

Usage:
    cd slides
    python build.py
"""

import json
import os
import re
import sys

SLIDES_DIR = os.path.dirname(os.path.abspath(__file__))
PRESENTATION = os.path.join(SLIDES_DIR, "presentation.html")

START_MARKER = '<script type="application/json" id="embedded-slides-data">\n'
END_MARKER = '\n  </script>'


def main():
    # Collect all slide files
    slides = {}
    for f in sorted(os.listdir(SLIDES_DIR)):
        if f.startswith("slide-") and f.endswith(".html"):
            with open(os.path.join(SLIDES_DIR, f), "r") as fh:
                slides[f] = fh.read()

    if not slides:
        print("ERROR: No slide files found", file=sys.stderr)
        sys.exit(1)

    # Read presentation.html
    with open(PRESENTATION, "r") as fh:
        content = fh.read()

    # Locate the embedded JSON block
    start_idx = content.find(START_MARKER)
    if start_idx == -1:
        print("ERROR: Could not find embedded-slides-data marker", file=sys.stderr)
        sys.exit(1)

    end_search_from = start_idx + len(START_MARKER)
    end_idx = content.find(END_MARKER, end_search_from)
    if end_idx == -1:
        print("ERROR: Could not find end of embedded-slides-data block", file=sys.stderr)
        sys.exit(1)

    old_json = content[start_idx + len(START_MARKER):end_idx]
    new_json = json.dumps(slides, ensure_ascii=False)

    # Replace
    new_content = (
        content[: start_idx + len(START_MARKER)] + new_json + content[end_idx:]
    )

    with open(PRESENTATION, "w") as fh:
        fh.write(new_content)

    print(f"OK: {len(slides)} slides embedded ({len(old_json)} -> {len(new_json)} chars)")


if __name__ == "__main__":
    main()
