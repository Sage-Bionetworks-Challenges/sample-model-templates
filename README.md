# sample-model-templates
Sample templates for creating a Docker model submission on Synapse. We currently
provide examples in Python and R.

### Requirements
* Python or R
* [Docker]
* [Synapse account]

## Write your algorithm

1. Replace the code in the `run_model.*` script with your own algorithm(s).

2. (If using Python) Update `requirements.txt` with any additional libraries/packages used
    by your script(s).

3. (optional) Locally run the script to ensure it can run successfully.  

    The sample scripts have been written so that the input and output files
    are not hard-coded in `/input` and `/output`, respectively.  This way, you
    can test your changes without having to create these directories. For
    example, the following indicates that the input files are available in
    `sample_data/`, while the output file, `predictions.csv`, will be written
    to the current working directory (`.`):

    ```
    python run_model.py --input-dir sample_data/ --output-dir .
    ```

## Build your model

1. (If using R) Update the Dockerfile with any additional packages used by your script(s).

> **Note** All Docker submissions are run without network access, so you must install all
> needed dependencies during this step (image building) rather than during the container run.

2. Dockerize your model (assuming you are either in `r/` or `python/`):

    ```
    docker build -t docker.synapse.org/<project id>/my-model:v1 .
    ```

    where:

    * `<project id>`: Synapse ID of your project
    * `my-model`: name of your model
    * `v1`: version of your model
    * `.`: filepath to the Dockerfile

3. (optional but recommended) Locally run the model to ensure it can run successfully:

    ```
    docker run \
        --rm \
        --network none \
        --volume $PWD/sample_data:/input:ro \
        --volume $PWD/output:/output:rw \
        docker.synapse.org/<project id>/my-model:v1
    ```

> **Note** if your model requires a GPU, be sure to expose it with `--runtime nvidia`

## Prepare your submission

1. If you haven't already, log into the Synapse Docker registry with your Synapse
    credentials. We highly recommend you use a Synapse Personal Access Token (PAT)
    for this step. Once logged in, you should not have to log in again, unless you
    log out or switch Docker registries.

    ```
    docker login docker.synapse.org --username <syn_username>
    ```

    When prompted for a password, enter your PAT.

    > [Learn more about Synapse PATs and how to generate one].

    You can also log in non-interactively through `STDIN` - this will prevent your
    password from being saved in the shell's history and log files. For example, if
    you saved your PAT into a file called `synapse.token`:

    ```
    cat ~/synapse.token | \
      docker login docker.synapse.org --username <syn_username> --password-stdin
    ```

2. Use `docker push` to push the model up to your project on Synapse.

    ```
    docker push docker.synapse.org/<project id>/my-model:v1
    ```

3. The Docker image should now be available in the **Docker** tab of your Synapse project.


[Docker]: https://docs.docker.com/get-docker/
[Synapse account]: https://www.synapse.org/#
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens