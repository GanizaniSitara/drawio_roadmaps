import random
import unittest
from datetime import datetime, timedelta

from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap


class TestDataDefinition(unittest.TestCase):
    def setUp(self):
        self.roadmap = Roadmap("Test Roadmap", last_year_runout=True)

    def test_roadmap_with_swimlane_and_events(self):
        swimlane = Swimlane("Test Swimlane")
        self.roadmap.add_swimlane(swimlane)

        for i in range(1,11):
            event_date = self.random_date(self.roadmap.start_year, self.roadmap.end_year)
            event = Event(f"Test Event {i}", date_input=f"2024-{i:02}-01")
            swimlane.events.append(event)

        self.assertEqual(len(self.roadmap.swimlanes), 1)
        self.assertEqual(len(self.roadmap.swimlanes[0].events), 10)

    @staticmethod
    def random_date(start_year, end_year):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        return start_date + (end_date - start_date) * random.random()

if __name__ == "__main__":
    unittest.main()