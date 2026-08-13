# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.

import re
from collections import Counter
from pathlib import Path

import pytest


def test_jenkinsfile_environment_no_duplicate_tn_cache_vars():
    """Fail if any *_TN_CACHE variable is assigned twice in the Jenkinsfile environment block."""
    jenkinsfile = Path(__file__).parents[2] / "Jenkinsfile"
    assert jenkinsfile.exists(), f"Jenkinsfile not found at {jenkinsfile}"

    content = jenkinsfile.read_text()
    env_match = re.search(r"environment\s*\{([^}]*)\}", content, re.DOTALL)
    assert env_match, "Could not find environment block in Jenkinsfile"
    env_block = env_match.group(1)

    # Find every TN_CACHE variable assignment in the environment block.
    assignments = re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)_TN_CACHE\s*=", env_block, re.MULTILINE)
    duplicates = [var for var, count in Counter(assignments).items() if count > 1]

    assert not duplicates, (
        f"Duplicate *_TN_CACHE definitions in Jenkinsfile environment block: {duplicates}"
