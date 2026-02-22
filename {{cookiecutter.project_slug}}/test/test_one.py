"""a first file for testing"""

import pandas as pd
import pytest
from conftest import sample_data


def test_addition(sample_data):
    """test addition"""
    assert sample_data["feature_a"].sum() == 15
    assert sample_data["target"].sum() == 2

def test_subtraction(sample_data):
    """test subtraction"""
    assert sample_data["feature_a"].sum() - sample_data["target"].sum() == 13

def test_multiplication(sample_data):
    """test multiplication"""
    assert sample_data["feature_a"].sum() * sample_data["target"].sum() == 30

def test_division(sample_data):
    """test division"""
    assert sample_data["feature_a"].sum() / sample_data["target"].sum() == 7.5  

def test_sample_data_fixture(sample_data):
    """test that the sample_data fixture returns expected DataFrame structure."""
    assert isinstance(sample_data, pd.DataFrame)
    assert len(sample_data) == 5
    assert sample_data.columns.tolist() == ["feature_a", "target"]
    assert sample_data["feature_a"].dtype == "int64"
    assert sample_data["target"].dtype == "int64"

def test_sample_data_fixture_values(sample_data):
    """test that the sample_data fixture returns expected values."""
    assert sample_data["feature_a"].sum() == 15
    assert sample_data["target"].sum() == 2 * 5 
    assert sample_data["feature_a"].mean() == 3
    assert sample_data["target"].mean() == 0.4
    assert sample_data["feature_a"].std() == 1.4142135623730951
    assert sample_data["target"].std() == 0.4472135954999579
    assert sample_data["feature_a"].min() == 1
    assert sample_data["target"].min() == 0
    assert sample_data["feature_a"].max() == 5
    assert sample_data["target"].max() == 1
