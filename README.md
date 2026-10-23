# Ironharbor Fitness Assistant

A retrieval-augmented chatbot that answers questions about Ironharbor Fitness
using its gym documents. Answers are grounded in retrieved passages and include
source citations.

## Quick start

Requirements: Python 3.10 or newer and an OpenAI API key.

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies and set your API key:

   ```powershell
   python -m pip install -r requirements.txt
   $env:OPENAI_API_KEY="your-api-key"
   ```

3. Build the searchable document database and launch the app:

   ```powershell
   python .\ingest.py
   python -m streamlit run app.py
   ```

To use a different shell, activate the virtual environment using that shell's
standard activation command and set `OPENAI_API_KEY` in the environment where
the app will run.

## Project files

| File or folder | Purpose |
| --- | --- |
| `app.py` | Streamlit chat interface |
| `chatbot.py` | Agent, document search, response instructions, and citations |
| `ingest.py` | Loads documents and builds the Chroma vector database |
| `evaluate.py` | Runs answer-faithfulness and completeness evaluations |
| `trace.py` | Prints the retrieval and response steps for one question |
| `test_questions.json` | Evaluation questions and expected answers |
| `data/` | Gym knowledge-base documents |

## Updating the knowledge base

Add or replace `.pdf`, `.md`, and `.txt` files anywhere under `data/`
(including subfolders such as `data/exercises/`), then rebuild the index:

```powershell
python .\ingest.py
```

The app and evaluator use the index in the system temporary directory by
default. Set `CHROMA_DB_DIR` to use another writable location. Restart the app
after rebuilding.

## Evaluate answers

```powershell
python .\evaluate.py
```

Each question is checked for faithfulness to its cited sources and completeness
against its expected answer. Evaluation requires OpenAI access for the chat,
embedding, and judge model calls.

## Deploy

The app can be deployed to Streamlit Community Cloud or another Streamlit host.
Configure `OPENAI_API_KEY` in the host's secrets/environment settings. Ensure
the host can write to the configured Chroma database directory; if not, set
`CHROMA_DB_DIR` to a writable path.
