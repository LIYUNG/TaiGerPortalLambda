# Use the AWS Lambda Python 3.12 runtime image (smaller than sam/build-*).
# This image is only used as a build tool: CDK's Code.fromDockerBuild extracts
# /asset and packages it as a zip for a Runtime.PYTHON_3_12 Lambda.
FROM public.ecr.aws/lambda/python:3.12

# Set the working directory
WORKDIR /var/task

# Install dependencies (wheels only, so no compiler toolchain is needed)
COPY requirements.txt .
RUN pip install --platform manylinux2014_aarch64 --only-binary=:all: -r requirements.txt -t .

# Copy Lambda function code
COPY . .

# Move all dependencies and code to /asset (required for AWS CDK)
RUN mkdir -p /asset && cp -r . /asset
