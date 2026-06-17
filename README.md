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

0. If needed, open the terminal and switch directories into the folder that
   contains your Dockerfile (either `r/` or `python/` from the template).

1. Use the `docker build` command to create your image.
  
   For the Synapse Docker Registry, image names must start with `docker.synapse.org/`
   followed by the project you want to push it to, then the name you want to give it:

   ```
   docker build --tag docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION FILEPATH/TO/DOCKERFILE
   ```

   where:

   Command Part | Description | Example
   --|--|--
   `PROJECT_ID` | synID of a Synapse project to push image, in this case, it should be your project | `syn1234567`
   `IMAGE_NAME` | name you choose for your model image | `my_model`
   `TAG_VERSION` | version of the image you are building; if omitted, `latest` is used | `v1.0.0`
   `FILEPATH/TO/DOCKERFILE` | relative path to the Dockerfile you are using to build the image | `.`

   For example, if your Synapse project synID is `syn1234567` and the Dockerfile is in the current
   directory (`.`), the command would be:

   ```
   docker build --tag docker.synapse.org/syn1234567/my_model:v1.0 .
   ```

> [!IMPORTANT]
> If you are building on a device with the M1/M2 chips (e.g. Apple silicon Macs), which
> uses the `arm64` processor, you will also need to build a Docker image for `amd64`.
> You can do this with either a single-platform or multi-platform build:
>
> ```
> # Single-platform build
> docker buildx build \
>   --platform linux/amd64 \
>   --tag docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION FILEPATH/TO/DOCKERFILE
> 
> # Multi-platform build (recommended if you share the image with other M1/M2 users)
> docker buildx build \
>   --platform=linux/amd64,linux/arm64 \
>   --tag docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION FILEPATH/TO/DOCKERFILE
> ```


2. (optional but **strongly recommended**) Test your newly-built model locally using
   sample data (such as the training data) to ensure it runs correctly and meets the
   performance constraints. For example:

   ```
   docker run \
       --rm \
       --network none \
       --volume SOURCE:DEST:PERMISSIONS [--volume ...] \
       --memory SIZE --memory-swap SIZE --shm-size SIZE \
       docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION
   ```

   where:
   
   Command Part | Description | Notes
   --|--|--
   `--rm` | Removes the container after execution | You can omit this if you need to check the logs or inspect the container post-run
   `--network none` | Disables all network connections to the container | Required for accurate testing, as it mimics the evaluation system for Synapse
   `--volume SOURCE:DEST:PERMISSIONS` | Mounts local directories to the container with read-only (`ro`) or read-write (`rw`) permissions | Use absolute paths for `SOURCE` and `DEST`
   `--memory SIZE` | Sets the primary RAM limit; unit can be `b`, `k`, `m`, or `g` | Adjust this to match the challenge constraints. Synapse defaults to `16g` if none provided.
   `--memory-swap SIZE` | Sets the the total memory (RAM + swap) limit; unit can be `b`, `k`, `m`, or `g` | Adjust this to match the constraints. Synapse defaults to `16g` (indicating no swap access) if none provided
   `--shm-size SIZE` | Sets the size of the shared memory (`/dev/shm`) | Adjust this to match the challenge constraints. Default is `64m` if none provided.

    For example:

   ```
   docker run \
       --rm \
       --network none \
       --volume $PWD/sample_data:/input:ro \
       --volume $PWD/output:/output:rw \
       --memory 4g --memory-swap 6g --shm-size 1g \
       docker.synapse.org/syn1234567/my_model:v1.0
   ```

    If your model requires a GPU, add `--runtime nvidia` or `--gpus all`. Ensure
    the [NVIDIA Container Toolkit] is installed if using GPU support.

### Prepare and push your model to Synapse

1. If you haven't already, log into the Synapse Docker registry with your Synapse
   credentials:

   ```
   docker login docker.synapse.org --username SYNAPSE_USERNAME
   ```

   Synapse now requires Multi-factor Authentication, so you must use a Synapse
   Personal Access Token (PAT) at this step.  The PAT you use has "Modify"
   permissions enabled so you can push images to your Synapse project(s).

   > [Learn more about Synapse PATs and how to generate one].

   You can also log in non-interactively through `STDIN` - this will prevent
   your PAT from being saved in the shell's history and log files. For example,
   if you saved your PAT into a file called `synapse.token`:

   ```
   cat ~/synapse.token | \
     docker login docker.synapse.org --username SYNAPSE_USERNAME --password-stdin
   ```

3. Push the Docker image to your Synapse project:

   ```
   docker push docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION
   ```

   The Docker image will be available in the **Docker** tab of your Synapse
   project.

> [!NOTE]
> If you receive an error, double-check that you are
> * a Certified User;
> * pushing to YOUR Synapse project (not the challenge's); and
> * using a Synapse PAT with "Modify" permissions

[Docker]: https://docs.docker.com/get-docker/
[Synapse account]: https://www.synapse.org/#
[Trusted Content images]: https://hub.docker.com/search?q=&image_filter=official%2Cstore
[Learn more about Docker's build cache]: https://docs.docker.com/build/cache/
[NVIDIA Container Toolkit]: https://github.com/NVIDIA/nvidia-docker
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens
