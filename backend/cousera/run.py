#!/usr/bin/env python3
"""
Coursera Profile Scraper Runner

This is a simple wrapper script that runs the Coursera Profile Scraper in interactive mode,
prompting the user for a Coursera profile URL.
"""

# import sys
# from interactive_scraper import main

# if __name__ == "__main__":
#     sys.exit(main())

import sys
from .interactive_scraper import main


def run_interactive():
    return main()

if __name__ == "__main__":
    sys.exit(run_interactive())
