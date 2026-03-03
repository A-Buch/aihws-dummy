#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import tempfile

sys.path.append("../../")
import src.data_handler as d 


# test a simple edge-case for the function load_text_sources(). 
# load_text_sources() is used to load the text sources for our LLM mining pipeline. 
# We want to make sure that only files with the correct naming convention are loaded, and that other files are ignored.
def test_load_text_sources():

    # create a temporary directory and files for testing
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some test files
        test_files = [
            "file1_cleaned.md",
            "file2_cleaned.md",
            "file3.md",  # this should be ignored
            "file3_cleaned.txt",  # this should be ignored
            "file3_cleaned.",  # this should be ignored
        ]
        for filename in test_files:
            with open(os.path.join(tmpdirname, filename), "w") as f:
                f.write("test content")

        # call the function to test
        result = d.load_text_sources(tmpdirname)

        # check that only the correct files are returned
        expected_files = [
            os.path.join(tmpdirname, "file1_cleaned.md"),
            os.path.join(tmpdirname, "file2_cleaned.md"),
        ]
        assert set(result) == set(expected_files)