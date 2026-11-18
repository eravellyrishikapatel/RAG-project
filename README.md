# PDF Chatbot with RAG

Ask questions about a PDF using local embeddings and ChromaDB. The default
answer mode is local and does not require an API key. On the first run,
Sentence Transformers downloads the `all-MiniLM-L6-v2` embedding model.

## Requirements

- Python 3.12
- Git

## Install and run

Clone the repository and enter its folder:

```bash
git clone https://github.com/eravellyrishikapatel/RAG-project.git
cd RAG-project
```

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Ask questions in the terminal. Type `exit` to quit.

## Use your own PDF

Replace `data/sample.pdf` with the PDF you want to query, keeping the filename
`sample.pdf`, then run `app.py` from the repository folder. The app builds its
local vector database when it starts.

## Answer modes

- **Local (default):** No API key or paid service is required. The app selects
  relevant sentences from the retrieved PDF text.
- **Optional OpenRouter:** Set `OPENROUTER_API_KEY` in a local `.env` file to
  use the configured OpenRouter model. Check the provider's current model
  availability and pricing before enabling it. Never commit your `.env` file.

The embedding model is downloaded from Hugging Face on first run, so an
internet connection is needed initially. After it is cached, local embeddings
run on your computer.
