# Coding_Exe

# Live Football World Cup Scoreboard

A simple library to manage and display live football match scores.

## Features

- Start new matches with initial score 0-0
- Update match scores
- Finish/remove matches from the scoreboard
- Get a summary of matches ordered by total score (and start time for ties)

## Usage

```python
from scoreboard import Scoreboard

# Create a scoreboard
scoreboard = Scoreboard()

# Start matches
scoreboard.start_match("Mexico", "Canada")
scoreboard.start_match("Spain", "Brazil")

# Update scores
scoreboard.update_score(0, 0, 5)  # Mexico 0 - Canada 5
scoreboard.update_score(1, 10, 2) # Spain 10 - Brazil 2

# Finish a match
scoreboard.finish_match(0)  # Remove Mexico vs Canada

# Get summary
summary = scoreboard.get_summary()
for match in summary:
    print(f"{match[0]} {match[1]} - {match[2]} {match[3]}")
