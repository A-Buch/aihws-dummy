#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anna Buch, TU Berlin"
__email__ = "anna.buch@tu-berlin.de"


from pathlib import Path
from glob import glob


def load_text_sources(data_dir):
    text_sources = glob(str(Path(data_dir, "*_cleaned.md" )))
    return text_sources
