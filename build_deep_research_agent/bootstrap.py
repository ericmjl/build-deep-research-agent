"""Bootstrap command: install Ollama, pull models, write .env, launch notebook 00.

Provides a single ``bootstrap()`` entrypoint that:

1. Installs Ollama (if not present).
2. Starts the Ollama service (if not running).
3. Pulls ``gemma2:2b`` (small model — always, for Parts 1-2).
4. Checks system RAM — if >= 32 GB, pulls ``gemma4:12b`` (large model, Parts 3-5).
5. Writes ``.env`` with local Ollama defaults for both models.
6. Launches ``notebooks/00_check.py`` for final verification.
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import psutil
from loguru import logger

SMALL_MODEL = "gemma2:2b"
LARGE_MODEL = "gemma4:12b"
MIN_RAM_GB = 32

OLLAMA_VERSION_URL = "http://localhost:11434/api/version"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
OLLAMA_V1_URL = "http://localhost:11434/v1"

LOCAL_ENV_TEMPLATE = (
    "LLM_MODEL_SMALL=ollama_chat/{small}\n"
    "LLM_MODEL_LARGE=ollama_chat/{large}\n"
    "TUTORIAL_LLM_BASE_URL={base_url}\n"
    "TUTORIAL_LLM_API_KEY=ollama-no-auth\n"
)


def is_ollama_installed() -> bool:
    """Check if the ``ollama`` binary is on PATH.

    :returns: True if ollama is found.
    """
    return shutil.which("ollama") is not None


def is_ollama_running() -> bool:
    """Check if the Ollama service is responding on localhost.

    :returns: True if ``/api/version`` returns 200.
    """
    try:
        req = urllib.request.Request(OLLAMA_VERSION_URL, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except (urllib.error.URLError, ConnectionError, OSError):
        return False


def install_ollama() -> bool:
    """Install Ollama for the current platform.

    :returns: True if installation succeeded.
    """
    # @spec TUT-BOOT-002
    system = platform.system()
    if system == "Darwin":
        if shutil.which("brew"):
            logger.info("Installing Ollama via Homebrew...")
            subprocess.run(["brew", "install", "ollama"], check=True)
        else:
            logger.info("Installing Ollama via install script...")
            subprocess.run(
                "curl -fsSL https://ollama.com/install.sh | sh",
                shell=True,
                check=True,
            )
    elif system == "Linux":
        logger.info("Installing Ollama via install script...")
        subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            check=True,
        )
    elif system == "Windows":
        if shutil.which("winget"):
            logger.info("Installing Ollama via winget...")
            subprocess.run(["winget", "install", "Ollama.Ollama"], check=True)
        else:
            logger.error(
                "winget not found. Please install Ollama manually from "
                "https://ollama.com"
            )
            return False
    else:
        logger.error(f"Unsupported platform: {system}")
        return False
    return True


def start_ollama() -> None:
    """Start the Ollama service in the background and wait for it."""
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        if is_ollama_running():
            logger.info("Ollama is running")
            return
        time.sleep(1)
    logger.warning("Ollama did not start within 30 seconds")


def list_ollama_models() -> list[str]:
    """List models available in the local Ollama instance.

    :returns: List of model names.
    """
    try:
        req = urllib.request.Request(OLLAMA_TAGS_URL, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [m["name"] for m in data.get("models", [])]
    except Exception:  # noqa: BLE001
        return []


def has_model(name: str) -> bool:
    """Check if a specific model is pulled in Ollama.

    :param name: Model name (e.g. ``gemma2:2b``).
    :returns: True if the model is available.
    """
    models = list_ollama_models()
    return any(m == name or m.startswith(name + ":") for m in models)


def pull_model(name: str) -> bool:
    """Pull a model from the Ollama registry.

    :param name: Model name to pull.
    :returns: True if pull succeeded.
    """
    logger.info(f"Pulling {name}...")
    try:
        subprocess.run(["ollama", "pull", name], check=True)
        logger.info(f"Done: {name}")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"Failed to pull {name}: {exc}")
        return False


def get_ram_gb() -> float:
    """Get total system RAM in GB.

    :returns: Total RAM, or 0.0 if measurement fails.
    """
    try:
        return psutil.virtual_memory().total / (1024**3)
    except Exception:  # noqa: BLE001
        return 0.0


def write_env(project_root: Path) -> None:
    """Write ``.env`` with local Ollama defaults for both models.

    :param project_root: Project root directory (where ``.env`` lives).
    """
    # @spec TUT-BOOT-005
    env_path = project_root / ".env"
    content = LOCAL_ENV_TEMPLATE.format(
        small=SMALL_MODEL,
        large=LARGE_MODEL,
        base_url=OLLAMA_V1_URL,
    )
    env_path.write_text(content, encoding="utf-8")
    logger.info(f"Wrote {env_path}")


def launch_notebook_00(project_root: Path) -> None:
    """Launch ``marimo edit notebooks/00_check.py``.

    :param project_root: Project root directory.
    """
    notebook = project_root / "notebooks" / "00_check.py"
    logger.info(f"Launching {notebook}...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "marimo",
            "edit",
            "--no-sandbox",
            "--no-token",
            str(notebook),
        ],
    )


def bootstrap(project_root: Path | None = None) -> None:
    """Run the full bootstrap sequence.

    1. Install Ollama (if not present).
    2. Start Ollama (if not running).
    3. Pull ``gemma2:2b`` (small model — always).
    4. Check RAM → pull ``gemma4:12b`` (large model) if >= 32 GB.
    5. Write ``.env`` with local Ollama defaults.
    6. Launch notebook 00 for verification.

    :param project_root: Project root directory. Defaults to auto-detection
        via :mod:`pyprojroot`.
    """
    # @spec TUT-BOOT-001
    if project_root is None:
        from pyprojroot import here

        project_root = here()

    # Step 1: Install Ollama
    if not is_ollama_installed():
        logger.info("Ollama not found — installing...")
        if not install_ollama():
            logger.error(
                "Failed to install Ollama. "
                "Please install manually from https://ollama.com"
            )
            return
    else:
        logger.info("Ollama is installed")

    # Step 2: Start Ollama if not running
    if not is_ollama_running():
        logger.info("Starting Ollama...")
        start_ollama()
    else:
        logger.info("Ollama is running")

    # Step 3: Pull small model (always)
    if not has_model(SMALL_MODEL):
        if not pull_model(SMALL_MODEL):
            logger.error(
                f"Failed to pull {SMALL_MODEL}. "
                "The tutorial needs this model for Parts 1-2."
            )
            return
    else:
        logger.info(f"{SMALL_MODEL} already pulled")

    # Step 4: Check RAM and pull large model if possible
    ram_gb = get_ram_gb()
    if ram_gb >= MIN_RAM_GB:
        if not has_model(LARGE_MODEL):
            pull_model(LARGE_MODEL)
        else:
            logger.info(f"{LARGE_MODEL} already pulled")
    elif ram_gb > 0:
        logger.warning(
            f"System RAM {ram_gb:.1f} GB < {MIN_RAM_GB} GB — skipping {LARGE_MODEL}. "
            f"Parts 3-5 will need the remote Modal endpoint "
            f"(switch to 'Remote' in notebook 00)."
        )
    else:
        logger.warning(
            f"Could not measure RAM — skipping {LARGE_MODEL} auto-pull. "
            f"If you have >= {MIN_RAM_GB} GB, run: ollama pull {LARGE_MODEL}"
        )

    # Step 5: Write .env
    write_env(project_root)

    # Step 6: Launch notebook 00
    logger.info("Launching notebook 00 for env verification...")
    launch_notebook_00(project_root)
