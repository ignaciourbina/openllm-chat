# Gemini Project: OpenLLM Chat

This document provides a comprehensive overview of the OpenLLM Chat project, its structure, and instructions for building, running, and interacting with it.

## Project Overview

This project is a web-based chat application that leverages the power of Large Language Models (LLMs) through the OpenLLM framework. The application is built with a Python backend using the Flask web framework and interacts with a running OpenLLM instance via the Langchain library.

The core functionality involves:

-   A simple web interface for users to input chat messages.
-   A Flask backend that receives user messages.
-   Integration with Langchain to process these messages and send them to a designated LLM.
-   Real-time responses from the LLM displayed back to the user in the web interface.

### Key Technologies

-   **Backend:** Python, Flask
-   **LLM Interaction:** Langchain, OpenLLM
-   **Frontend:** HTML, CSS, JavaScript (as per the project structure)
-   **Dependency Management:** pip, venv

## Building and Running the Project

The project includes shell scripts to streamline the setup and execution process.

### 1. Installation

To install the necessary dependencies, run the following command from the project root:

```bash
./install_deps.sh
```

This script will:

1.  Create a Python virtual environment in the `venv/` directory if it doesn't exist.
2.  Activate the virtual environment.
3.  Install the Python packages listed in `requirements.txt`.
4.  It also intelligently checks for changes in `requirements.txt` to avoid unnecessary re-installations.

### 2. Running the Application

To start the chat application, you first need to have an OpenLLM server running.

**Start the OpenLLM Server:**

Follow the [OpenLLM documentation](https://docs.bentoml.com/openllm/concepts/llm_runners) to serve your desired model. For example, to serve the "dolly-v2" model, you would run:

```bash
openllm start dolly-v2
```

**Start the Flask Server:**

Once the OpenLLM server is running, you can start the Flask application with this command:

```bash
./start_server.sh
```

This script will:

1.  Ensure dependencies are up-to-date by calling `install_deps.sh`.
2.  Activate the virtual environment.
3.  Navigate into the `app/` directory.
4.  Run the Flask application (`app.py`).

After running the script, you can access the chat application in your web browser at `http://127.0.0.1:5000`.

## Development Conventions

-   **Backend Logic:** All backend and server-side logic is contained within `app/app.py`. This includes Flask routes, LLM interaction, and handling of chat requests.
-   **Frontend Files:** The frontend is structured with `index.html` in the `app/templates/` directory, and `style.css` and `script.js` in the `app/static/` directory.
-   **Virtual Environment:** All dependencies are managed within a virtual environment located in the `venv/` directory. Remember to activate it (`source venv/bin/activate`) when working on the project.
-   **Configuration:** The LLM model and connection details are configured in `app/app.py`. You may need to modify the `OpenLLM()` instantiation to point to your specific model and OpenLLM server address.
