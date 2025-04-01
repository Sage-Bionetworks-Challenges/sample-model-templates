<h1 align="center">
    Docker Model Templates
</h1>
<h3 align="center">
    Templates for creating a Docker model submission on Synapse.
</h3>

You can either build off of this repository template or use it as reference
to build your model from scratch. Sample model templates for both R and
Python are provided.

### Requirements

- Python or R
- [Docker](https://docs.docker.com/get-docker/)
- [Synapse account](https://www.synapse.org/#)
- Synapse project for the challenge

---

### Write your algorithm(s)

1. Replace the placeholder code in `run_model.*` script with your own
   algorithm(s). Create additional functions and scripts for modularity
   and organization as needed.

2. Manage the dependencies:

   - **Python:** Update `requirements.txt` with any required Python libraries.
   - **R:** Update `requirements.R` by modifying the `pkg_list` variable to
     include or exclude necessary R packages.

3. (optional) Locally run `run_model.*` to verify it can run successfully.

   The scripts have been designed to accept input and output directories as
   command-line arguments, allowing you to test with various data locations.

   - By default, the scripts look for input in the `/input` directory
     and write output to the `/output` directory, as expected by the
     Synapse submission system.

   - To use custom directories, specify them as arguments. For example:

     **Python**

     ```
     python python/run_model.py --input-dir sample_data/ --output-dir .
     ```

     **R**

     ```
     Rscript r/run_model.R --input-dir sample_data/ --output-dir .
     ```

     where:

     - `sample_data/` is used as the input directory
     - `.` (current working directory) is used as the output directory

### Update the Dockerfile

- Ensure all dependencies are listed in `requirements.*` so that they are
  installed during this build process, as network access is disabled when
  your submission is run.

- Use `COPY` to add any files required by your model. We recommend using
  one `COPY` command per file for optimized build caching.

- Update the base image and/or tag version if the provided base do not 
  fulfill your needs. Although you may use any valid image as the base,
  we recommend using one of the [Trusted Content images] for security and
  reliability, such as:

  * `ubuntu`
  * `python`
  * `bitnami/pytorch`
  * `r-base`
  * `rocker/tidyverse`

- If your image is taking some time to build, consider optimizing the order
  of the Dockerfile commands by placing frequently changing parts near the
  end. This will take advantage of Docker's build caching.

    > [Learn more about Docker's build cache].

### Build your model

1. If you haven't already, change directories to `r/` or `python/`. Then run
   the `build` command to Dockerize your model:

   ```
   docker build -t docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION FILEPATH/TO/DOCKERFILE
   ```

   where:

   - _PROJECT_ID_: Synapse ID of your project.
   - _IMAGE_NAME_: name of your image.
   - _TAG_VERSION_: version of the image. If TAG_VERSION is not supplied,
     `latest` will be used.
   - _FILEPATH/TO/DOCKERFILE_: filepath to the Dockerfile, in this case, it
     will be the current directory (`.`).

2. (optional but highly recommended) Test your newly-built model by running
   it locally. For example:

   ```
   docker run \
       --rm \
       --network none \
       --volume $PWD/sample_data:/input:ro \
       --volume $PWD/output:/output:rw \
       docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION
   ```

   where:

   - `--rm`: removes the container after execution.
   - `--network none`: disables all network connections to the container,
     emulating the same behavior as the Synapse submission system.
   - `--volume SOURCE:DEST:PERMISSIONS`: mounts local directories to the container;
     use absolute paths for _SOURCE_ and _DEST_.

   If your model requires a GPU, add `--runtime nvidia` or `--gpus all`. Ensure
   the [NVIDIA Container Toolkit] is installed if using GPU support.

### Prepare and push your model to Synapse

1. If you haven't already, log into the Synapse Docker registry.  We recommend
   using a Synapse Personal Access Token (PAT) for this step rather than your
   password:

   ```
   docker login docker.synapse.org --username SYNAPSE_USERNAME
   ```

   Enter your PAT when prompted.

   > [Learn more about Synapse PATs and how to generate one].

   You can also log in non-interactively through `STDIN` - this will prevent
   your PAT from being saved in the shell's history and log files. For example,
   if you saved your PAT into a file called `synapse.token`:

   ```
   cat ~/synapse.token | \
     docker login docker.synapse.org --username SYNAPSE_USERNAME --password-stdin
   ```

2. Push the Docker image to your Synapse project:

   ```
   docker push docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION
   ```

   The Docker image will be available in the **Docker** tab of your Synapse
   project.

[Docker]: https://docs.docker.com/get-docker/
[Synapse account]: https://www.synapse.org/#
[Trusted Content images]: https://hub.docker.com/search?q=&image_filter=official%2Cstore
[Learn more about Docker's build cache]: https://docs.docker.com/build/cache/
[NVIDIA Container Toolkit]: https://github.com/NVIDIA/nvidia-docker
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens
