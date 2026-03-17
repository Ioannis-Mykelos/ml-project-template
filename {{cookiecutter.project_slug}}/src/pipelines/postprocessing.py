"""Postprocessing pipeline template — compatible with Azure ML and Databricks."""

import os

import mlflow
import pandas as pd


def postprocessing_pipeline(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Postprocessing pipeline template compatible with Azure ML and Databricks.

    Arguments:
    ----------
    - dataframe (pd.DataFrame) : Input data to be postprocessed.

    Returns:
    -------
    - data (pd.DataFrame)      : The postprocessed data.
    """
    data = dataframe.copy()

    # TODO: Add your postprocessing logic here

    return data


if __name__ == "__main__":

    with mlflow.start_run():
        print("Loading Data ...")
        file_path = os.getenv("DATA_PATH_POSTPROCESSING")
        if file_path is None:
            raise ValueError("DATA_PATH_POSTPROCESSING environment variable is not set")
        the_data = (
            pd.read_parquet(path=file_path)
            if ".parquet" in file_path
            else pd.read_csv(filepath_or_buffer=file_path, engine="python")
        )
        print("Data loaded ✓")

        # Log input data metrics
        input_schema_info = {
            "shape": list(the_data.shape),
            "columns": list(the_data.columns),
            "dtypes": the_data.dtypes.astype(str).to_dict(),
        }
        mlflow.log_dict(input_schema_info, "input_dataframe_info.json")

        # Run the postprocessing pipeline
        print("Postprocessing ...")
        processed = postprocessing_pipeline(dataframe=the_data)
        print("Postprocessing completed ✓")

        # Log output data metrics
        output_schema_info = {
            "shape": list(processed.shape),
            "columns": list(processed.columns),
            "dtypes": processed.dtypes.astype(str).to_dict(),
        }
        mlflow.log_dict(output_schema_info, "output_dataframe_info.json")
