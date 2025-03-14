# Use AWS Lambda Python 3.12 Base Image (Amazon Linux 2023)
FROM public.ecr.aws/sam/build-python3.12:latest

# Set the working directory
WORKDIR /var/task

# Install dependencies
COPY requirements.txt .
RUN pip install --platform manylinux2014_aarch64 --only-binary=:all: -r requirements.txt -t .

# Copy Lambda function code
COPY . .

# Move all dependencies and code to /asset-output (required for AWS CDK)
RUN mkdir -p /asset-output && cp -r . /asset-output