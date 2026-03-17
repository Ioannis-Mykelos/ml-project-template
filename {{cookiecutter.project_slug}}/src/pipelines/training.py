"""Training pipeline template — compatible with Azure ML and Databricks."""

import io
import os
from typing import Any

import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb
from mlflow.tracking import MlflowClient
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


def compute_confusion_matrix_image(cm: np.ndarray, class_labels: list) -> plt.Figure:
    """
    Generate a confusion matrix heatmap figure.

    Arguments:
    ----------
    - cm            (np.ndarray) : Confusion matrix array.
    - class_labels  (list)       : Labels for majority and minority classes.

    Returns:
    --------
    - fig (plt.Figure) : Matplotlib figure of the heatmap.
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_labels,
        yticklabels=class_labels,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


def training_pipeline(
    dataframe: pd.DataFrame,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
    xgb_params: dict[str, Any] | None = None,
) -> tuple[xgb.XGBClassifier, dict, list, np.ndarray, pd.Series]:
    """
    Training pipeline template compatible with Azure ML and Databricks.
    Supports binary classification only.

    Arguments:
    ----------
    - dataframe     (pd.DataFrame) : Input data for training.
    - target_column (str)          : Name of the target column.
    - test_size     (float)        : Total fraction of data held out, split evenly between test and eval.
    - random_state  (int)          : Random seed for reproducibility.
    - xgb_params    (dict)         : XGBoost hyperparameters. Uses defaults if None.

    Returns:
    -------
    - model        (xgb.XGBClassifier) : Trained XGBoost classifier.
    - metrics      (dict)              : Evaluation metrics on the test set.
    - class_labels (list)              : [majority_class, minority_class] labels.
    - cm           (np.ndarray)        : Confusion matrix.
    - feature_importances (pd.Series)  : Feature importance scores from the model.
    """
    data = dataframe.copy()

    # TODO: Add any feature engineering logic here
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # First split: separate train from (test + eval)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    # Second split: divide (test + eval) evenly into test and eval
    X_test, X_eval, y_test, y_eval = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=random_state, stratify=y_temp
    )

    # Identify majority and minority classes by frequency in training set
    class_counts = y_train.value_counts()
    majority_class = class_counts.idxmax()
    minority_class = class_counts.idxmin()
    class_labels = [majority_class, minority_class]

    # Default XGBoost hyperparameters
    if xgb_params is None:
        xgb_params = {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "use_label_encoder": False,
            "eval_metric": "logloss",
            "random_state": random_state,
        }

    model = xgb.XGBClassifier(**xgb_params)
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_eval, y_eval)],
        early_stopping_rounds=20,
        verbose=True,
    )

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    y_eval_pred = model.predict(X_eval)
    y_eval_prob = model.predict_proba(X_eval)[:, 1]

    # Per-class F1 scores (binary: pos_label targets each class)
    f1_majority = f1_score(y_test, y_pred, pos_label=majority_class)
    f1_minority = f1_score(y_test, y_pred, pos_label=minority_class)

    # Feature importances as a pandas Series for easier logging and interpretation
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)

    # Overall metrics
    metrics = {
        # Random seed and data split info for reproducibility
        "random_state": random_state,
        # Training metrics (from log dict passed via XGBoost callbacks if used)
        "loss": None,  # TODO: populate if using early stopping callbacks
        "val_loss": None,  # TODO: populate if using early stopping callbacks
        # Test set metrics
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, average="weighted"),
        "precision": precision_score(y_test, y_pred, average="weighted"),
        "recall": recall_score(y_test, y_pred, average="weighted"),
        "auc": roc_auc_score(y_test, y_prob),
        # Eval set metrics
        "val_accuracy": accuracy_score(y_eval, y_eval_pred),
        "val_f1_score": f1_score(y_eval, y_eval_pred, average="weighted"),
        "val_precision": precision_score(y_eval, y_eval_pred, average="weighted"),
        "val_recall": recall_score(y_eval, y_eval_pred, average="weighted"),
        "val_auc": roc_auc_score(y_eval, y_eval_prob),
        # Per-class F1
        "f1_majority_class": f1_majority,
        "f1_minority_class": f1_minority,
    }

    # Remove None metrics (loss/val_loss if not populated)
    metrics = {k: v for k, v in metrics.items() if v is not None}

    # Confusion matrix on test set
    cm = confusion_matrix(y_test, y_pred, labels=class_labels)

    return model, metrics, class_labels, cm, feature_importances


if __name__ == "__main__":

    TARGET_COLUMN = "churn"
    XGB_PARAMS = {
        "n_estimators": 100,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "use_label_encoder": False,
        "eval_metric": "logloss",
        "random_state": 42,
    }

    with mlflow.start_run():

        mlflow.set_tag("pipeline", "training_pipeline_template")
        mlflow.log_params(XGB_PARAMS)

        # Load data
        file_path = os.getenv("DATA_PATH_TRAINING")
        if file_path is None:
            raise ValueError("DATA_PATH_TRAINING environment variable is not set")
        the_data = (
            pd.read_parquet(file_path)
            if file_path.endswith(".parquet")
            else pd.read_csv(file_path, engine="python")
        )

        # Log input data info
        mlflow.log_dict(
            {
                "shape": list(the_data.shape),
                "columns": list(the_data.columns),
                "dtypes": the_data.dtypes.astype(str).to_dict(),
            },
            "input_dataframe_info.json",
        )

        # Train model
        model, metrics, class_labels, cm, feature_importances = training_pipeline(
            dataframe=the_data,
            target_column=TARGET_COLUMN,
            xgb_params=XGB_PARAMS,
        )

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log confusion matrix
        mlflow.log_dict(
            {"labels": [str(lbl) for lbl in class_labels], "matrix": cm.tolist()},
            "confusion_matrix.json",
        )
        fig = compute_confusion_matrix_image(cm, [str(lbl) for lbl in class_labels])
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        mlflow.log_image(buf.read(), "confusion_matrix.png")
        plt.close(fig)

        # Log feature importance
        mlflow.log_dict(feature_importances.to_dict(), "feature_importance.json")
        fig, ax = plt.subplots(figsize=(8, max(6, len(feature_importances) / 2)))
        feature_importances.sort_values().plot.barh(ax=ax)
        mlflow.log_figure(fig, "feature_importance.png")
        plt.close(fig)

        # Save and register the model
        mlflow.log_param(
            "registered_model_uri", f"runs:/{mlflow.active_run().info.run_id}/model"
        )
        mlflow.xgboost.log_model(model, artifact_path="model")

        result = mlflow.register_model(
            model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
            name="churn_model",
        )

        # Assign version to Staging for validation
        client = MlflowClient()
        client.transition_model_version_stage(
            name="churn_model", version=result.version, stage="Staging"
        )

        print(f"Model version {result.version} registered in Staging. ✅")
