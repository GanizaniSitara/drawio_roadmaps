from drawio_roadmaps.classes.config import RoadmapConfig
from drawio_roadmaps.classes.swimlane import Swimlane

from drawio_roadmaps.renderer_manager import RendererManager
renderer_manager = RendererManager()

class Roadmap:
    def __init__(self, name, start_year=2024, years=4, last_year_runout=False):
        self.name = name

        self.segment_width = RoadmapConfig.Text.segment_width

        self.swimlane_column_title = "SWIMLANES"

        self.start_year = start_year
        self.end_year = start_year + years
        self.years = years

        self.swimlanes = []  # Applications under this roadmap
        self.last_year_runout = last_year_runout


    def __str__(self, indent=0):
        roadmap_str = ' ' * indent + f"Roadmap: {self.name}, {self.start_year}, {self.end_year}\n"
        for swimlane in self.swimlanes:
            roadmap_str += swimlane.__str__(indent + 4)
        return roadmap_str

    def set_swimlane_column_title(self, title):
        self.swimlane_column_title = title

    def add_swimlane(self, swimlane_or_name):
        if isinstance(swimlane_or_name, Swimlane):
            # If a Swimlane instance is provided, set its roadmap attribute
            swimlane = swimlane_or_name
        else:
            # If a name is provided, create a new Swimlane instance
            swimlane = Swimlane(swimlane_or_name, self)
        swimlane.set_roamap(self)
        self.swimlanes.append(swimlane)
        return swimlane

    def get_swimlane_by_name(self, name):
        for swimlane in self.swimlanes:
            if swimlane.name == name:
                return swimlane
        return None  # Return None if no swimlane with the given name is found

    def set_renderer(self, renderer):
        self.renderer = renderer

    def render(self):
        self.renderer = renderer_manager.get_renderer("roadmap")
        return self.renderer.render(self)




