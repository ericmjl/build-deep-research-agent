"""Regression tests for the environment-check notebook wiring."""

import re

from pyprojroot import here


# @spec TUT-INFRA-006
def test_check_notebook_has_env_check_cells() -> None:
    """The env-check cells live in 00_check.py (form before check) with full wiring."""
    notebook_path = here("notebooks/00_check.py")
    source = notebook_path.read_text(encoding="utf-8")

    # New cell names: detect_ollama -> choice_form -> env_check
    detect_index = source.find("def detect_ollama(")
    form_index = source.find("def choice_form(")
    check_index = source.find("def env_check(")
    assert detect_index != -1, "detect_ollama cell was not found"
    assert form_index != -1, "choice_form cell was not found"
    assert check_index != -1, "env_check cell was not found"
    assert detect_index < form_index, "detect_ollama must come before choice_form"
    assert form_index < check_index, "choice_form must come before env_check"

    assert re.search(r'env_path\s*=\s*Path\(".env"\)', source)
    assert re.search(r'"TUTORIAL_LLM_BASE_URL"', source)
    assert re.search(r'"LLM_MODEL"', source)
    assert re.search(r'os\.getenv\("TUTORIAL_LLM_API_KEY"', source)
    assert re.search(r'endpoint\s*=\s*f"\{base_url\}/chat/completions"', source)
    assert re.search(r"Write \.env and test", source)
    assert re.search(r"env_path\.write_text\(", source)
    assert re.search(r"load_dotenv\(dotenv_path=env_path,\s*override=True\)", source)
    # Local Ollama detection
    assert re.search(r"OLLAMA_TAGS_URL", source), "must probe local Ollama"
    assert re.search(r"gemma4:12b", source), "must reference gemma4:12b"
    assert re.search(r"psutil", source), "must check system resources"
    # model name sent to the endpoint must drop the litellm provider prefix
    assert re.search(r'\.split\("/", 1\)\[-1\]', source)
    # readiness gates on a real .env file (not stale process env)
    assert re.search(r"has_env\s*=", source)


def test_intro_notebook_no_longer_has_env_check() -> None:
    """The env-check cells were moved out of 01 into 00_check.py."""
    source = here("notebooks/01_intro_prompting.py").read_text(encoding="utf-8")
    assert "def startup_form():" not in source
    assert "def startup_validation(" not in source
