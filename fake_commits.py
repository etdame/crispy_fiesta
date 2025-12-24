#!/usr/bin/env python3
"""
Fake Commit Generator
Generates backdated commits with realistic probability distribution.
"""

import subprocess
import random
from datetime import datetime, timedelta

# ============== CONFIGURATION ==============
# Number of days to go back
DAYS_BACK = 20

# Probability distribution for number of commits per day
# Format: {num_commits: probability_percentage}
# Probabilities should sum to 100
COMMIT_PROBABILITIES = {
    0: 25,   # 25% chance of no commits (rest day)
    1: 20,   # 20% chance of 1 commit
    2: 18,   # 18% chance of 2 commits
    3: 15,   # 15% chance of 3 commits
    4: 10,   # 10% chance of 4 commits
    5: 6,    # 6% chance of 5 commits
    6: 3,    # 3% chance of 6 commits
    7: 2,    # 2% chance of 7 commits
    8: 0.7,  # 0.7% chance of 8 commits
    9: 0.3,  # 0.3% chance of 9 commits
}

# Commit messages pool
COMMIT_MESSAGES = [
    "Update README",
    "Fix typo",
    "Refactor code",
    "Add feature",
    "Bug fix",
    "Update docs",
    "Clean up",
    "Minor changes",
    "Improve performance",
    "Add tests",
]
# ===========================================


def get_random_commit_count():
    """Select number of commits based on probability distribution."""
    rand = random.uniform(0, 100)
    cumulative = 0
    for count, prob in COMMIT_PROBABILITIES.items():
        cumulative += prob
        if rand <= cumulative:
            return count
    return 0


def create_commit(date: datetime, message: str):
    """Create a backdated commit."""
    # Format date for git
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Modify a file to have something to commit
    with open("history.txt", "a") as f:
        f.write(f"// {message}\n")
    
    # Stage and commit with backdated timestamp
    subprocess.run(["git", "add", "."], check=True)
    
    env_date = date.strftime("%a %b %d %H:%M:%S %Y %z")
    result = subprocess.run(
        ["git", "commit", "-m", message, "--date", date_str],
        env={
            **dict(__import__('os').environ),
            "GIT_AUTHOR_DATE": date_str,
            "GIT_COMMITTER_DATE": date_str,
        },
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"  ✓ {message}")
    else:
        print(f"  ✗ Failed: {result.stderr.strip()}")


def main():
    print(f"Generating commits for the past {DAYS_BACK} days\n")
    print("Probability distribution:")
    for count, prob in COMMIT_PROBABILITIES.items():
        print(f"  {count} commits: {prob}%")
    print()
    
    total_commits = 0
    
    for days_ago in range(DAYS_BACK, 0, -1):
        date = datetime.now() - timedelta(days=days_ago)
        commit_count = get_random_commit_count()
        
        print(f"{date.strftime('%Y-%m-%d')} - {commit_count} commits")
        
        for i in range(commit_count):
            # Randomize time throughout the day
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = date.replace(hour=hour, minute=minute, second=second)
            
            message = random.choice(COMMIT_MESSAGES)
            create_commit(commit_time, message)
            total_commits += 1
    
    print(f"\nDone! Created {total_commits} commits over {DAYS_BACK} days")


if __name__ == "__main__":
    main()

