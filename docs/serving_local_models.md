# Serving Local and Custom Models with OpenLLM

This guide provides instructions on how to use OpenLLM to serve language models that you have downloaded to your local machine. This is useful for air-gapped environments, custom models, or when you prefer not to download models from the Hugging Face Hub at runtime.

## Serving a Locally Downloaded Model

OpenLLM can serve models directly from a local directory. This is the most straightforward way to use a model you already have on your machine.

### Prerequisites

- You have a language model saved on your local filesystem. The model should be in a format that OpenLLM can recognize (e.g., a directory containing the model's weights and configuration files).

### Steps

1.  **Identify the path to your model:**
    Make sure you have the full, absolute path to the directory containing your model. For example, `/path/to/my/local/model`.

2.  **Use the `openllm serve` command:**
    Instead of providing a model name from the Hugging Face Hub, provide the local path to your model.

    ```bash
    openllm serve /path/to/my/local/model
    ```

    OpenLLM will then load the model from the specified directory and start a server.

## Serving a Gated Model from Hugging Face

Some models on the Hugging Face Hub are "gated," meaning you need to agree to their terms of service and obtain an access token.

### Prerequisites

- A Hugging Face account.
- An access token from your Hugging Face account.
- You have requested and been granted access to the gated model.

### Steps

1.  **Set your Hugging Face token as an environment variable:**

    ```bash
    export HF_TOKEN=<your_hugging_face_token>
    ```

2.  **Serve the model:**
    You can now use the `openllm serve` command with the model's Hugging Face ID.

    ```bash
    openllm serve <hugging_face_model_id>
    ```

    OpenLLM will use the `HF_TOKEN` environment variable to authenticate with the Hugging Face Hub and download the model.

## Building a Custom Bento for Your Model

For more advanced use cases, you can build a custom "Bento" for your model. A Bento is a self-contained package that includes your model and all the code and dependencies needed to run it.

### Prerequisites

- Your model and any related files.
- A `bentofile.yaml` to define the Bento.

### Example `bentofile.yaml`

```yaml
service: "my_custom_llm_service.py:svc"
models:
  - my_custom_model:
      uri: /path/to/my/local/model
```

### Steps

1.  **Create a service file (`my_custom_llm_service.py`):**
    This file defines how your model is served.

2.  **Create a `bentofile.yaml`:**
    This file defines the Bento, including the service and the model.

3.  **Build the Bento:**

    ```bash
    bentoml build
    ```

4.  **Serve the Bento:**

    ```bash
    bentoml serve <bento_name>
    ```

This approach provides more control and is ideal for production deployments.
