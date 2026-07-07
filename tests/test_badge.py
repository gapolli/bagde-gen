import pytest
import requests_mock
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from badge_gen import (
    generate_static,
    generate_dynamic,
    build_markdown,
    check_badge_status,
    send_webhook,
)
import badge_gen


def test_static_auto_color():
    res = generate_static("python", "3.12")
    assert "3776AB" in res


def test_build_time_endpoint():
    res = generate_dynamic("build-time", user="pypa", repo="pip", workflow="ci.yml")
    assert "last-commit" in res


def test_visibility_filter_mock():
    url = "https://shields.io"
    with requests_mock.Mocker() as m:
        m.get(url, text="unknown", status_code=200)
        res = build_markdown(url, None, hide_broken=True)
        assert res == ""


def test_markdown_link_embedding():
    url = "https://shields.io"
    link = "https://example.com"
    res = build_markdown(url, link)
    assert res == f"[![Badge]({url})]({link})"


def test_static_fallback_color():
    res = generate_static("linguagem-inexistente", "1.0")
    assert "grey" in res


def test_check_badge_status_success():
    url = "https://shields.io"
    with requests_mock.Mocker() as m:
        m.get(url, text="svg content here", status_code=200)
        assert check_badge_status(url) is True


def test_check_badge_status_network_error():
    url = "https://shields.io"
    with requests_mock.Mocker() as m:
        m.get(url, exc=Exception("Timeout simulado"))
        assert check_badge_status(url) is False


def test_send_webhook_missing_url(monkeypatch):
    monkeypatch.delenv("WEBHOOK_URL", raising=False)
    assert send_webhook("Test", "Hello") is None


def test_send_webhook_success(monkeypatch):
    mock_url = "https://discord.com"
    monkeypatch.setenv("WEBHOOK_URL", mock_url)
    with requests_mock.Mocker() as m:
        m.post(mock_url, status_code=204)
        send_webhook("CI Status", "All tests passed")
        assert m.called
        assert m.last_request.json()["content"] == "**CI Status**: All tests passed"


def test_dynamic_unsupported_type():
    res = generate_dynamic("tipo-invalido-que-nao-existe", user="user", repo="repo")
    assert res == ""


def test_static_with_logo_and_label_color():
    res = generate_static("rust", "1.75", logo="rust", label_color="black")
    assert "logo=rust" in res
    assert "labelColor=black" in res


def test_dynamic_with_custom_style_and_colors():
    res = generate_dynamic(
        "repo-size",
        user="user",
        repo="repo",
        style="flat-square",
        color="red",
        label_color="blue",
    )
    assert "style=flat-square" in res
    assert "color=red" in res
    assert "labelColor=blue" in res


def test_send_webhook_exception_handling(monkeypatch):
    mock_url = "https://discord.com"
    monkeypatch.setenv("WEBHOOK_URL", mock_url)
    with requests_mock.Mocker() as m:
        m.post(mock_url, exc=Exception("Conexão recusada"))
        send_webhook("Title", "Message")
        assert m.called


def test_notify_disabled():
    res = badge_gen.notify("Title", "Message", enabled=False)
    assert res is None


def test_dynamic_complex_mappings():
    """Testa endpoints específicos (Snyk e UptimeRobot) para cobrir o dicionário mapping."""
    res_snyk = generate_dynamic("vulnerability", user="owasp", repo="juice-shop")
    assert "snyk/vulnerabilities/github" in res_snyk

    res_uptime = generate_dynamic("response-time", uptime_key="m778899")
    assert "uptimerobot/region/7/m778899" in res_uptime


@pytest.fixture
def mock_section_json():
    data = [
        {"type": "static", "label": "Docker", "message": "v24", "color": "2496ED"},
        {
            "type": "dynamic",
            "type_param": "vulnerability",
            "user": "awesome-user",
            "repo": "awesome-repo",
        },
    ]
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name
    yield tmp_path
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


def test_main_section_workflow(mock_section_json, monkeypatch, capsys):
    test_args = [
        "badge_gen.py",
        "section",
        "--title",
        "Test Section Header",
        "--file",
        mock_section_json,
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    badge_gen.main()

    captured = capsys.readouterr()
    assert "## Test Section Header" in captured.out
    assert "https://shields.io" in captured.out
    assert "snyk/vulnerabilities/github" in captured.out


def test_main_help_command(monkeypatch, capsys):
    """Testa o comando help na CLI para cobrir as instruções do argparse."""
    test_args = ["badge_gen.py", "help"]
    monkeypatch.setattr(sys, "argv", test_args)
    badge_gen.main()

    captured = capsys.readouterr()
    assert "Usage: badge_gen.py COMMAND" in captured.out


def test_main_static_command(monkeypatch, capsys):
    """Testa o comando static disparado de dentro da main()."""
    test_args = ["badge_gen.py", "static", "--label", "FastAPI", "--message", "0.100"]
    monkeypatch.setattr(sys, "argv", test_args)
    badge_gen.main()

    captured = capsys.readouterr()
    assert "https://shields.io" in captured.out
