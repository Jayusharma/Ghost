# Sorting with key: lamba a small function in key

def leaderboard(players):
    return sorted(players, key=lambda s: (-s["score"], s["name"], s["age"]))

players = [
    {"name": "Ann", "score": 90, "age": 22},
    {"name": "Bob", "score": 85, "age": 21},
    {"name": "Cat", "score": 90, "age": 21},
    {"name": "Dan", "score": 85, "age": 21},
    {"name": "Eve", "score": 100, "age": 25},
]

print(leaderboard(players))