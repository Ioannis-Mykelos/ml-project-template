"""Scoring pipeline template — compatible with Azure ML and Databricks."""

import os

import mlflow.pyfunc
import pandas as pd


def scoring_pipeline(
    dataframe: pd.DataFrame, model: mlflow.pyfunc.PyFuncModel
) -> pd.DataFrame:
    """
    Scoring pipeline template compatible with Azure ML and Databricks.

    Arguments:
    ----------
    - dataframe (pd.DataFrame) : Input data to be scored
    - model (mlflow.pyfunc.PyFuncModel) : Trained ML model for scoring

    Returns:
    -------
    - data (pd.DataFrame)      : The scored data.
    """
    data = dataframe.copy()

    # Make predictions
    predictions = model.predict(data)

    return pd.DataFrame(predictions, columns=["prediction"])


if __name__ == "__main__":

    with mlflow.start_run(run_name="scoring_run", nested=True):
        print("Loading Data ...")
        file_path = os.getenv("DATA_PATH_SCORING")
        if file_path is None:
            raise ValueError("DATA_PATH_SCORING environment variable is not set")
        the_data = (
            pd.read_parquet(path=file_path)
            if file_path.endswith(".parquet")
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

        # Run the scoring pipeline
        print("Scoring ...")
        model = mlflow.pyfunc.load_model("models:/churn_model/Production")
        scored = scoring_pipeline(dataframe=the_data, model=model)
        print("Scoring completed ✓")

        # Log output data metrics
        output_schema_info = {
            "shape": list(scored.shape),
            "columns": list(scored.columns),
            "dtypes": scored.dtypes.astype(str).to_dict(),
        }
        mlflow.log_dict(output_schema_info, "output_dataframe_info.json")
