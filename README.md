# Project-1-LLM

This project is a simple web chatbot that uses Streamlit for the frontend and FastAPI for the backend to connect to the Google Gemini LLM API.

## Features

* Real-time chat interface.
* Secure API key management.
* Input validation and rate limiting.
* Conversation history within a session.

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Google Gemini API key to the `.env` file:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## How to Run

1.  **Activate the virtual environment:**
    ```bash
    # Windows
    .\\venv\\Scripts\\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    * Start the backend server in one terminal:
        ```bash
        uvicorn app:app --reload
        ```
    * Start the frontend in a second terminal:
        ```bash
        streamlit run streamlit_app.py
        ```

## Troubleshooting

* **`Command not found` error**: Ensure your virtual environment is active.
* **Authentication Error**: Double-check that your `GOOGLE_API_KEY` in the `.env` file is correct.
* **Rate Limit Error**: Wait 60 seconds and try again.
