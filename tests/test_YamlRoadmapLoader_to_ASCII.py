import unittest
from drawio_roadmaps.loaders.loaders import YamlRoadmapLoader
from drawio_roadmaps.classes.roadmap import Roadmap
from drawio_roadmaps.enums.event_type import EventType

class TestRoadmapLoader(unittest.TestCase):
    def setUp(self):
        self.loader = YamlRoadmapLoader()
        self.roadmap = self.loader.load('test_data/swimlane.yaml')

    def test_load_roadmap(self):
        self.assertIsInstance(self.roadmap, Roadmap)

    def test_single_swimlane(self):
        self.assertEqual(len(self.roadmap.swimlanes), 1)

    def test_swimlane_milestones(self):
        swimlane = self.roadmap.get_swimlane_by_name('Swimlane 1')
        self.assertEqual(len(swimlane.events), 5)

        # Verify each milestone type
        for event in swimlane.events:
            self.assertIn(event.event_type, [EventType.UNFUNDED, EventType.TARGET, EventType.DECISION,
                                             EventType.COMPLETED, EventType.RETIREMENT])

    def test_output(self):
        output = self.roadmap.render()
        expected_output = """######################################
Roadmap: Strategic Roadmap
######################################
O Unfunded Milestone, @ Target Milestone, X Completed Milestone, † Point of Retirement, # Strategy Decision Point
= Platform, — Independent
+------------------------------------+------------------------------------+------------------------------------+------------------------------------+------------------------------------+
|                                    |                                    |                                    |                                    |                                    |
| SWIMLANES                          |                2024                |                2025                |                2026                |                2027                |
|                                    |                                    |                                    |                                    |                                    |
+------------------------------------+------------------------------------+------------------------------------+------------------------------------+------------------------------------+
|                                    |                                                                                                                                                   |
| Swimlane 1                         | =================O=================@=================X=================†=================#==============================================>>>       |
|                                    |                  O Unfunded Milestone                                                                                                             |
|                                    |                                    @ Target Milestone                                                                                             |
|                                    |                                                      X Completed Milestone                                                                        |
|                                    |                                                                        † Retirement Milestone                                                     |
|                                    |                                                                                          # Decision Milestone                                     |
|                                    |                                                                                                                                                   |
+------------------------------------+------------------------------------+------------------------------------+------------------------------------+------------------------------------+
"""
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
