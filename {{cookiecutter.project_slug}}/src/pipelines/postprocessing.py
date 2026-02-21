"""postprocessing pipeline"""

import argparse
import os

import pandas as pd
from azureml.core import Run


def postprocessing_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    """
    Post-processing pipeline

    Arguments:
    ----------
    - df   : The initial dataframe

    Returns:
    -------
    - data : The post-processed dataframe.
    """

    data_ = data.copy()

    return data_


def parse_args():
    """parse the arguments passed to the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str, help="input datapath argument")
    parser.add_argument("--output_data", type=str, help="output datapath argument")
    parser.add_argument(
        "--filename",
        type=str,
        help="Filename to be processed",
        default="default_data",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # Parse args and get the parameters
    the_args = parse_args()
    run = Run.get_context()

    print("Loading Data ...")
    file_path = os.path.join(the_args.input_data, the_args.filename)
    the_data = (
        pd.read_parquet(file_path)
        if ".parquet" in file_path
        else pd.read_csv(file_path)
    )
    print("Data loaded ✓")

    print("Post-processing...")
    post_processed = postprocessing_pipeline(data=the_data)
    print("Post-processing ✓")

    # Path
    print("Saving data ...")
    FILE_PRED = (
        f"{the_args.filename.replace('.csv', '').replace('.parquet', '')}.parquet"
    )
    path = the_args.output_data
    os.makedirs(path, exist_ok=True)
    post_processed.to_parquet(path=os.path.join(path, FILE_PRED))
    print("Data saved ✓")

    # End run
    run.complete()
