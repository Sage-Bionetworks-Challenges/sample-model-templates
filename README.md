<h1 align="center">
    Docker Model Templates
</h1>
<h3 align="center">
    Templates for creating a Docker model submission on Synapse.
</h3>

Sample model templates for both Python and R are provided. You can build off of
this template or use it as a reference to build your model from scratch.

### Requirements

- Python (and [uv](https://docs.astral.sh/uv/getting-started/installation/)) or R
- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose (included with Docker Desktop; Linux users without Docker Desktop can follow the
  [Compose install guide])
- Synapse project for the challenge

---

### TL;DR - Quickstart

```sh
cp .env.example .env
open .env                      # update with your config values
docker compose build           # build and tag the image
docker compose run --rm model  # test locally against sample_data/
docker compose push            # push to the Synapse Docker registry
```

---

### Step-by-step guide

#### 1. Write your algorithm

- Replace the placeholder code in `run_model.*` with your own logic. Add helper functions
  and scripts as needed.

- Update dependencies:
  - **Python:** Use `uv add <package>` or edit `pyproject.toml` directly. Run
    `uv lock` to regenerate the lockfile for fully reproducible builds
  - **R:** Edit the `pkg_list` variable in `requirements.R`

- (optional) Run the script locally to verify it works before containerizing:

  ```sh
  # Python
  uv run python/run_model.py --input-dir sample_data/ --output-dir .

  # R
  Rscript r/run_model.R --input-dir sample_data/ --output-dir .
  ```

#### 2. Update the Dockerfile

- All dependencies must be installed at build time — network access is
  disabled when your submissions are evaluated
- Use one `COPY` instruction per file to maximize Docker's layer cache
- If needed, swap the base image for another [Trusted Content image] such as
  `bitnami/pytorch`, `r-base`, or `rocker/tidyverse`

  > → [Learn more about Docker's build cache].

#### 3. Configure `.env`

Copy `.env.example` to `.env` and fill in your values:

```sh
cp .env.example .env
```

Key variables:

| Variable | Description | Example |
|---|---|---|
| `DOCKERFILE_FOLDER` | Subfolder with the Dockerfile (`python` or `r`) | `python` |
| `IMAGE` | Full image name to build and push.<br/><br/>If pushing to Synapse, image names must start with `docker.synapse.org/` followed by the project ID you want to push it to, then the name you want to give the image. | `docker.synapse.org/syn1234567/my_model:v1.0` |
| `INPUT_DIR` | Absolute path to local input data folder | `$PWD/sample_data` |
| `OUTPUT_DIR` | Absolute path for generated prediction(s) | `$PWD/output` |

Resource limits (`MEMORY_LIMIT`, `MEMORY_SWAP_LIMIT`, `SHM_SIZE`) can also be
set in `.env` — see `.env.example` for details. Match these to the constraints
specified in the challenge.

#### 4. Build and test

```sh
# Build the model image
docker compose build

# Run your model against the input data (defined by INPUT_DIR in .env)
docker compose run --rm model
```

**Multi-platform builds**

`docker compose build` targets the `linux/amd64` platform by default. If you are using
a newer Mac (2020 or later), your machine natively runs on `arm64`. To ensure your image
can run locally for testing and on the evaluation infrastructure, use `docker buildx build`
to cross-compile for both platforms:

```sh
# Load .env variables into your terminal session
export $(cat .env | xargs)

# Execute the multi-architecture build
docker buildx build \
  --platform=linux/amd64,linux/arm64 \
  --tag $IMAGE \
  $DOCKERFILE_FOLDER/
```

#### 5. Push your model to Synapse

Before pushing, you must log in to the Synapse Docker Registry first. This is generally only
needed one time.

```sh
docker login docker.synapse.org --username SYNAPSE_USERNAME
```

Because Synapse now requires multi-factor authentication, you must use a Synapse Personal
Access Token (PAT) with "Modify" permissions enabled when prompted for a password.

> → [Learn more about Synapse PATs and how to generate one].

You can also log in non-interactively through `STDIN` - this will prevent your PAT from being
saved in the shell's history and log files. For example, if you saved your PAT into a file
called `synapse.token`:

```sh
cat ~/synapse.token | \
  docker login docker.synapse.org --username SYNAPSE_USERNAME --password-stdin
```

Once logged in, push your image up to Synapse:

```sh
docker compose push
```

If `docker compose push` fails, double-check that you are:
 - a Certified Synapse User
 - pushing to **your** project (not the challenge's project)
 - using a PAT with "Modify" permissions

---

### Manual steps (without Docker Compose)

If you prefer to use the Docker commands instead of Compose:

```sh
# Build the image
docker build \
  --tag docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION \
  python/   # or r/

# Test locally
docker run \
  --rm \
  --network none \
  --volume $PWD/sample_data:/input:ro \
  --volume $PWD/output:/output:rw \
  --memory 4g --memory-swap 6g --shm-size 1g \
  docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION

# Push to Synapse
docker push docker.synapse.org/PROJECT_ID/IMAGE_NAME:TAG_VERSION
```

where:

| Flag | Description |
|---|---|
| `--rm` | Remove the container after it exits |
| `--network none` | Disable networking (mimics Synapse evaluation environment) |
| `--volume SOURCE:DEST:ro\|rw` | Mount a local directory into the container |
| `--memory` | RAM limit (e.g. `4g`). Synapse default: `16g` |
| `--memory-swap` | Total RAM + swap limit. Synapse default: `16g` (no swap) |
| `--shm-size` | Shared memory size. Default: `64m` |

If your model requires a GPU, add `--runtime nvidia` or `--gpus all`. Ensure the 
[NVIDIA Container Toolkit] is installed if using GPU support.

---

## Extras

### Measuring runtime

If there is a time limit in the challenge you're participating in, you can measure
how long your model takes to run by prefixing the command with `time`:

```sh
time docker compose run --rm model
```

When the container finishes, you'll see output like:

```
real    1m23.45s
user    0m0.12s
sys     0m0.08s
```

`real` is the wall-clock time — the number to compare against the challenge's
time limit. 

For more precise timestamps (e.g. millisecond precision or programmatic use),
you can omit `--rm` from the command and then use `docker inspect` to get the
start and end timestamps.

```sh
docker compose run model
docker inspect $(docker ps -lq) \
  --format 'Start: {{.State.StartedAt}}{{"\n"}}End:   {{.State.FinishedAt}}'
docker rm $(docker ps -lq)  # clean up manually
```

[Compose install guide]: https://docs.docker.com/compose/install/
[Trusted Content image]: https://hub.docker.com/search?q=&image_filter=official%2Cstore
[Learn more about Docker's build cache]: https://docs.docker.com/build/cache/
[NVIDIA Container Toolkit]: https://github.com/NVIDIA/nvidia-docker
[Learn more about Synapse PATs and how to generate one]: https://help.synapse.org/docs/Managing-Your-Account.2055405596.html#ManagingYourAccount-PersonalAccessTokens
