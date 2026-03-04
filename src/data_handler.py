#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anna Buch, TU Berlin"
__email__ = "anna.buch@tu-berlin.de"


from pathlib import Path
from glob import glob

def load_text_sources(data_dir):
    
    text_sources = glob(str(Path(data_dir, ["*_cleaned.md", "*_cleaned.txt"])))
    
    return text_sources


def get_document_text(text_sources: list):
    for text_source in text_sources:
        with open(text_source, "r") as f:
            text = f.read()
            print(f"Preprocessing text source {text} ...")
