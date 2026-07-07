#!/usr/bin/env python3
"""Badge Generator Tool - Minimal argparse version."""

import argparse
import urllib.parse
import json
import sys
import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

LANG_COLORS = {
    "python": "3776AB",
    "javascript": "F7DF1E",
    "typescript": "3178C6",
    "rust": "DEA584",
    "java": "007396",
    "go": "00ADD8",
    "php": "777BB4",
    "ruby": "CC342D",
    "swift": "F05138",
    "kotlin": "7F52FF",
    "dart": "0175C2",
}


def send_webhook(title, message):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return
    data = {"content": f"**{title}**: {message}"}
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except Exception:
        pass


def notify(title, message, enabled=True):
    if not enabled:
        return
    send_webhook(title, message)
    try:
        if sys.platform == "win32":
            from win10toast import ToastNotifier

            ToastNotifier().show_toast(title, message, duration=5)
        elif sys.platform == "darwin":
            os.system(
                f'osascript -e \'display notification "{message}" with title "{title}"\''
            )
        else:
            os.system(f"notify-send '{title}' '{message}'")
    except Exception:
        pass


def check_badge_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200 and "unknown" not in response.text.lower()
    except Exception:
        return False


def build_markdown(url, link, hide_broken=False):
    if hide_broken and not check_badge_status(url):
        return ""
    return f"[![Badge]({url})]({link})" if link else f"![Badge]({url})"


def generate_static(
    label,
    message,
    color=None,
    logo=None,
    style="for-the-badge",
    link=None,
    hide_broken=False,
    label_color=None,
):
    final_color = color if color else LANG_COLORS.get(label.lower(), "grey")
    label_esc = urllib.parse.quote(label.replace("-", "--"))
    msg_esc = urllib.parse.quote(message.replace("-", "--"))
    url = f"https://shields.io/badge/{label_esc}-{msg_esc}-{final_color}?style={style}"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    if label_color:
        url += f"&labelColor={label_color}"
    return build_markdown(url, link, hide_broken)


def generate_dynamic(
    b_type,
    user=None,
    repo=None,
    pkg=None,
    workflow=None,
    path=None,
    uptime_key=None,
    style="for-the-badge",
    link=None,
    hide_broken=False,
    label_color=None,
    color=None,
):
    params = {"style": style}
    if label_color:
        params["labelColor"] = label_color
    if color:
        params["color"] = color

    mapping = {
        "actions": f"github/actions/status/user/{user}/{repo}",
        "build-time": f"github/last-commit/{user}/{repo}",
        "repo-size": f"github/repo-size/{user}/{repo}",
        "file-size": f"github/size/{user}/{repo}/{path or ''}",
        "vulnerability": f"snyk/vulnerabilities/github/{user}/{repo}",
        "license": f"github/license/{user}/{repo}",
        "views": f"github/stars/{user}/{repo}",
        "clones": f"github/downloads/{user}/{repo}/total",
        "top-lang": f"github/languages/top/{user}/{repo}",
        "lang-count": f"github/languages/count/{user}/{repo}",
        "response-time": f"uptimerobot/region/7/{uptime_key or ''}",
        "codecov": f"codecov/c/github/{user}/{repo}",
    }

    if b_type not in mapping:
        return ""
    url = f"https://shields.io/{mapping[b_type]}"
    query_params = urllib.parse.urlencode(params)
    if query_params:
        url += "?" + query_params
    return build_markdown(url, link, hide_broken)


def setup_env():
    path = ".env"
    if not os.path.exists(path):
        open(path, "w").close()
    set_key(path, "GITHUB_TOKEN", input("GitHub Token: "))
    set_key(path, "SNYK_TOKEN", input("Snyk Token: "))
    set_key(path, "WEBHOOK_URL", input("Webhook URL: "))
    print("Environment setup completed.")


def main():
    parser = argparse.ArgumentParser(prog="badge_gen.py", add_help=False)
    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        help="Command to run: setup, static, dynamic, section, help",
    )
    parser.add_argument("--no-notify", action="store_true")
    parser.add_argument("--hide-broken", action="store_true")

    # Static args
    parser.add_argument("--label")
    parser.add_argument("--message")
    parser.add_argument("--color")
    parser.add_argument("--label-color")
    parser.add_argument("--logo")
    parser.add_argument("--style", default="for-the-badge")
    parser.add_argument("--link")
    parser.add_argument("--output")
    parser.add_argument("--type")
    parser.add_argument("--user")
    parser.add_argument("--repo")
    parser.add_argument("--pkg")
    parser.add_argument("--workflow")
    parser.add_argument("--path")
    parser.add_argument("--uptime-key")
    parser.add_argument("--title")
    parser.add_argument("--file")

    args = parser.parse_args()

    if args.command == "help":
        print("Usage: badge_gen.py COMMAND [OPTIONS]")
        print("\nCommands:")
        print("  setup       Configure environment variables")
        print("  static      Generate static badge")
        print("  dynamic     Generate dynamic badge")
        print("  section     Generate section from JSON")
        print("  help        Show this help")
        print("\nRun './badge-gen.sh --help' for detailed documentation.")
        return

    if args.command == "setup":
        setup_env()
        return

    result = ""
    hide_broken = args.hide_broken

    if args.command == "static":
        result = generate_static(
            args.label,
            args.message,
            args.color,
            args.logo,
            args.style,
            args.link,
            hide_broken,
            args.label_color,
        )
    elif args.command == "dynamic":
        result = generate_dynamic(
            args.type,
            args.user,
            args.repo,
            args.pkg,
            args.workflow,
            args.path,
            args.uptime_key,
            args.style,
            args.link,
            hide_broken,
            args.label_color,
            args.color,
        )
    elif args.command == "section":
        result = f"## {args.title}\n\n"
        with open(args.file, "r") as f:
            for b in json.load(f):
                if b["type"] == "static":
                    res = generate_static(
                        b["label"],
                        b["message"],
                        b.get("color"),
                        b.get("logo"),
                        b.get("style", "for-the-badge"),
                        b.get("link"),
                        hide_broken,
                        b.get("label_color"),
                    )
                else:
                    res = generate_dynamic(
                        b.get("type_param", ""),
                        b.get("user"),
                        b.get("repo"),
                        b.get("pkg"),
                        b.get("workflow"),
                        b.get("path"),
                        b.get("uptime_key"),
                        b.get("style", "for-the-badge"),
                        b.get("link"),
                        hide_broken,
                        b.get("label_color"),
                        b.get("color"),
                    )
                if res:
                    result += res + " "
        result += "\n"

    if result:
        print(result)
        if args.output:
            with open(args.output, "a") as f:
                f.write(result + "\n")
        notify("Badge Generator", f"Finished {args.command}", not args.no_notify)


if __name__ == "__main__":
    main()
