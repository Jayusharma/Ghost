from per_link import extract_pr

commits = [
    {"author":"jay <jay@admin.com>" , "hash":"ae3243gdsa" , "date":"12 oct 2026" ,"message":"this is the push for the request update to http for moer security" },
    {"author":"varun <varun@admin.com>" , "hash":"ae64hwrdd" , "date":"10 oct 2026" , "message": "this is more related to the permission level of the system"},
    {"author":"done <done@admin.com>" , "hash":"rt136qa" , "date":"7 oct 2026" , "message":"this is upgrade to the security to the cybersecuirty system for more antivirus act "}
]

def find_commits(commits , word):
    result=[]
    for commit in commits:
        if word.lower() in commit["message"].lower():
            result.append(commit)
    return result

# for com in find_commits(commits , "SECURITY"):
#     print(f"{com['hash']} includes {com['message']} written by {com['author']}")


def parse_commits(text):
    commits = []
    for record in text.split("@@END@@"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("|", 4)
        commit_hash, author, date, message, body = parts
        body = body.strip()
        commits.append({
            "hash": commit_hash,
            "author": author,
            "date": date,
            "message": message,
            "body": body,
            "pr": extract_pr(message + "\n" + body),
        })
    return commits



# with open("commits.txt") as f:
#     text = f.read()

# com = parse_commits(text)
# # print(com) 


# for c in find_commits(com , "retry"):
#     print(c["hash"] , c["message"])