# Smolagent-Chat CLI 😎

This is a simple chat interface to a Smolagents agentic search tool, inspired by the Smolagents multi-agents orchestration lesson at Huggingface.

It's an exercise in making a simple CLI tool that can be configured to use both local (Ollama) and remote (Anthropic) models and telemetry services (Arize/Phoenix). It's a great vehicle for learning.

## Get Started

There are two ways to run this: directly in your local cli environment, or via docker

### Local (no-docker)
Create a new conda forge environment:

```
conda create --prefix ./conda python=3.12
conda activate ./conda
```

Install dependencies

```
pip install -r requirements.txt
```

### Docker

You can run the script in a docker container, using a read-only mount (for safety - it's good practice with agents)

```
docker build -t smolchat .
docker run --name smolchat --network local-net  -v ./:/app:ro -it smolchat python chat.py
```

then subsequent runs

```
docker start -i smolchat
```

_NOTE_ If you are using ollama locally, add `--network=host` to the `docker run` command, also ensuring your ollama domain is `host.docker.internal` (for development only). If you're connecting to a local Phoenix container, change the network to `--network local-net`

### Environment Configuration

Add your environment vars to .env (not tracked by git)

```

HF_TOKEN=your-huggingface-token

## ANTHROPIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ANTHROPIC_TOKEN=your-anthropic-token
MODEL_ID="anthropic/claude-3-5-sonnet-20240620"

## OLLAMA / Locally ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL_ID="ollama_chat/qwen2.5-coder:7b-instruct"
# MODEL_ID="ollama_chat/granite3-dense:2b"
# LLM_API_BASE="http://host.docker.internal:11434"

## TELEMETRY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Local / Docker
PHOENIX_COLLECTOR_ENDPOINT="http://phoenix:6006/v1/traces"

### Cloud
# PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com
# PHOENIX_API_KEY=your-api-key
# PHOENIX_SPACE_ID=your-space-id

## WRAP UP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### Convenience
LLM_API_TOKEN=${ANTHROPIC_TOKEN}

```

### Telemetry

This project assumes [Arize / Phoenix](https://app.arize.com/) telemetry is configured. Dependencies for both configurations are installed. Though smolagents also supports [Langfuse](https://github.com/langfuse/langfuse), it is not included here.

You can run Phoenix locally via docker

First run
```
docker run --rm  --name phoenix --network local-net  -p 6006:6006 -p 4317:4317 -i -t arizephoenix/phoenix
```

subsequent runs
```
docker start -i phoenix
```

It's important to note that the docker-docker name of this container is `phoenix`, such that your collector endpoint should look like this in the .env file
```
PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006/v1/traces
```

Or using a free Arize account, simply configure these in your .env
*  `PHOENIX_COLLECTOR_ENDPOINT`
*  `PHOENIX_API_KEY`
*  `PHOENIX_SPACE_ID`

The script will configure local vs cloud based on the collector endpoint.

#### Local/Docker Environment Configuration

Docker:
```
PHOENIX_COLLECTOR_ENDPOINT="http://phoenix:6006/v1/traces"
```

#### Arize Cloud Environment Configuration

```
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com
PHOENIX_API_KEY=yourAPIkey
PHOENIX_SPACE_ID=FromArizeSpaceConfiguration
```
The Spaec ID can be obtained by creating a "New Project Or Model" from the project dashboard at arize.com