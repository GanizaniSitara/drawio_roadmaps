from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap

roadmap = Roadmap("Test Roadmap")
roadmap.set_swimlane_column_title("CUSTOM SWIMLANES")

swimlane = Swimlane("Swimlane 1")

roadmap.add_swimlane(swimlane)
roadmap.add_swimlane("Swimlane 2")
roadmap.add_swimlane("Swimlane 3")

event1 = Event("Event 1",  "2024-06-01",)
event2 = Event("Event 2",  "2026-06-01", )
event3 = Event("Event 3",  "2025-06-01", )

swimlane.add_event(event1)
swimlane.add_event(event2)
swimlane.add_event(event3)
swimlane.add_event(Event("Event 4",  "2025-12-31"))

# Print the Roadmap to the console
print(str(roadmap))
print(f"{'#' * 80}")

print(roadmap.render())