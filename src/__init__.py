"""
HWP Parser Module

A Docker-based HWP (Hangul Word Processor) file parser that extracts
text content, tables, and exports to various formats.
"""

from .hwp_parser import (
    extract_text,
    extract_text_to_stdout,
    normalize_text,
    parse_pipe_tables,
    export_to_json,
)

__version__ = "0.1.0"
__all__ = [
    "extract_text",
    "extract_text_to_stdout",
    "normalize_text",
    "parse_pipe_tables",
    "export_to_json",
]
