import boto3
import sagemaker
from sagemaker.xgboost.model import XGBoostModel

# Step 1: Setup SageMaker Session and S3 Bucket
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()
bucket = sagemaker_session.default_bucket()
prefix = "xgboost-batch-inference-gpu"

# Define paths
test_data_file = "test.csv"  # Ensure this file is preprocessed
s3_test_data = f"s3://{bucket}/{prefix}/test.csv"
s3_output_path = f"s3://{bucket}/{prefix}/predictions/"

# Step 2: Upload Test Data to S3
s3 = boto3.client("s3")
s3.upload_file(test_data_file, bucket, f"{prefix}/test.csv")
print(f"Test dataset uploaded to: {s3_test_data}")

# Step 3: Retrieve Trained Model from S3
model_artifact_path = "s3://your-bucket/xgboost-model-path/model.tar.gz"  # Update this path

# Step 4: Create SageMaker XGBoost Model (GPU-Compatible)
xgb_model = XGBoostModel(
    model_data=model_artifact_path,
    role=role,
    framework_version="1.5-1"
)

# Step 5: Run Batch Inference on GPU
transformer = xgb_model.transformer(
    instance_count=1,
    instance_type="ml.p3.2xlarge",  # ✅ Use GPU for inference
    output_path=s3_output_path,
    assemble_with="Line",
    accept="text/csv"
)

# Start Batch Transform on GPU
transformer.transform(
    data=s3_test_data,
    content_type="text/csv",
    split_type="Line",
    input_filter="$[1:]",  # Ignore the first column if test data has labels
    join_source="Input",
    wait=True
)

print(f"Batch inference completed! Predictions saved at: {s3_output_path}")

# Step 6: Download and View Predictions
local_predictions_file = "predictions.csv"
s3.download_file(bucket, f"{prefix}/predictions/test.csv.out", local_predictions_file)
print(f"Predictions downloaded as: {local_predictions_file}")

# Display Predictions
import pandas as pd
df_preds = pd.read_csv(local_predictions_file, header=None)
print("Predictions Preview:")
print(df_preds.head())
