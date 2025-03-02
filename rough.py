import sagemaker
from sagemaker.estimator import Estimator
import pandas as pd
import boto3

# Step 1: Set Up SageMaker Session & Role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Step 2: Retrieve the Trained Estimator
# Use the model artifact from the completed training job
model_artifact_path = "s3://your-bucket/xgboost-model-path/model.tar.gz"  # Update this path

xgb_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", sagemaker_session.boto_region_name, "1.5-1"),
    role=role,
    instance_count=1,
    instance_type="ml.p3.2xlarge",  # ✅ Use GPU for inference
    model_data=model_artifact_path,  # ✅ Load trained model from S3
    sagemaker_session=sagemaker_session
)

# Step 3: Deploy the Model as a Real-Time Endpoint
predictor = xgb_estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.p3.2xlarge",  # ✅ GPU Instance for fast inference
    endpoint_name="xgboost-gpu-endpoint"  # ✅ Custom endpoint name
)

print("Model deployed successfully!")

# Step 4: Load Test Data for Inference
test_data = pd.read_csv("test.csv", header=None)  # Ensure test.csv has no labels
print("Test Data Shape:", test_data.shape)

# Step 5: Convert to CSV String (SageMaker expects CSV-formatted payload)
payload = test_data.to_csv(index=False, header=False).encode("utf-8")

# Step 6: Invoke the Deployed Endpoint for Real-Time Inference
response = predictor.predict(payload)
print("Raw Predictions:", response)

# Step 7: Process Predictions
import numpy as np

# Convert response to numpy array
predictions = np.array(response.splitlines()).astype(float)  # Adjust if using `multi:softprob`

# If using `multi:softprob`, get class with highest probability
if predictions.ndim > 1:
    predicted_classes = np.argmax(predictions, axis=1)
else:
    predicted_classes = predictions.astype(int)

print("Final Predicted Classes:", predicted_classes)

# Step 8: Save Predictions to a CSV File
df_predictions = pd.DataFrame(predicted_classes, columns=["Predicted_Class"])
df_predictions.to_csv("predictions.csv", index=False)

print("Predictions saved to predictions.csv")
