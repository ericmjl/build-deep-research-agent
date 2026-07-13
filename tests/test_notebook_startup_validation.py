"""Regression tests for the environment-check notebook wiring."""

import re

from pyprojroot import here


# @spec TUT-INFRA-006
def test_check_notebook_has_env_check_cells() -> None:
    """The env-check cells live in 00_check.py (form before check) with full wiring."""
    notebook_path = here("notebooks/00_check.py")
    source = notebook_path.read_text(encoding="utf-8")

    # Cell flow: detect_local -> choice_form -> lms_model_picker -> env_check
    detect_index = source.find("def detect_local(")
    form_index = source.find("def choice_form(")
    picker_index = source.find("def lms_model_picker(")
    check_index = source.find("def env_check(")
    assert detect_index != -1, "detect_local cell was not found"
    assert form_index != -1, "choice_form cell was not found"
    assert picker_index != -1, "lms_model_picker cell was not found"
    assert check_index != -1, "env_check cell was not found"
    assert detect_index < form_index, "detect_local must come before choice_form"
    assert form_index < picker_index, "choice_form must come before lms_model_picker"
    assert picker_index < check_index, "lms_model_picker must come before env_check"

    assert re.search(r'env_path\s*=\s*Path\(".env"\)', source)
    assert re.search(r'"TUTORIAL_LLM_BASE_URL"', source)
    assert re.search(r'"LLM_MODEL_SMALL"', source), "must reference LLM_MODEL_SMALL"
    assert re.search(r'"LLM_MODEL_LARGE"', source), "must reference LLM_MODEL_LARGE"
    # TUTORIAL_LLM_API_KEY is written to .env for the local path
    assert re.search(r"TUTORIAL_LLM_API_KEY", source)
    assert re.search(r"Write \.env and test", source)
    assert re.search(r"env_path\.write_text\(", source)
    assert re.search(r"load_dotenv\(dotenv_path=env_path,\s*override=True\)", source)
    # SimpleBot integration test (replaces raw HTTP ping)
    assert re.search(r"from llamabot import SimpleBot", source), "must call SimpleBot"
    # Local Ollama detection
    assert re.search(r"OLLAMA_TAGS_URL", source), "must probe local Ollama"
    assert re.search(r"gemma4:12b", source), "must reference gemma4:12b"
    assert re.search(r"gemma2:2b", source), "must reference gemma2:2b"
    assert re.search(r"psutil", source), "must check system resources"
    assert re.search(r"ollama_chat/", source), "must use ollama_chat prefix for local"
    # LM Studio detection (second-priority local backend)
    assert re.search(r"LMSTUDIO_V1_URL", source), "must probe local LM Studio"
    assert re.search(r"LMSTUDIO_MODELS_URL", source), "must query LM Studio /v1/models"
    assert re.search(r"google/gemma-2-2b-it", source), (
        "must reference LM Studio small model"
    )
    assert re.search(r"google/gemma-3-12b-it", source), (
        "must reference LM Studio large model"
    )
    # readiness gates on a real .env file (not stale process env)
    assert re.search(r"has_env\s*=", source)


def test_intro_notebook_no_longer_has_env_check() -> None:
    """The env-check cells were moved out of 01 into 00_check.py."""
    source = here("notebooks/01_intro_prompting.py").read_text(encoding="utf-8")
    assert "def startup_form():" not in source
    assert "def startup_validation(" not in source
