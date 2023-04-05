# Define the base of your image.
# We recommend to always specify a tag. `latest` may not 
# always ensure reproducibility.
FROM python:3.10-slim

# Set the working directory for the COPY, RUN, and ENTRYPOINT
# commands of the Dockerfile.
WORKDIR /usr/local/bin

# Copy files over to the image.
# We recommend copying over each file individually, as to take
# advantage of cache building (which helps reduce build time).
COPY requirements.txt .

# Install needed libraries/packages.
# Your model will be run without network access, so the dependencies
# must be installed here (and not during code execution).
RUN pip install -r requirements.txt

COPY run_model.py .

# Set the main command of the image.
# We recommend using this form instead of `ENTRYPOINT command param1`.
ENTRYPOINT ["python", "run_model.py"]
