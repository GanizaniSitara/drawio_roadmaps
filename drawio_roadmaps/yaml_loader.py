import yaml

from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType


def load_roadmap_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    roadmap = Roadmap(data['name'])
    roadmap.set_swimlane_column_title(data['swimlane_column_title'])

    for swimlane_data in data['swimlanes']:
        swimlane = Swimlane(swimlane_data['name'])
        if 'type' in swimlane_data:
            swimlane.set_swimlane_type(SwimlaneType[swimlane_data['type']])

        for event_data in swimlane_data.get('events', []):
            event_type = EventType[event_data['type']] if 'type' in event_data else None
            event = Event(event_data['name'], event_data['date'], event_type)
            swimlane.add_event(event)

        roadmap.add_swimlane(swimlane)

    return roadmap

# Usage example
roadmap = load_roadmap_from_yaml('..\\examples\\swimlane.yaml')
print(roadmap.render())