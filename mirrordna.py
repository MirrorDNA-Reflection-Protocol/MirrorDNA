#!/usr/bin/env python3
"""
MirrorDNA CLI entry point.

This script provides a convenient entry point for the MirrorDNA CLI.
It delegates all functionality to the cli.mirrordna_cli module.

Usage:
    python mirrordna.py [command] [options]
    python mirrordna.py --help

Alternative usage:
    python -m cli.mirrordna_cli [command] [options]
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the CLI
from cli.mirrordna_cli import cli

if __name__ == '__main__':
    cli()
