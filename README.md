<h1 align="center">
    Docker Model Templates
</h1>
<h3 align="center">
    Templates for creating a Docker model submission on Synapse.
</h3>

You can either build off of this repository template or use it as reference 
to build your model from scratch.  We have provided a sample model template
for both R and Python.

### Requirements
* Python or R
* [Docker](https://docs.docker.com/get-docker/)
* [Synapse account](https://www.synapse.org/#)
* Synapse project for the challenge

---

### Write your algorithm(s)

1. Replace the code in the `run_model.*` script with your own algorithm(s).
    You can create additional scripts for modularization/better organization
    if desired.

2. If using Python, update `requirements.txt` with any additional
    libraries/packages used by your script(s).

    If using R, update `requirements.R` and add/remove any libraries/packages
    listed in `pkg_list` that are used by your script(s).

3. (optional) Locally run `run_model.*` to ensure it can run successfully.

    These scripts have been written so that the input and output files are not
    hard-coded in the `/input` and `/output` directories, respectively (though
    they are used by default).  This way, you can test your changes using any
    directories as input and/or output.

    For example, the following indicates that the input files are in
    `sample_data/`, while the output file should be written to the current
    working directory (`.`):

    **Python**
    ```
    python run_model.py --input-dir ../sample_data/ --output-dir .
    ```

    **R**
    ```
    Rscript run_model.R --input-dir ../sample_data/ --output-dir .
    ```

### Update the Dockerfile

* Again, make sure that all needed libraries/packages are specified in the 
`requirements.*` file.  Because all Docker submissions are run without network
access, you will not able to install anything during the container run. If
you do not want to use a `requirements.*` file, you may run replace the RUN
command with the following:

    **Python**
    ```
    RUN pip install pandas
    ```

    **R**
    ```
    RUN R -e "install.packages(c('optparse'), repos = 'http://cran.us.r-project.org')"
    ```

* `COPY` over any additional files required by your model. We recommend using
one `COPY` command per file, as this can help speed up build time.

* Feel free to update the base image and/or tag version if the provided base
image do not fulfill your needs. Although you can use any valid image as the
base, we recommend using one of the [Trusted Content images], especially if
you are new to Docker. Images to consider:
    * ubuntu
    * python
    * bitnami/pytorch
    * r-base
    * rocker/tidyverse

* If your image takes some time to build, look at the order of your Dockerfile
commands -- **the order matters**.  To best take advantage of Docker's
build-caching (that is, reusing previously built layers), it's often a good
idea to put frequently-changing parts (such as `run_model.*`) near the end
of the Dockerfile. The way build-caching works is that once a step needs to
be rebuilt, all of the subsequent steps will also be rebuilt.

    > [Learn more about Docker's build cache].

### Build your model

1. Assuming you are either in `r/` or `python/`, Dockerize your model:

    ```
    docker build -t docker.synapse.org/<project id>/my-model:v1 .
    ```

    where:

    * `<project id>`: Synapse ID of your project
    * `my-model`: name of your model
    * `v1`: version of your model
    * `.`: filepath to the Dockerfile

    Update the model name and/or tag name as desired.

> [!IMPORTANT]
> The submission system uses the x86-64 cpu architecture. If your machine uses a different architecture, e.g. Apple Silicon, you will need to additionally include `--platform linux/amd64` into the command, e.g.
> 
> `docker build -t <image name> --platform linux/amd64 <filepath to Dockerfile>`

3. (optional but highly recommended) Locally run a container to ensure the
    model can run successfully:

    ```
    docker run \
        --rm \
        --network none \
        --volume $PWD/sample_data:/input:ro \
        --volume $PWD/output:/output:rw \
        docker.synapse.org/<project id>/my-model:v1
    ```
    
    where:

    * `--rm`: stops and removes the container once it is done running
    * `--network none`: disables all network connections to the container
        (emulating the same behavior seen in the submission queues)
    * `--volume ...`: mounts data generated by and used by the container. For
        example, `--volume $PWD/sample_data:/input:ro` will mount
        `$PWD/sample_data` (from your machine) as `/input` (in the container)
        with read-only permissions.
    * `docker.synapse.org/<project id>/my-model:v1`: Docker image and tag
        version to run

    If your model requires a GPU, be sure to expose it by adding `--runtime nvidia`
    or `--gpus all`. Note that your local machine will also need the
    [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker).

### Prepare and push your model to Synapse

1. If you haven't already, log into the Synapse Docker registry with your
    Synapse credentials. We highly recommend you use a Synapse Personal Access
    Token (PAT) for this step. Once logged in, you should not have to log in
    again, unless you log out or switch Docker registries.

    ```
    docker login docker.synapse.org --username <syn_username>
    ```

    When prompted for a password, enter your PAT.

    > [Learn more about Synapse PATs and how to generate one].

    You can also log in non-interactively through `STDIN` - this will prevent
    your password from being saved in the shell's history and log files. For
    example, if you saved your PAT into a file called `synapse.token`:

    ```
    cat ~/synapse.token | \
      docker login docker.synapse.org --username <syn_username> --password-stdin
    ```

2. Use `docker push` to push the model up to your project on Synapse.

    ```
    docker push docker.synapse.org/<project id>/my-model:v1
    ```

    The Docker image should now be available in the **Docker** tab of your
    Synapse project.



[Docker]: https://docs.docker.com/get-docker/
[Synapse account]: https://www.synapse.org/#
[Trusted Content images]: https://hub.docker.com/search?q=&image_filter=official%2Cstore
[Learn more about Docker's build cache]: https://docs.docker.com/build/cache/
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens
