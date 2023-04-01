# sample-model-templates
Sample templates for creating a Docker model submission on Synapse. We currently
provide examples in Python and R.

### Requirements
* Python or R
* [Docker](https://docs.docker.com/get-docker/)
* [Synapse account](https://www.synapse.org/#)

## Write your algorithm

1. Replace the code in the `run_model.*` script with your own algorithm(s).

2. Update `requirements.txt` with any additional libraries/packages used.

3. (optional) Locally run the script to ensure it can run successfully.  

    The sample scripts are written in a way so that you can adjust the values of 
    `input_dir` and `output_dir`. That is, `input_dir` and `output_dir` does not 
    always have to be `/input` and `/output`, respectively. For example:

    ```
    python run_model.py --input-dir sample_data/ --output-dir .
    ```

## Build your model

1. Dockerize your model:

    ```
    docker build -t docker.synapse.org/<project id>/my-model:v1 .
    ```

    where:

    * `<project id>`: Synapse ID of your project
    * `my-model`: name of your model
    * `v1`: version of your model
    * `.`: filepath to the Dockerfile

2. (optional but recommended) Locally run the model to ensure it can run successfully:

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

1. If you haven't already, log into the Synapse Docker registry with your Synapse credentials.
You should only need to do this step once, assuming you do not switch Docker registries.

    ```
    docker login docker.synapse.org
    ```

    You can also log in non-interactively through `STDIN` - this will prevent
    your password from being saved in the shell's history and log files:

    ```
    cat ~/syn_password.txt | \
      docker login docker.synapse.org --username <syn_username> --password-stdin
    ```

2. Use `docker push` to push the model up to your project on Synapse.

    ```
    docker push docker.synapse.org/<project id>/my-model:v1
    ```

3. The Docker image should now be available in the **Docker** tab of your Synapse project.