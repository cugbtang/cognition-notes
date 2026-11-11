"""用 GitHub REST API 把本地工作区同步到远程 main。

适用场景：网络代理只放行 api.github.com，github.com 的 git 端点
返回 "CONNECT tunnel failed, 502"，导致 git push / fetch 不可用。

用法：
    GH_TOKEN=$(gh auth token) python tools/sync_via_api.py "commit message"

前提：
    - 已安装并登录 gh（脚本从 GH_TOKEN 读凭据，不会打印）
    - 本地 HEAD 与远程 main 一致；脚本会检查，不一致就中止
    - 仓库非首次创建（空仓库需先用 Contents API PUT 一个文件激活）

行为：
    1. git add -A 后用 write-tree 拿到本地 tree
    2. 通过 Git Data API 创建 blobs / tree / commit（parent = 远程 HEAD）
    3. 强制更新远程 refs/heads/main
    4. 在本地复现同一个 commit 对象，把 main 与 origin/main 对齐到该 sha
       这样工作区保持干净，后续仍能正常增量提交
"""

import base64
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = os.environ.get("GITHUB_REPO", "cugbtang/cognition-notes")
TOKEN = os.environ.get("GH_TOKEN")
MSG = sys.argv[1] if len(sys.argv) > 1 else "update notes"

if not TOKEN:
    sys.exit('缺少 GH_TOKEN。用法：GH_TOKEN=$(gh auth token) python tools/sync_via_api.py "msg"')
if "\n" in MSG:
    sys.exit("commit message 不支持换行")

HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "cognition-notes-sync",
    "Content-Type": "application/json",
}


def api(method, path, payload=None):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request("https://api.github.com" + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        print("HTTP %s %s" % (exc.code, path))
        print(exc.read().decode("utf-8")[:800])
        raise


def git(*args, stdin=None):
    proc = subprocess.run(["git", "-C", ROOT, *args], input=stdin, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError("git %s 失败：%s" % (" ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8").strip()


git("add", "-A")
tree_local = git("write-tree")
files = [f for f in git("ls-files").splitlines() if f]
head_local = git("rev-parse", "HEAD")

remote_ref = api("GET", "/repos/%s/git/ref/heads/main" % SLUG)
head_remote = remote_ref["object"]["sha"]
if head_local != head_remote:
    sys.exit("本地 HEAD %s 与远程 main %s 不一致，请先人工对齐" % (head_local[:8], head_remote[:8]))

remote_commit = api("GET", "/repos/%s/git/commits/%s" % (SLUG, head_remote))
if remote_commit["tree"]["sha"] == tree_local:
    print("工作区无改动，跳过提交。")
    sys.exit(0)

entries = []
for rel in files:
    with open(os.path.join(ROOT, rel), "rb") as fh:
        encoded = base64.b64encode(fh.read()).decode("ascii")
    blob = api("POST", "/repos/%s/git/blobs" % SLUG, {"content": encoded, "encoding": "base64"})
    entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print("blob  ", rel)

tree = api("POST", "/repos/%s/git/trees" % SLUG, {"tree": entries})
if tree["sha"] != tree_local:
    sys.exit("tree 不一致（本地 %s / 远程 %s），远程未被修改" % (tree_local, tree["sha"]))
print("tree  ", tree["sha"])

name = git("config", "user.name")
email = git("config", "user.email")
ts = int(time.time())
offset = datetime.now().astimezone().utcoffset() or timedelta(0)
seconds = int(offset.total_seconds())
tz = "%+03d%02d" % (seconds // 3600, (seconds % 3600) // 60)
date_iso = datetime.fromtimestamp(ts, timezone(offset)).isoformat()
who = {"name": name, "email": email, "date": date_iso}

commit = api("POST", "/repos/%s/git/commits" % SLUG, {
    "message": MSG,
    "tree": tree["sha"],
    "parents": [head_remote],
    "author": who,
    "committer": who,
})
new_sha = commit["sha"]

# Git Data API 生成的 commit message 不带末尾换行；按同样字节构造才能复现 sha
raw = (
    "tree %s\nparent %s\nauthor %s <%s> %d %s\ncommitter %s <%s> %d %s\n\n%s"
    % (tree["sha"], head_remote, name, email, ts, tz, name, email, ts, tz, MSG)
).encode("utf-8")
rebuilt = hashlib.sha1(b"commit %d\0" % len(raw) + raw).hexdigest()
if rebuilt != new_sha:
    print("无法精确复现 commit 对象，远程 main 尚未更新。")
    print("  远程 sha :", new_sha)
    print("  重建 sha :", rebuilt)
    print("  远程字段 :", json.dumps(commit.get("author"), ensure_ascii=False),
          json.dumps(commit.get("committer"), ensure_ascii=False), repr(commit.get("message")))
    sys.exit(1)

api("PATCH", "/repos/%s/git/refs/heads/main" % SLUG, {"sha": new_sha, "force": True})
git("hash-object", "-w", "-t", "commit", "--stdin", stdin=raw)
for ref in ("refs/heads/main", "refs/remotes/origin/main"):
    git("update-ref", ref, new_sha)

print("提交完成：%s  %s" % (new_sha[:8], MSG))
print("本地 main 与 origin/main 已对齐")
