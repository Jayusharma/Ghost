from per_link import extract_pr
from main import  parse_commits

def test_extract_pr_from_subject():
    result = extract_pr("Add inline types to Requests (#7272)")
    assert result == 7272

def test_extract_pr_none():
    result = extract_pr("Rework authorization stripping logic as discussed")
    assert result is None

def test_parse_commits_finds_pr_in_body():
    text = "3331e2ae|Bruce|2018-06-28|Strip header|leaks creds (#4716)@@END@@"
    commits = parse_commits(text)
    assert len(commits) == 1
    assert commits[0]["pr"] == 4716