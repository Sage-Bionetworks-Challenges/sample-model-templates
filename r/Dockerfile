# Define the base of your image.
# We recommend to always specify a tag. `latest` may not 
# always ensure reproducibility.
FROM r-base:4.4.3

# For best practice, run container as non-root user.
RUN groupadd -r user && useradd -m --no-log-init -r -g user user

# Set the working directory for the COPY, RUN, and ENTRYPOINT
# commands of the Dockerfile.
WORKDIR /home/user

# Copy files over to the image.
# We recommend copying over each file individually, as to take
# advantage of cache building (which helps reduce build time).
COPY requirements.R .

# Install needed libraries/packages.
# Your model will be run without network access, so the dependencies
# must be installed here (and not during code execution).
RUN Rscript requirements.R

# Switch to the non-root user.
USER user

COPY --chown=user:user run_model.R .

# Set the main command of the image.
# We recommend using this form instead of `ENTRYPOINT command param1`.
ENTRYPOINT ["Rscript", "run_model.R"]
