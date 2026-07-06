import argparse
import urllib.parse
import json
import sys
import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

# Official brand colors for popular technologies
LANG_COLORS = {
    "python": "3776AB", "javascript": "F7DF1E", "typescript": "3178C6",
    "rust": "DEA584", "java": "007396", "go": "00ADD8", "php": "777BB4",
    "ruby": "CC342D", "swift": "F05138", "kotlin": "7F52FF", "dart": "0175C2"
}

def send_webhook(title, message):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url: return
    data = {"content": f"**{title}**: {message}"}
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except Exception:
        pass

def notify(title, message, enabled=True):
    if not enabled: return
    send_webhook(title, message)
    try:
        if sys.platform == "win32":
            from win10toast import ToastNotifier
            ToastNotifier().show_toast(title, message, duration=5)
        elif sys.platform == "darwin":
            os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")
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

def generate_static(label, message, color=None, logo=None, style="for-the-badge", link=None, hide_broken=False, l_color=None):
    final_color = color if color else LANG_COLORS.get(label.lower(), "grey")
    label_esc = urllib.parse.quote(label.replace("-", "--"))
    msg_esc = urllib.parse.quote(message.replace("-", "--"))
    url = f"https://shields.io{label_esc}-{msg_esc}-{final_color}?style={style}"
    if logo: url += f"&logo={logo}&logoColor=white"
    if l_color: url += f"&labelColor={l_color}"
    return build_markdown(url, link, hide_broken)

def generate_dynamic(b_type, user=None, repo=None, pkg=None, workflow=None, path=None, uptime_key=None, style="for-the-badge", link=None, hide_broken=False, l_color=None, color=None):
    params = {"style": style}
    if l_color: params["labelColor"] = l_color
    if color: params["color"] = color
    
    mapping = {
        "actions": f"github/actions/workflow/status/{user}/{repo}/{urllib.parse.quote(workflow or '')}",
        "build-time": f"github/actions/workflow/run-duration/{user}/{repo}/{urllib.parse.quote(workflow or '')}",
        "repo-size": f"github/repo-size/{user}/{repo}",
        "file-size": f"github/size/{user}/{repo}/{path or ''}",
        "vulnerability": f"snyk/vulnerabilities/github/{user}/{repo}",
        "license": f"github/license/{user}/{repo}",
        "views": f"github/search/hits/{user}/{repo}",
        "clones": f"github/downloads/{user}/{repo}/total",
        "top-lang": f"github/languages/top/{user}/{repo}",
        "lang-count": f"github/languages/count/{user}/{repo}",
        "response-time": f"uptimerobot/response/{uptime_key or ''}",
        "codecov": f"codecov/c/github/{user}/{repo}"
    }
    
    if b_type not in mapping: return ""
    url = f"https://shields.io{mapping[b_type]}?{urllib.parse.urlencode(params)}"
    return build_markdown(url, link, hide_broken)

def setup_env():
    path = ".env"
    if not os.path.exists(path): open(path, "w").close()
    set_key(path, "GITHUB_TOKEN", input("GitHub Token: "))
    set_key(path, "SNYK_TOKEN", input("Snyk Token: "))
    set_key(path, "WEBHOOK_URL", input("Webhook URL: "))
    print("Environment setup completed.")

def main():
    parser = argparse.ArgumentParser(description="Professional Badge Generation Tool")
    parser.add_argument("--no-notify", action="store_true")
    parser.add_argument("--hide-broken", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("setup")
    
    st_p = subparsers.add_parser("static")
    st_p.add_argument("--label", required=True); st_p.add_argument("--message", required=True)
    st_p.add_argument("--color"); st_p.add_argument("--label-color"); st_p.add_argument("--logo")
    st_p.add_argument("--style", default="for-the-badge"); st_p.add_argument("--link"); st_p.add_argument("--output")

    dyn_p = subparsers.add_parser("dynamic")
    dyn_p.add_argument("--type", required=True); dyn_p.add_argument("--user"); dyn_p.add_argument("--repo")
    dyn_p.add_argument("--pkg"); dyn_p.add_argument("--workflow"); dyn_p.add_argument("--path"); dyn_p.add_argument("--uptime-key")
    dyn_p.add_argument("--color"); dyn_p.add_argument("--label-color"); dyn_p.add_argument("--style", default="for-the-badge")
    dyn_p.add_argument("--link"); dyn_p.add_argument("--output")

    sec_p = subparsers.add_parser("section")
    sec_p.add_argument("--title", required=True); sec_p.add_argument("--file", required=True); sec_p.add_argument("--output")

    args = parser.parse_args()
    if args.command == "setup": setup_env(); return

    result = ""
    if args.command == "static":
        result = generate_static(args.label, args.message, args.color, args.logo, args.style, args.link, args.hide_broken, args.label_color)
    elif args.command == "dynamic":
        result = generate_dynamic(args.type, args.user, args.repo, args.pkg, args.workflow, args.path, args.uptime_key, args.style, args.link, args.hide_broken, args.label_color, args.color)
    elif args.command == "section":
        result = f"## {args.title}\n\n"
        with open(args.file, 'r') as f:
            for b in json.load(f):
                if b['type'] == 'static':
                    res = generate_static(b['label'], b['message'], b.get('color'), b.get('logo'), b.get('style', 'for-the-badge'), b.get('link'), args.hide_broken, b.get('label_color'))
                else:
                    res = generate_dynamic(b['type'], b.get('user'), b.get('repo'), b.get('pkg'), b.get('workflow'), b.get('path'), b.get('uptime_key'), b.get('style', 'for-the-badge'), b.get('link'), args.hide_broken, b.get('label_color'), b.get('color'))
                if res: result += res + " "
        result += "\n"

    if result:
        print(result)
        if hasattr(args, 'output') and args.output:
            with open(args.output, "a") as f: f.write(result + "\n")
        notify("Badge Generator", f"Finished {args.command}", not args.no_notify)

if __name__ == "__main__": main()
