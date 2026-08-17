# CareerGraph AI Backend

The backend API foundation for CareerGraph AI.

## Run locally

From this directory, create a Python 3.12 virtual environment, install the
project with development dependencies, and start Uvicorn:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m uvicorn careergraph.main:app --reload
```

The health endpoint is available at `http://127.0.0.1:8000/health`.

## Test

```powershell
python -m pytest
```

