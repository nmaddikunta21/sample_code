import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
from sagemaker.tuner import IntegerParameter, ContinuousParameter, HyperparameterTuner
from sagemaker.inputs import TrainingInput

# Set SageMaker session and role
sagemaker_session = sagemaker.Session()
role = get_execution_role()

# Define S3 paths for training and validation data
s3_train_data = "s3://your-bucket/train.csv"
s3_validation_data = "s3://your-bucket/validation.csv"

s3_input_train = TrainingInput(s3_train_data, content_type="csv")
s3_input_validation = TrainingInput(s3_validation_data, content_type="csv")

# Define XGBoost Estimator
xgb_estimator = Estimator(
    image_uri="811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    volume_size=50,
    max_run=14400,
    output_path="s3://your-bucket/output/",
    base_job_name="xgboost-binary-classification",
    hyperparameters={
        "objective": "binary:logistic",
        "num_round": 500,
        "max_depth": 6,
        "eta": 0.2,
        "gamma": 4,
        "min_child_weight": 6,
        "subsample": 0.8,
        "verbosity": 1,
        "tree_method": "auto"
    },
    sagemaker_session=sagemaker_session
)

# Define Hyperparameter Ranges
hyperparameter_ranges = {
    "max_depth": IntegerParameter(3, 10),
    "eta": ContinuousParameter(0.01, 0.3),
    "gamma": ContinuousParameter(0, 5),
    "min_child_weight": IntegerParameter(1, 10),
    "subsample": ContinuousParameter(0.5, 1.0)
}

# Define Metric Definitions
metric_definitions = [
    {"Name": "validation:logloss", "Regex": ".*\\[\\d+\\]\\s+validation-logloss:([-+]?[0-9]*\\.?[0-9]+).*"}
]

# Create Hyperparameter Tuner
tuner = HyperparameterTuner(
    estimator=xgb_estimator,
    objective_metric_name="validation:logloss",
    hyperparameter_ranges=hyperparameter_ranges,
    metric_definitions=metric_definitions,
    max_jobs=10,
    max_parallel_jobs=2,
    strategy="Bayesian"
)

# Fit the model with hyperparameter tuning
tuner.fit({"train": s3_input_train, "validation": s3_input_validation})
