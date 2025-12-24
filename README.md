# Fake Commit Generator

Generate realistic-looking commit history with configurable probability distribution.

## Usage

```bash
python3 fake_commits.py
```

## Configuration

Edit the constants at the top of `fake_commits.py`:

```python
# Number of days to go back
DAYS_BACK = 20

# Probability distribution (must sum to 100)
COMMIT_PROBABILITIES = {
    0: 25,   # 25% chance of no commits
    1: 20,   # 20% chance of 1 commit
    2: 18,   # etc...
    ...
}
```
