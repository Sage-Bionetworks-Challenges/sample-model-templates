# Define the base of your image.
# We recommend to always specify a tag. `latest` may not 
# always ensure reproducibility.
FROM r-base:4.2.0

# Set the working directory for the COPY, RUN, and ENTRYPOINT
# commands of the Dockerfile.
WORKDIR /usr/local/bin

# Copy files over to the image.
# We recommend copying over each file individually, as to take
# advantage of cache building (which helps reduce build time).
COPY run_model.R .

# Install needed libraries/packages.
# Your model will be run without network access, so the dependencies
# must be installed here (and not during code execution).
RUN R -e "install.packages(c('optparse', 'readr', 'tidyr'), repos = 'http://cran.us.r-project.org')"

# Set the main command of the image.
# We recommend using this form instead of `ENTRYPOINT command param1`.
ENTRYPOINT ["Rscript", "run_model.R"]
