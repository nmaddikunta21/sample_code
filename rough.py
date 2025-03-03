import sagemaker
from sagemaker import get_execution_role, Session
from sagemaker.model import Model

role = get_execution_role()
session = Session()

# The model artifact has been uploaded to S3 during training or otherwise
model_data = "s3://my-bucket/path/model.tar.gz"
image_uri = "<image-uri-of-your-inference-container>"

my_model = Model(
    image_uri=image_uri,
    model_data=model_data,
    role=role,
    sagemaker_session=session
)

# Create a Transformer object from the model
transformer = my_model.transformer(
    instance_count=2,
    instance_type="ml.m5.xlarge",
    output_path="s3://my-bucket/path/batch_output",
    max_concurrent_transforms=4,
    max_payload_in_mb=50,
    accept="text/csv"
)

# Run the batch transform job
transformer.transform(
    data="s3://my-bucket/path/batch_input/",
    content_type="text/csv",
    split_type="Line",
    job_name="my-batch-job"
)
transformer.wait()  # Wait until the job is complete

print("Batch transform job completed.")
print("Output at:", transformer.output_path)
