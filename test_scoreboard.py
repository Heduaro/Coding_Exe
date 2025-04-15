import unittest
from datetime import datetime, timedelta
from scoreboard import Scoreboard, Match


class TestScoreboard(unittest.TestCase):
    def setUp(self):
        self.scoreboard = Scoreboard()
        # Add some test matches with controlled start times
        self.match1 = self.scoreboard.start_match("Mexico", "Canada")
        self.match2 = self.scoreboard.start_match("Spain", "Brazil")
        self.match3 = self.scoreboard.start_match("Germany", "France")
        
        # Manually set start times for consistent testing
        self.match1.start_time = datetime.now() - timedelta(minutes=30)
        self.match2.start_time = datetime.now() - timedelta(minutes=20)
        self.match3.start_time = datetime.now() - timedelta(minutes=10)

    def test_start_match(self):
        initial_count = len(self.scoreboard.matches)
        new_match = self.scoreboard.start_match("Uruguay", "Italy")
        self.assertEqual(len(self.scoreboard.matches), initial_count + 1)
        self.assertEqual(new_match.home_team, "Uruguay")
        self.assertEqual(new_match.away_team, "Italy")
        self.assertEqual(new_match.home_score, 0)
        self.assertEqual(new_match.away_score, 0)

    def test_update_score(self):
        self.scoreboard.update_score(0, 0, 5)  # Mexico vs Canada
        self.assertEqual(self.match1.home_score, 0)
        self.assertEqual(self.match1.away_score, 5)
        
        self.scoreboard.update_score(1, 10, 2)  # Spain vs Brazil
        self.assertEqual(self.match2.home_score, 10)
        self.assertEqual(self.match2.away_score, 2)

    def test_finish_match(self):
        initial_count = len(self.scoreboard.matches)
        self.scoreboard.finish_match(0)
        self.assertEqual(len(self.scoreboard.matches), initial_count - 1)
        self.assertNotIn(self.match1, self.scoreboard.matches)

    def test_get_summary(self):
        # Set up scores
        self.scoreboard.update_score(0, 0, 5)   # Mexico 0-5 Canada (total 5)
        self.scoreboard.update_score(1, 10, 2)  # Spain 10-2 Brazil (total 12)
        self.scoreboard.update_score(2, 2, 2)   # Germany 2-2 France (total 4)
        
        match4 = self.scoreboard.start_match("Uruguay", "Italy")
        match4.start_time = datetime.now() - timedelta(minutes=5)
        self.scoreboard.update_score(3, 6, 6)   # Uruguay 6-6 Italy (total 12)
        
        match5 = self.scoreboard.start_match("Argentina", "Australia")
        match5.start_time = datetime.now()
        self.scoreboard.update_score(4, 3, 1)  # Argentina 3-1 Australia (total 4)
        
        # Get summary
        summary = self.scoreboard.get_summary()
        
        expected_order = [
            ("Uruguay", 6, 6, "Italy"),      # Total 12, newer than Spain
            ("Spain", 10, 2, "Brazil"),      # Total 12, older than Uruguay
            ("Mexico", 0, 5, "Canada"),      # Total 5
            ("Argentina", 3, 1, "Australia"), # Total 4, newer than Germany
            ("Germany", 2, 2, "France"),     # Total 4, older than Argentina
        ]
        
        self.assertEqual(summary, expected_order)

    def test_invalid_operations(self):
        with self.assertRaises(IndexError):
            self.scoreboard.update_score(99, 1, 1)
            
        with self.assertRaises(IndexError):
            self.scoreboard.finish_match(99)
            
        with self.assertRaises(ValueError):
            self.scoreboard.start_match("", "Canada")
            
        with self.assertRaises(ValueError):
            self.scoreboard.update_score(0, -1, 0)


if __name__ == "__main__":
    unittest.main()