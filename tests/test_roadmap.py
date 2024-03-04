import unittest
from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap


class TestRoadmap(unittest.TestCase):
    def setUp(self):
        self.roadmap = Roadmap("Test Roadmap")

    def test_add_swimlane_to_roadmap(self):
        swimlane = Swimlane("Test Swimlane")
        self.roadmap.add_swimlane(swimlane)
        self.assertIn(swimlane, self.roadmap.swimlanes)

    def test_roadmap_last_year_runout_default(self):
        self.assertFalse(self.roadmap.last_year_runout)

if __name__ == "__main__":
    unittest.main()