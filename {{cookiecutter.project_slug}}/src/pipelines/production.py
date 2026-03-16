""""This is the production pipeline. It should be used to run the model in production. It should be as simple as possible and only contain the necessary steps to run the model in production. The pipeline should be run on a regular basis (e.g. daily, weekly, monthly) to generate predictions for the next period."""

import os

import mlflow
import pandas as pd
from preprocessing import preprocessing_pipeline
from scoring import scoring_pipeline

if __name__ == "__main__":

    with mlflow.start_run():
        print("Loading Data ...")
        file_path = os.getenv("DATA_PATH")
        if file_path is None:
            raise ValueError("DATA_PATH environment variable is not set")
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

        # Run the preprocessing pipeline
        print("Preprocessing ...")
        processed = preprocessing_pipeline(dataframe=the_data)
        print("Preprocessing completed ✓")

        # Log output data metrics
        output_schema_info = {
            "shape": list(processed.shape),
            "columns": list(processed.columns),
            "dtypes": processed.dtypes.astype(str).to_dict(),
        }
        mlflow.log_dict(output_schema_info, "preprocessed_dataframe_info.json")

        # Run the scoring pipeline
        print("Scoring ...")
        scored = scoring_pipeline(data=processed)
        print("Scoring completed ✓")

        # Log output data metrics
        scored_schema_info = {
            "shape": list(scored.shape),
            "columns": list(scored.columns),
            "dtypes": scored.dtypes.astype(str).to_dict(),
        }
        mlflow.log_dict(scored_schema_info, "scored_dataframe_info.json")
