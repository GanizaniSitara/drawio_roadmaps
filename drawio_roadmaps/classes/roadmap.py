from drawio_roadmaps.config import RoadmapConfig as config
from drawio_roadmaps.classes.swimlane import Swimlane

from drawio_roadmaps.renderer_manager import RendererManager
renderer_manager = RendererManager()

class Roadmap:
    def __init__(self, name, start_year=2024, years=4, last_year_runout=False):
        self.name = name


        self.swimlane_column_title = "SWIMLANES"

        self.start_year = start_year
        self.end_year = start_year + years
        self.years = years

        self.swimlanes = []  # Applications under this roadmap
        self.last_year_runout = last_year_runout


    def __str__(self, indent=0):
        result = ' ' * indent + f"Roadmap: {self.name}\n"
        for swimlane in self.swimlanes:
            result += swimlane.__str__(indent + 4)
        return result

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

    def get_renderer(self):
        if self.renderer is None:
            raise ValueError("Renderer not set in roadmap instance. Use set_renderer() method to set the renderer.")
        return self.renderer

    def render(self):
        self.renderer = renderer_manager.get_renderer("roadmap")
        return self.renderer.render(self)




