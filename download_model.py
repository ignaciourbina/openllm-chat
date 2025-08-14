import os
from huggingface_hub import snapshot_download

# --- Configuration ---
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LOCAL_MODEL_DIR = "models"
TARGET_DIR = os.path.join(LOCAL_MODEL_DIR, MODEL_NAME.split('/')[-1]) # e.g., models/TinyLlama-1.1B-Chat-v1.0

def main():
    """
    Downloads a specified Hugging Face model to a local directory.
    """
    print(f"Downloading model: {MODEL_NAME}")
    
    # Create the target directory if it doesn't exist
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")

    # Use snapshot_download to get all the model files
    try:
        snapshot_download(
            repo_id=MODEL_NAME,
            local_dir=TARGET_DIR,
            local_dir_use_symlinks=False, # Set to False to download actual files
            resume_download=True
        )
        print(f"\nModel downloaded successfully to: {TARGET_DIR}")
        print("You can now run the E2E tests or the application with this local model.")
        
    except Exception as e:
        print(f"\nAn error occurred during download: {e}")
        print("Please ensure you have an active internet connection.")
        print("If this is a private model, you may need to log in using 'huggingface-cli login'.")

if __name__ == "__main__":
    main()
