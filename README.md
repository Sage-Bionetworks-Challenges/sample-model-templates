# Sample Templates for Docker Submissions
Sample templates for creating a Docker model submission on Synapse. We currently
provide examples in Python and R.

### Requirements
* Python or R
* [Docker](https://docs.docker.com/get-docker/)
* [Synapse account](https://www.synapse.org/#)

## Setup

You can either fork this repository or use this respository as reference to
build your model from scratch.  We have provided a sample directory structure
for both R and Python.


## 1. Write your algorithm

1. Replace the code in the `run_model.*` script with your own algorithm(s).
    You can create additional scripts for modularization/better organization
    if desired.

2. (If using Python) Update `requirements.txt` with any additional
    libraries/packages used by your script(s).

3. (optional) Locally run `run_model.*` to ensure it can run successfully.

    These scripts have been written so that the input and output files are not
    hard-coded in `/input` and `/output`, respectively (though `/input` and
    `/output` are used as default).  This way, you can test your changes using
    any directories as input and/or output.

    For example, the following indicates that the input files are in `sample_data/`,
    while the output file should be written to the current working directory (`.`):

    **Python**
    ```
    python run_model.py --input-dir ../sample_data/ --output-dir .
    ```

    **R**
    ```
    Rscript run_model.R --input-dir ../sample_data/ --output-dir .
    ```

## 2. Update the Dockerfile

1. (If using R) Update the Dockerfile with any additional packages used by your
    script(s).

> **Note** All Docker submissions will be run without network access, so you
> must install all needed dependencies here in the Dockerfile rather than in
> your Rscripts.

2. `COPY` over any additional files required by your model. To help speed up
    the build time, we recommend `COPY`ing over each file individually.

Note that the order in which you write Dockerfile commands **do matter**. Docker
provides a handy build-caching feature to help speed up build time, by reusing
previously built layers.  Therefore, it's often a good idea to put frequently-changing
parts (such as `run_model.*`) near the end of the Dockerfile, as once one step
needs to be rebuilt, all subsequent steps will also be rebuilt.

> [Learn more about Docker's build cache].

## 3. Build your model

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

3. (optional but highly recommended) Locally run the model to ensure it can run
    successfully:

    ```
    docker run \
        --rm \
        --network none \
        --volume $PWD/sample_data:/input:ro \
        --volume $PWD/output:/output:rw \
        docker.synapse.org/<project id>/my-model:v1
    ```

> **Note** if your model requires a GPU, be sure to expose it with `--runtime nvidia`

## 4. Prepare your submission

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

3. The Docker image should now be available in the **Docker** tab of your
    Synapse project.


[Docker]: https://docs.docker.com/get-docker/
[Synapse account]: https://www.synapse.org/#
[Learn more about Docker's build cache]: https://docs.docker.com/build/cache/
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens