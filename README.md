# AI Research Assistant

## Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

Install `uv` if you haven't already:

```bash
pip install uv
```

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-research-assistant
```

### 2. Create a virtual environment

```bash
uv venv
```

This creates a `.venv` directory in the project root.

### 3. Activate the virtual environment

**Windows (PowerShell)**
```powershell
.venv\Scripts\activate
```

**Windows (Command Prompt)**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Once activated, your terminal prompt will be prefixed with `(.venv)`.

### 4. Install dependencies

```bash
uv sync
```

### 5. Run the project

```bash
python main.py
```

### Deactivate the virtual environment

When you are done, deactivate the virtual environment by running:

```bash
deactivate
```
