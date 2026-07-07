import pytest
import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import badge_gen


@pytest.fixture
def clean_env():
    """Ensures isolation by temporarily clearing the .env file before and after the tests."""
    env_path = ".env"
    backup_data = None
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            backup_data = f.read()
        os.remove(env_path)

    yield env_path

    if os.path.exists(env_path):
        os.remove(env_path)
    if backup_data is not None:
        with open(env_path, "w") as f:
            f.write(backup_data)


def test_integration_setup_command(clean_env, monkeypatch):
    """Tests the setup command by simulating real user inputs in the terminal (stdin)."""
    simulated_inputs = iter(
        ["gh_token_abc123", "snyk_token_xyz789", "https://discord.com"]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(simulated_inputs))
    monkeypatch.setattr(sys, "argv", ["badge_gen.py", "setup"])
    badge_gen.main()

    assert os.path.exists(clean_env)
    with open(clean_env, "r") as f:
        content = f.read()
        assert "GITHUB_TOKEN='gh_token_abc123'" in content
        assert "SNYK_TOKEN='snyk_token_xyz789'" in content
        assert "WEBHOOK_URL='https://discord.com'" in content


def test_integration_static_badge_append_to_file(monkeypatch):
    """Tests the actual recording by simulating a full CLI call with the `--output` flag."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as tmp_file:
        output_path = tmp_file.name

    try:
        test_args = [
            "badge_gen.py",
            "static",
            "--label",
            "java",
            "--message",
            "17",
            "--output",
            output_path,
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        badge_gen.main()

        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            file_content = f.read()
            assert "https://shields.io" in file_content
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def test_integration_complete_pipeline_flow(monkeypatch, capsys):
    """Tests the end-to-end flow by calling the dynamic command and verifying the output in the CLI."""
    test_args = [
        "badge_gen.py",
        "dynamic",
        "--type",
        "repo-size",
        "--user",
        "python",
        "--repo",
        "cpython",
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    badge_gen.main()

    captured = capsys.readouterr()
    assert "https://shields.io" in captured.out
