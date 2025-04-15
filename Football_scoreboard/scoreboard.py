from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple


@dataclass
class Match:
    home_team: str
    away_team: str
    home_score: int = 0
    away_score: int = 0
    start_time: datetime = None

    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

    @property
    def total_score(self) -> int:
        return self.home_score + self.away_score


class Scoreboard:
    def __init__(self):
        self.matches: List[Match] = []

    def start_match(self, home_team: str, away_team: str) -> Match:
        """Start a new match with initial score 0-0 and add it to the scoreboard."""
        if not home_team or not away_team:
            raise ValueError("Team names cannot be empty")
            
        match = Match(home_team=home_team, away_team=away_team)
        self.matches.append(match)
        return match

    def update_score(self, match_index: int, home_score: int, away_score: int) -> Match:
        """Update the score of a match."""
        if match_index < 0 or match_index >= len(self.matches):
            raise IndexError("Match index out of range")
        if home_score < 0 or away_score < 0:
            raise ValueError("Scores cannot be negative")
            
        match = self.matches[match_index]
        match.home_score = home_score
        match.away_score = away_score
        return match

    def finish_match(self, match_index: int) -> None:
        """Remove a match from the scoreboard."""
        if match_index < 0 or match_index >= len(self.matches):
            raise IndexError("Match index out of range")
        del self.matches[match_index]

    def get_summary(self) -> List[Tuple[str, int, int, str]]:
        """Get matches ordered by total score (descending) and start time (descending for ties)."""
        # Sort by total score (descending) and then by start time (descending - newer matches come first)
        sorted_matches = sorted(
            self.matches,
            key=lambda m: (-m.total_score, -m.start_time.timestamp())
        )
        
        return [
            (match.home_team, match.home_score, match.away_score, match.away_team)
            for match in sorted_matches
        ]