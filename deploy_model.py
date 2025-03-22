import sagemaker
from sagemaker.pytorch import PyTorchModel
from sagemaker import Session

# Set up SageMaker session with the US East (N. Virginia) region
sagemaker_session = Session(boto_session=sagemaker.Session().boto_session, region_name='us-east-1')

role = 'root'  # Replace with your actual IAM role

# ECR image URI for Hugging Face PyTorch Inference
image_uri = "763104351884.dkr.ecr.us-west-2.amazonaws.com/huggingface-pytorch-inference:1.12.1-transformers4.25.1-gpu-py38-cu117-ubuntu20.04"

# S3 location of your model files
model_data_url = f's3://charankoyaguritransfermodelbucket/'

# Create a PyTorch model
model = PyTorchModel(
    entry_point='inference.py',  # Your inference script
    source_dir='.',  # Directory containing your inference script
    role=role,
    framework_version='1.12.1',  # Ensure compatible version
    model_data=model_data_url,
    image_uri=image_uri,
)

# Deploy the model
predictor = model.deploy(
    instance_type='g6.12xlarge',  # Choose an instance type suitable for your model size
    initial_instance_count=1,
)
