"""monitoring pipeline"""

import argparse
import os

import numpy as np
import pandas as pd
from azureml.core import Run
from scoring import scoring_pipeline


def monitoring_pipeline(data: pd.DataFrame, model, scoring_pipeline=scoring_pipeline):
    """
    Monitoring pipeline

    Arguments:
    ----------
    - data    : Input data to be cleaned

    Returns:
    -------
    - data  : The processed music data.
    """
    data_ = data.copy()
    new_model = model
    pipe = scoring_pipeline
    return data_, new_model, pipe


def parse_args():
    """parse the arguments passed to the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str, help="input datapath argument")
    parser.add_argument("--input_model", type=str, help="input datapath argument")
    parser.add_argument("--output_data", type=str, help="output datapath argument")
    parser.add_argument(
        "--filename", type=str, help="Filename to be processed", default="default_data"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # Parse args and get the parameters
    the_args = parse_args()
    run = Run.get_context()

    print("Loading Data ...")
    file_path = os.path.join(the_args.input_data, the_args.filename)
    the_data = pd.read_csv(file_path, engine="python")
    print("Data loaded ✓")

    print("Loading Model ...")
    file_path = os.path.join(the_args.input_model)
    the_model = "model"
    print("Data loaded ✓")

    print("Monitoring ...")
    pre_processed = monitoring_pipeline(
        data=the_data, model=the_model, scoring_pipeline=scoring_pipeline
    )
    print("Monitoring ✓")

    # Path
    print("Saving data ...")
    FILE_PRED = (
        f"{the_args.filename.replace('.csv', '').replace('.parquet', '')}.parquet"
    )
    path = the_args.output_data
    os.makedirs(path, exist_ok=True)
    pre_processed.to_parquet(path=os.path.join(path, FILE_PRED))
    print("Data saved ✓")

    # End run
    run.complete()
