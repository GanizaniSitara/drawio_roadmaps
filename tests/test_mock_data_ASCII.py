from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType

roadmap = Roadmap("Technology Strategy")
roadmap.set_swimlane_column_title("CAPABILITY FOCUS")

roadmap.add_swimlane("Build Once Architecture")
roadmap.add_swimlane("Authentication")
roadmap.add_swimlane("Profiles")
roadmap.add_swimlane("Authorisation")
roadmap.add_swimlane("Search")

swimlane = Swimlane("Containment")
roadmap.add_swimlane(swimlane)

swimlane = roadmap.get_swimlane_by_name("Build Once Architecture")
swimlane.add_event(Event("React Native",  "2024-03-31", EventType.UNFUNDED))
swimlane.add_event(Event("DAF Session Cache",  "2024-09-30", EventType.TARGET))
swimlane.add_event(Event("DAF Web",  "2024-12-31", EventType.DECISION))
swimlane.add_event(Event("Modern Identity",  "2025-09-30"))
swimlane.add_event(Event("Rich Error Handling",  "2026-06-30"))
swimlane.add_event(Event("Channel Compatibility",  "2026-10-31", EventType.RETIREMENT))

swimlane = roadmap.get_swimlane_by_name("Authentication")
swimlane.set_swimlane_type(SwimlaneType.INDEPENDENT)
swimlane.add_event(Event("IAM Platform Selection",  "2024-06-30"))
swimlane.add_event(Event("Device Authentication",  "2024-12-31"))
swimlane.add_event(Event("Web Authentication",  "2025-03-30"))

print(roadmap.render())

