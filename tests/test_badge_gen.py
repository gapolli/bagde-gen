import pytest
import requests_mock
import os
from badge_gen import generate_static, generate_dynamic, build_markdown

def test_static_auto_color():
    # Verify that the script correctly maps brand colors
    res = generate_static("Python", "3.12")
    assert "3776AB" in res

def test_build_time_endpoint():
    res = generate_dynamic("build-time", user="pypa", repo="pip", workflow="ci.yml")
    assert "run-duration" in res

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
