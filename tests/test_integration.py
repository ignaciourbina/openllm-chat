import pytest
import requests
import os
import subprocess
import time
import signal

# --- Configuration ---
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5001
FLASK_URL = f"http://{FLASK_HOST}:{FLASK_PORT}"

OPENLLM_HOST = "127.0.0.1"
OPENLLM_PORT = 3001
OPENLLM_URL = f"http://{OPENLLM_HOST}:{OPENLLM_PORT}"

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LOCAL_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'TinyLlama-1.1B-Chat-v1.0'))
VENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv'))

# --- Helper Functions ---
def wait_for_server(url, timeout=180):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server at {url} is ready.")
                return True
        except requests.ConnectionError:
            time.sleep(2)
    return False

# --- Pytest Fixtures ---

@pytest.fixture(scope="module")
def openllm_server():
    """Starts the OpenLLM server with the downloaded model."""
    command = [
        f"{VENV_PATH}/bin/openllm", "serve", MODEL_ID,
        f"--model-dir={LOCAL_MODEL_PATH}",
        "--port", str(OPENLLM_PORT)
    ]
    
    print(f"\nStarting OpenLLM server with command: {' '.join(command)}")
    server_process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid
    )

    if not wait_for_server(f"{OPENLLM_URL}/healthz"):
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        stdout, stderr = server_process.communicate()
        pytest.fail(f"OpenLLM server failed to start.\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}")
    
    yield
    
    print("Tearing down OpenLLM server...")
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    server_process.wait()

@pytest.fixture(scope="module")
def flask_app_server(openllm_server):
    """Starts the Flask app, dependent on the OpenLLM server."""
    env = os.environ.copy()
    env["PORT"] = str(FLASK_PORT)
    env["OPENLLM_BASE_URL"] = f"{OPENLLM_URL}/v1"

    command = [f"{VENV_PATH}/bin/python", "app/app.py"]
    
    print(f"Starting Flask server with command: {' '.join(command)}")
    server_process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, env=env
    )

    if not wait_for_server(FLASK_URL):
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        stdout, stderr = server_process.communicate()
        pytest.fail(f"Flask server failed to start.\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}")
        
    yield
    
    print("Tearing down Flask server...")
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    server_process.wait()

# --- E2E Test ---

def test_e2e_chat_completion(flask_app_server):
    """End-to-end test that verifies a real chat completion."""
    try:
        response = requests.post(f"{FLASK_URL}/chat", json={"message": "What is the capital of France?"}, timeout=20)
        response.raise_for_status()
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] is not None
        assert isinstance(data["response"], str)
        print(f"Received model response: {data['response']}")
        assert "paris" in data["response"].lower()
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to the chat endpoint failed: {e}")
