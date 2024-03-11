import sys
import yaml
import csv
from datetime import datetime
import sqlite3

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



# ToDo: Loaders need sorting out and moving out to the loaders module. No need for them to sit here.
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
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                data = list(reader)

            roadmap_name = data[0]['roadmap_name']
            swimlane_column_title = data[0]['swimlane_column_title']

            roadmap = Roadmap(roadmap_name)
            roadmap.set_swimlane_column_title(swimlane_column_title)

            for row in data:
                swimlane_name = row['swimlane_name']
                swimlane_type = SwimlaneType[row['swimlane_type']] if row['swimlane_type'] else None

                swimlane = roadmap.get_swimlane_by_name(swimlane_name)
                if not swimlane:
                    swimlane = Swimlane(swimlane_name)
                    if swimlane_type:
                        swimlane.set_swimlane_type(swimlane_type)
                    roadmap.add_swimlane(swimlane)

                event_name = row['event_name']
                event_date = datetime.strptime(row['event_date'], '%Y-%m-%d')
                event_type = EventType[row['event_type']] if row['event_type'] else None

                event = Event(event_name, event_date, event_type)
                swimlane.add_event(event)

        except Exception as e:
            raise LoadError(file_path, e)

        return roadmap

class DatabaseRoadmapLoader(RoadmapLoader):
    def load(self, connection_string):
        try:
            conn = sqlite3.connect(connection_string)
            cursor = conn.cursor()

            # Fetch roadmap data
            cursor.execute("SELECT * FROM roadmaps")
            roadmap_data = cursor.fetchone()
            roadmap = Roadmap(roadmap_data[1])
            roadmap.set_swimlane_column_title(roadmap_data[2])

            # Fetch swimlanes
            cursor.execute("SELECT * FROM swimlanes WHERE roadmap_id = ?", (roadmap_data[0],))
            swimlane_data = cursor.fetchall()
            for swimlane_row in swimlane_data:
                swimlane_id = swimlane_row[0]
                swimlane_name = swimlane_row[2]
                swimlane_type = SwimlaneType[swimlane_row[3]] if swimlane_row[3] else None

                swimlane = roadmap.get_swimlane_by_name(swimlane_name)
                if not swimlane:
                    swimlane = Swimlane(swimlane_name)
                    if swimlane_type:
                        swimlane.set_swimlane_type(swimlane_type)
                    roadmap.add_swimlane(swimlane)

                # Fetch events for each swimlane
                cursor.execute("SELECT * FROM events WHERE swimlane_id = ?", (swimlane_id,))
                event_data = cursor.fetchall()
                for event in event_data:
                    event_name = event[2]
                    event_date = datetime.strptime(event[3], '%Y-%m-%d')
                    event_type = EventType[event[4]] if event[4] else None

                    event_obj = Event(event_name, event_date, event_type)
                    swimlane.add_event(event_obj)

            conn.close()
        except Exception as e:
            raise LoadError(connection_string, e)

        return roadmap

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
    elif renderer_type.lower() == "powerpoint":
        renderer_manager.set_renderer_type(RendererType.POWERPOINT)
    elif renderer_type.lower() == "string":
        renderer_manager.set_renderer_type(RendererType.STRING)
    else:
        print(f"Invalid renderer type: {renderer_type}")
        return

    print(roadmap.render())

if __name__ == "__main__":
    main()