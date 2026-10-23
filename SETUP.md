# Environment setup

This project requires Python 3.10 or newer and an OpenAI API key. Create an
account and API key at https://platform.openai.com/api-keys.

## Windows PowerShell

From the project directory, create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the following command for the current
terminal session, then activate the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm Python is coming from `.venv`, then install dependencies and configure
the API key:

```powershell
python --version
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="your-api-key"
```

Build the vector database and start the app:

```powershell
python .\ingest.py
python -m streamlit run app.py
```

Run `python .\ingest.py` again whenever you add or update documents in `data/`.

## macOS and Linux

Create and activate a virtual environment, install dependencies, and set your
API key:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
```

Then build the database and launch Streamlit:

```bash
python ingest.py
python -m streamlit run app.py
```

## Troubleshooting

- **`No API key found`**: Set `OPENAI_API_KEY` in the same terminal or host
  environment that runs the app.
- **`No module named ...`**: Activate `.venv` and run
  `python -m pip install -r requirements.txt`.
- **Python version is too old**: Install Python 3.10 or newer and recreate the
  virtual environment with that interpreter.
- **Database write or locking errors**: Stop other running app/ingestion
  processes and ensure the Chroma directory is writable. Set `CHROMA_DB_DIR` to
  a writable directory if needed.
- **Answers are stale after changing documents**: Re-run the ingestion command
  and restart the app.
