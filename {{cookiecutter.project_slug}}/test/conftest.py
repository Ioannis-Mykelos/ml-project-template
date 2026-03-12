"""conftest.py for testing"""

import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    """Returns a tiny 5-row dataframe for testing."""
    return pd.DataFrame({"feature_a": [1, 2, 3, 4, 5], "target": [0, 1, 0, 1, 0]})
