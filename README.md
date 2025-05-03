# 📚 Chat With Multiple PDFs using Gemini AI 🤖

This Streamlit app allows you to **chat with multiple PDF documents at once** using **Google Gemini AI** (Gemini 1.5/Flash). It's perfect for querying long or complex documents like research papers, eBooks, legal files, and more — all in a conversational format.

---

## 🚀 Features

- ✅ Upload and process **multiple PDFs**
- 💬 Ask questions about the uploaded PDFs
- 🧠 Uses **Google Gemini AI** for intelligent, context-aware answers
- 🔍 Efficient semantic search via FAISS vector store
- ⚡ Choose between different Gemini models (e.g., `gemini-pro`, `gemini-1.5`, or `gemini-2.0-flash`)
- 🔐 Enter your Gemini API key in the sidebar (No hardcoding required!)

---

## 📦 Requirements

All required dependencies are listed in the `requirements.txt` file.

### Install dependencies:

```bash
pip install -r requirements.txt
🔑 Gemini API Setup
Go to Google AI Studio or Google Cloud Console and generate a Gemini API key (Free tier is available).

Launch the app, and paste your API key into the sidebar input.

Select the Gemini model you want to use from the dropdown in the sidebar.

▶️ How to Run the App
bash
Copy code
streamlit run app.py
Then open the URL provided by Streamlit in your browser.

📂 Project Structure
bash
Copy code
chat-pdf/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── faiss_index/            # Auto-generated after processing PDFs
├── .env (optional)         # For local development (not required anymore)
└── README.md               # Project instructions


📝 Notes
The app does not store your API key. It’s only used during your session.

Vector embeddings are stored locally using FAISS and reused for fast question-answering.

When loading saved indexes, the app allows dangerous deserialization assuming files are self-generated and trusted.

You can use the free Gemini API key from Google AI Studio for testing purposes.

📧 Contributions
Pull requests are welcome! If you'd like to improve the design, add more features, or optimize the workflow—feel free to fork and contribute.
