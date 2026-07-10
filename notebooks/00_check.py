# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "python-dotenv",
# ]
# ///

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo


@app.cell(hide_code=True)
def title():
    mo.md("""
    # Environment check

    Verify your tutorial LLM endpoint before starting the notebooks. This checks
    for a `.env` with `LLM_MODEL` and `TUTORIAL_LLM_BASE_URL`, offers a form to
    write one from the README defaults, and pings the endpoint.

    Once you see **✓ Environment ready**, continue to `01_intro_prompting`.
    """)
    return


@app.cell(hide_code=True)
def env_form():
    import json
    import os
    from pathlib import Path
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    from dotenv import load_dotenv

    # @spec TUT-INFRA-006
    env_path = Path(".env")

    readme_defaults = {
        "LLM_MODEL": "",
        "TUTORIAL_LLM_BASE_URL": "",
    }
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_lines = readme_path.read_text(encoding="utf-8").splitlines()
        for line in readme_lines:
            if "=" not in line:
                continue
            key, sep, value = line.partition("=")
            if key in readme_defaults:
                readme_defaults[key] = value.strip()

    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)

    required_vars = (
        "TUTORIAL_LLM_BASE_URL",
        "LLM_MODEL",
    )
    env_values = {name: os.getenv(name, "").strip() for name in required_vars}

    base_url_input = mo.ui.text(
        value=env_values["TUTORIAL_LLM_BASE_URL"]
        or readme_defaults["TUTORIAL_LLM_BASE_URL"],
        label="TUTORIAL_LLM_BASE_URL",
        full_width=True,
    )
    model_input = mo.ui.text(
        value=env_values["LLM_MODEL"] or readme_defaults["LLM_MODEL"],
        label="LLM_MODEL",
        full_width=True,
    )
    save_env = mo.ui.run_button(label="Write .env from these values")

    mo.vstack([base_url_input, model_input, save_env])
    return (
        HTTPError,
        Request,
        URLError,
        base_url_input,
        env_path,
        json,
        load_dotenv,
        model_input,
        os,
        required_vars,
        save_env,
        urlopen,
    )


@app.cell(hide_code=True)
def env_check(
    HTTPError,
    Request,
    URLError,
    base_url_input,
    env_path,
    json,
    load_dotenv,
    model_input,
    os,
    required_vars,
    save_env,
    urlopen,
):
    if save_env.value:
        lines = [
            f"LLM_MODEL={model_input.value.strip()}",
            f"TUTORIAL_LLM_BASE_URL={base_url_input.value.strip()}",
        ]
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        load_dotenv(dotenv_path=env_path, override=True)

    active_values = {name: os.getenv(name, "").strip() for name in required_vars}
    has_env = (
        env_path.exists()
        and bool(active_values["LLM_MODEL"])
        and bool(active_values["TUTORIAL_LLM_BASE_URL"])
    )

    result = None
    if not has_env:
        result = mo.callout(
            mo.md(
                "❌ **Environment not ready**\n\n"
                "No `.env` with `LLM_MODEL` and `TUTORIAL_LLM_BASE_URL` is set. "
                "Fill in the values above and click **Write .env from these values**."
            ),
            kind="danger",
        )
    else:
        model_name = active_values["LLM_MODEL"].split("/", 1)[-1]
        base_url = active_values["TUTORIAL_LLM_BASE_URL"].rstrip("/")
        endpoint = f"{base_url}/chat/completions"

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": "Reply with READY."}],
            "max_tokens": 8,
            "temperature": 0,
        }
        headers = {"Content-Type": "application/json"}
        auth_key = os.getenv("TUTORIAL_LLM_API_KEY", "").strip()
        if auth_key:
            headers["Authorization"] = "Bearer " + auth_key
        request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        ENDPOINT_PING_TIMEOUT_SECONDS = 90

        try:
            with urlopen(request, timeout=ENDPOINT_PING_TIMEOUT_SECONDS) as resp:
                status_code = resp.status
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace").strip()
            error_detail = (
                f"\n\nEndpoint response snippet:\n```\n{error_body[:400]}\n```"
                if error_body
                else ""
            )
            result = mo.callout(
                mo.md(
                    "❌ **Environment not ready**\n\n"
                    f"LLM endpoint ping failed with HTTP status `{exc.code}`."
                    f"{error_detail}\n\n"
                    "**Fix:**\n"
                    "- Verify `TUTORIAL_LLM_BASE_URL` points to a running OpenAI-compatible `/v1` endpoint.\n"
                    "- Verify `LLM_MODEL` is available on that endpoint.\n"
                    "- Edit the values above and click **Write .env from these values** to retry."
                ),
                kind="danger",
            )
        except URLError as exc:
            reason = str(exc.reason) if getattr(exc, "reason", None) else str(exc)
            result = mo.callout(
                mo.md(
                    "❌ **Environment not ready**\n\n"
                    f"Could not reach the configured LLM endpoint (`{reason}`).\n\n"
                    "**Fix:** Verify `TUTORIAL_LLM_BASE_URL` and your network connection, then click "
                    "**Write .env from these values** to retry."
                ),
                kind="danger",
            )
        except TimeoutError:
            result = mo.callout(
                mo.md(
                    "❌ **Environment not ready**\n\n"
                    f"The endpoint did not respond within {ENDPOINT_PING_TIMEOUT_SECONDS}s — it is likely "
                    "cold-starting (the shared Modal container spins down when idle). Wait ~30s for it to "
                    "wake, then click **Write .env from these values** to retry."
                ),
                kind="danger",
            )
        else:
            if 200 <= status_code < 300:
                result = mo.callout(mo.md("✓ Environment ready"), kind="success")
            else:
                result = mo.callout(
                    mo.md(
                        "❌ **Environment not ready**\n\n"
                        f"LLM endpoint ping returned unexpected status `{status_code}`.\n\n"
                        "**Fix:** Confirm endpoint availability and credentials, then retry."
                    ),
                    kind="danger",
                )

    result
    return


if __name__ == "__main__":
    app.run()
