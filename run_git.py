import subprocess
import sys
from main import parse_commits

repo = sys.argv[1]
file_path = sys.argv[2]
start = sys.argv[3]
end = sys.argv[4]

result = subprocess.run(
    ["git", "log", "-L", f"{start},{end}:{file_path}",
     "--date=short", "--format=%h|%an|%ad|%s|%b@@END@@", "-s"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    cwd=repo,
)

if result.returncode != 0:
    print("git failed:", result.stderr)
    sys.exit(1)

print("final_result" ,repr(result.stdout))

commits = parse_commits(result.stdout)

linked = 0
for c in commits:
    print(c["date"], c["hash"], c["author"], "PR:", c["pr"], "|", c["message"], "| body chars:", len(c["body"]))
    if c["pr"] is not None:
        linked += 1

print(f"{linked} of {len(commits)} commits have a PR number")