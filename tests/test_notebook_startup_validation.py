"""Regression tests for notebook startup validation wiring."""

import re

from pyprojroot import here


# @spec TUT-INFRA-006
def test_intro_notebook_has_startup_validation_cell() -> None:
    """Ensure startup validation remains present and positioned before intro cells."""
    notebook_path = here("notebooks/01_intro_prompting.py")
    source = notebook_path.read_text(encoding="utf-8")

    startup_index = source.find("def startup_form():")
    validation_index = source.find("def startup_validation(")
    intro_index = source.find("def intro():")
    assert startup_index != -1, "startup_form cell was not found"
    assert validation_index != -1, "startup_validation cell was not found"
    assert intro_index != -1, "intro cell was not found"
    assert startup_index < validation_index < intro_index

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
