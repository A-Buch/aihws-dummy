#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anna Buch, TU Berlin"
__email__ = "anna.buch@tu-berlin.de"


from pathlib import Path
from glob import glob
import numpy as np
import pandas as pd



def load_text_sources(data_dir: Path) -> list:

    text_sources = glob(str(Path(data_dir, "*_cleaned.md")))
    
    return text_sources


def replace_missing_values(df:pd.DataFrame) -> pd.DataFrame:
    df = df.replace(
        {-999: np.nan, "-999": np.nan, None: np.nan}
    )
    return df
