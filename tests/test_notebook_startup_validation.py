"""Regression tests for the environment-check notebook wiring."""

import re

from pyprojroot import here


# @spec TUT-INFRA-006
def test_check_notebook_has_env_check_cells() -> None:
    """The env-check cells live in 00_check.py (form before check) with full wiring."""
    notebook_path = here("notebooks/00_check.py")
    source = notebook_path.read_text(encoding="utf-8")

    form_index = source.find("def env_form():")
    check_index = source.find("def env_check(")
    assert form_index != -1, "env_form cell was not found"
    assert check_index != -1, "env_check cell was not found"
    assert form_index < check_index, "env_form must come before env_check"

    assert re.search(r'env_path\s*=\s*Path\(".env"\)', source)
    assert re.search(r'"TUTORIAL_LLM_BASE_URL"', source)
    assert re.search(r'"LLM_MODEL"', source)
    assert re.search(r'os\.getenv\("TUTORIAL_LLM_API_KEY"', source)
    assert re.search(r'endpoint\s*=\s*f"\{base_url\}/chat/completions"', source)
    assert re.search(r"Write \.env from these values", source)
    assert re.search(r"env_path\.write_text\(", source)
    assert re.search(r"load_dotenv\(dotenv_path=env_path,\s*override=True\)", source)
    assert re.search(
        r'mo\.callout\(mo\.md\("✓ Environment ready"\),\s*kind="success"\)', source
    )
    # model name sent to the endpoint must drop the litellm provider prefix
    assert re.search(r'\.split\("/", 1\)\[-1\]', source)
    # readiness gates on a real .env file (not stale process env)
    assert re.search(r"has_env\s*=", source)


def test_intro_notebook_no_longer_has_env_check() -> None:
    """The env-check cells were moved out of 01 into 00_check.py."""
    source = here("notebooks/01_intro_prompting.py").read_text(encoding="utf-8")
    assert "def startup_form():" not in source
    assert "def startup_validation(" not in source
