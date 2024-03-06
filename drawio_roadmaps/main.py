import sys
import yaml

from drawio_roadmaps.classes.event import Event
from drawio_roadmaps.classes.swimlane import Swimlane
from drawio_roadmaps.classes.roadmap import Roadmap
from drawio_roadmaps.renderers.roadmap_renderer import AsciiRoadmapRenderer
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType
from drawio_roadmaps.renderer_manager import RendererManager, RendererType


class RoadmapLoader:
    def load(self):
        raise NotImplementedError("Subclasses must implement this method")


class LoadError(Exception):
    def __init__(self, filename, original_exception):
        self.filename = filename
        self.original_exception = original_exception
        super().__init__(f"Error loading file {filename}: {original_exception}")



class YamlRoadmapLoader(RoadmapLoader):
    def load(self, file_path):
        try:
            with open(file_path, 'r') as file:
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
        except Exception as e:
            raise LoadError(file_path, e)

        return roadmap


class CsvRoadmapLoader(RoadmapLoader):
    def load(self, file_path):
        # Implement CSV loading logic
        pass

class DatabaseRoadmapLoader(RoadmapLoader):
    def load(self, connection_string):
        # Implement Database loading logic
        pass


class RoadmapLoaderFactory:
    @staticmethod
    def get_loader(source_type):
        if source_type == 'yaml':
            return YamlRoadmapLoader()
        elif source_type == 'csv':
            return CsvRoadmapLoader()
        elif source_type == 'database':
            return DatabaseRoadmapLoader()
        else:
            raise ValueError(f"Unknown source type: {source_type}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <source_type> <renderer_type> <source_path>")
        return

    source_type = sys.argv[1]
    renderer_type = sys.argv[2]
    source_path = sys.argv[3]

    loader = RoadmapLoaderFactory.get_loader(source_type)
    roadmap = loader.load(source_path)

    renderer_manager = RendererManager()

    if renderer_type.lower() == "ascii":
        renderer_manager.set_renderer_type(RendererType.ASCII)
    elif renderer_type.lower() == "drawio":
        renderer_manager.set_renderer_type(RendererType.DRAWIO)
    else:
        print(f"Invalid renderer type: {renderer_type}")
        return

    print(roadmap.render())

if __name__ == "__main__":
    main()