# Define the base of your image.
# Always specify a tag; `latest` is not guaranteed to be reproducible.
FROM r-base:4.4.3

WORKDIR /app

# Install dependencies before copying your code to maximize build cache reuse.
# No network access at runtime, so all dependencies must be installed here.
COPY requirements.R .
RUN Rscript requirements.R

# Copy each file individually to take advantage of Docker's layer cache.
COPY run_model.R .

# Set the main command of the image.
# Use exec form so signals (e.g. timeouts) reach the process directly.
ENTRYPOINT ["Rscript", "run_model.R"]
