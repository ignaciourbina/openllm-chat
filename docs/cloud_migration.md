# Migrating to a Cloud-Based LLM Inference Provider

This document outlines the steps required to migrate the OpenLLM Chat application from a local inference setup to a cloud-based provider. This approach is recommended when local hardware is insufficient for running larger, more capable models.

## 1. Choosing a Cloud Provider

The first step is to select a cloud GPU provider that fits your budget and performance needs. Based on our research, here are some of the most cost-effective options for deep learning workloads:

| Provider | Key Features |
|---|---|
| **Vast.ai** | Marketplace model with potentially the lowest prices, pay-per-use billing. |
| **RunPod** | Secure and Community Cloud options, serverless deployments, easy-to-use interface. |
| **TensorDock** | Marketplace model, competitive pricing, wide selection of GPUs. |
| **Hyperstack** | On-demand, reserved, and spot instances, focuses on high-performance computing. |
| **Lambda Labs** | Geared towards AI and deep learning, offers both on-demand and reserved instances. |
| **Genesis Cloud** | Focus on large-scale, multi-GPU setups, 100% green energy. |

**Recommendation:** For most users, **RunPod** or **Vast.ai** will offer the best balance of price and performance.

## 2. Setting up the Cloud Instance

Once you've chosen a provider, you'll need to set up a new cloud instance. The general steps are as follows:

1.  **Create an account** with your chosen provider.
2.  **Add a payment method.**
3.  **Deploy a new instance (or "Pod"):**
    *   Select a GPU that meets the memory requirements of your desired model (e.g., an NVIDIA A100 for large models).
    *   Choose a template with a pre-installed PyTorch or TensorFlow environment. This will save you time on setup.
    *   Set a password for SSH access.
4.  **Connect to your instance** via SSH. Your provider will give you the necessary connection details (IP address, port, and username).

## 3. Migrating the Application

With your cloud instance running, you can now migrate the OpenLLM Chat application.

### 3.1. Clone the Repository

Connect to your cloud instance via SSH and clone the project repository:

```bash
git clone https://github.com/your-username/openllm-chat.git
cd openllm-chat
```

### 3.2. Install Dependencies

Run the `install_deps.sh` script to create a virtual environment and install the necessary Python packages:

```bash
./install_deps.sh
```

### 3.3. Start the OpenLLM Server

You can now start the OpenLLM server on your cloud instance. You'll need to choose a model that is compatible with your selected GPU. For example, to run the `llama-3.1-8b-instruct` model, you would use the following command:

```bash
source venv/bin/activate
openllm start meta-llama/Llama-3.1-8b-instruct
```

**Note:** You may need to log in to Hugging Face to access certain models.

### 3.4. Expose the OpenLLM Port

By default, the OpenLLM server runs on port 3000. You'll need to expose this port so that your local Flask application can connect to it. Your cloud provider will have instructions on how to do this.

## 4. Modifying the Local Application

The final step is to modify your local Flask application to connect to the remote OpenLLM server.

### 4.1. Update `app.py`

Open `app/app.py` and find the following line:

```python
llm = OpenLLM(server_url="http://localhost:3000")
```

Change `localhost` to the IP address of your cloud instance:

```python
llm = OpenLLM(server_url="http://<your-cloud-instance-ip>:3000")
```

### 4.2. Run the Local Server

You can now start your local Flask server:

```bash
./start_server.sh
```

Your chat application will now be running locally, but all LLM inference will be handled by your powerful cloud instance. This allows you to run large, state-of-the-art models without needing expensive local hardware.
