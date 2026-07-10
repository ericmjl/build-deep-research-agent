from pathlib import Path


# @spec TUT-INFRA-006
def test_intro_notebook_has_startup_validation_cell() -> None:
    notebook_path = Path("notebooks/01_intro_prompting.py")
    source = notebook_path.read_text(encoding="utf-8")

    startup_index = source.index("def startup_validation():")
    intro_index = source.index("def intro():")
    assert startup_index < intro_index

    assert 'env_path = Path(".env")' in source
    assert '"TUTORIAL_LLM_BASE_URL"' in source
    assert '"TUTORIAL_LLM_API_KEY"' in source
    assert '"LLM_MODEL"' in source
    assert 'endpoint = f"{base_url}/chat/completions"' in source
    assert 'mo.callout(mo.md("✓ Environment ready"), kind="success")' in source
