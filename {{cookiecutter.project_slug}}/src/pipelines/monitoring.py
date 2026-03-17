"""Monitoring pipeline template for ML projects"""

import os
from typing import Protocol, Tuple

import mlflow
import mlflow.pyfunc
import pandas as pd
from dotenv import load_dotenv
from scoring import scoring_pipeline

load_dotenv()


class ScoringPipeline(Protocol):
    def __call__(
        self,
        dataframe: pd.DataFrame,
        model: mlflow.pyfunc.PyFuncModel,
    ) -> pd.DataFrame:
        pass


def monitoring_pipeline(
    dataframe: pd.DataFrame,
    model: mlflow.pyfunc.PyFuncModel,
    pipeline: ScoringPipeline,
) -> Tuple[pd.DataFrame, mlflow.pyfunc.PyFuncModel, pd.DataFrame]:
    """
    Monitoring pipeline template for ML projects.

    Arguments:
    ----------
    - dataframe (pd.DataFrame)              : Input data to be processed
    - model     (mlflow.pyfunc.PyFuncModel) : Trained model for scoring
    - pipeline (ScoringPipeline)            : Scoring pipeline function to be applied on the data

    Returns:
    -------
    - dataframe (pd.DataFrame)              : The processed data.
    - model     (mlflow.pyfunc.PyFuncModel) : The model used for scoring.
    - pipeline (pd.DataFrame)               : The output of the scoring pipeline.
    """
    data = dataframe.copy()
    pipe = pipeline(dataframe=data, model=model)
    return data, model, pipe


if __name__ == "__main__":

    with mlflow.start_run(run_name="monitoring_run"):
        print("Loading Data ...")
        file_path = os.getenv("DATA_PATH_MONITORING")
        if file_path is None:
            raise ValueError("DATA_PATH_MONITORING environment variable is not set")
        the_data = (
            pd.read_parquet(path=file_path)
            if file_path.endswith(".parquet")
            else pd.read_csv(filepath_or_buffer=file_path, engine="python")
        )
        print("Data loaded ✓")

        print("Loading Model ...")
        the_model = mlflow.pyfunc.load_model("models:/churn_model/Production")
        print("Model loaded ✓")

        print("Monitoring ...")
        data, model, pipe = monitoring_pipeline(
            dataframe=the_data, model=the_model, pipeline=scoring_pipeline
        )
        print("Monitoring ✓")

        # Log basic info about the run
        mlflow.log_param("data_path", file_path)
        mlflow.log_param("data_shape", str(the_data.shape))
        mlflow.log_metric("row_count", len(the_data))

        # If pipe is a DataFrame with predictions, log summary stats
        if isinstance(pipe, pd.DataFrame):
            mlflow.log_metric("prediction_count", len(pipe))
            mlflow.log_artifact(pipe.to_csv(index=False), "predictions.csv")
