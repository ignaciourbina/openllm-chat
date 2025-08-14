# OpenLLM Chat with Flask and Langchain

This project provides a skeleton for a chat application using Flask as the web framework, Langchain for interacting with Large Language Models (LLMs), and OpenLLM for serving the LLM.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd openllm_chat
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start OpenLLM Server:**
    Before running this application, you need to have an OpenLLM server running with your desired model. Refer to the [OpenLLM documentation](https://docs.bentoml.com/openllm/concepts/llm_runners) for instructions on how to serve a model.
    
    Example (serving Dolly V2):
    ```bash
    openllm start dolly-v2
    ```
    Ensure the OpenLLM server is accessible from where you run this Flask application.

4.  **Run the Flask Application:**
    ```bash
    ./start_server.sh
    ```

## Usage

Once the Flask server is running, open your web browser and navigate to `http://127.0.0.1:5000` (or the address where your Flask app is hosted).

## Project Structure

```
openllm_chat/
├── app/
│   ├── templates/
│   │   └── index.html (To be created)
│   ├── static/
│   │   └── style.css (To be created)
│   │   └── script.js (To be created)
│   └── app.py
├── requirements.txt
├── start_server.sh
└── README.md
```

## Next Steps

-   Create `app/templates/index.html` for the chat interface.
-   Create `app/static/style.css` for styling.
-   Create `app/static/script.js` for client-side chat logic.
-   Further configure `app/app.py` to connect to your specific OpenLLM instance and model.
