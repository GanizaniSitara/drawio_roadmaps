from typing import List, Optional

from drawio_roadmaps.enums.swimlane_type import SwimlaneType
from drawio_roadmaps.renderer_manager import RendererManager

from drawio_roadmaps.config import RoadmapConfig as config
from datetime import datetime, date

renderer_manager = RendererManager()

class Swimlane:
    def __init__(
            self,
            name,
            roadmap=None,
            swimlane_type: SwimlaneType = SwimlaneType.PLATFORM,
            lifelines=None
    ):
        self.name = name
        self.renderer = renderer_manager.get_renderer("swimlane")

        self.events = []  # Events under this swimlane
        self.type = swimlane_type
        self.roadmap = roadmap
        self.roadmap_renderer = None
        if lifelines is None:
            self.lifelines = []

    def __str__(self, indent=0):
        swimlane_str = ' ' * indent + f"Swimlane: {self.name} [{getattr(self.type.metadata_drawio, 'color', '')}]\n"
        for event in self.events:
            swimlane_str += event.to_string(indent + 4)
        swimlane_str += '\n'
        return swimlane_str

    def set_renderer(self, renderer):
        self.renderer = renderer

    # Todo: This is output specifc implementation for Drawio, should be moved to the appropriate renderer
    # and if we still want abstraction, should work equally for all output formats, we might even implement it here?
    def tubemap_line(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        renderer = renderer_manager.get_renderer('swimlane')
        renderer.render_swimline(root=root,
                                 layer=layer,
                                 begin_x=begin_x,
                                 begin_y=begin_y,
                                 end_x=end_x,
                                 end_y=end_y,
                                 width=width,
                                 height=height,
                                 style=style,
                                 value=kwargs.get('value', ''))
        return

    def height(self):
        return config.DrawIO.swimlane_height_px + (len(self.lifelines) * config.DrawIO.swimlane_height_px // 4)

    def render(self):
        result = renderer_manager.get_renderer('swimlane').render(self)
        return result

    def get_swimlane_marker(self):
        return self.type.marker

    def set_swimlane_type(self, swimlane_type):
        self.type = swimlane_type

    def set_roamap(self, roadmap):
        self.roadmap = roadmap

    def add_event(self, event):
        self.events.append(event)
        self.events.sort(key=lambda x: x.date)

    def add_lifeline(self, lifeline):
        self.lifelines.append(lifeline)

    def get_lifeline_y_coordinate_index(self, lifeline_name):
        for index, lifeline in enumerate(self.lifelines):
            if lifeline.name == lifeline_name:
                return index
        return None



