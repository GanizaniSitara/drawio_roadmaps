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
    def tubemap_line(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style):
        renderer = renderer_manager.get_renderer('swimlane')
        renderer.render_line(root=root,
                             layer=layer,
                             begin_x=begin_x,
                             begin_y=begin_y,
                             end_x=end_x,
                             end_y=end_y,
                             width=width,
                             height=height,
                             style=style)
        return

    def render(self):
        # ToDo: The whole thing needs moving out to SwimlaneRenderer, for now only Acsii output uses this
        # NOTE - This is totally pointless at the moment as implementation is here
        # self.roadmap_renderer = self.roadmap.get_renderer()


        # ToDo: should be handled in config, we should also remember why this is ... :S
        if config.Global.show_quarters:
            segment_width = config.Ascii.segment_width - 1
        else:
            segment_width = config.Ascii.segment_width
        years = self.roadmap.years



        swimlane_pad = '|' + ' ' * segment_width + '|' + ' ' * (years * (segment_width + 1) - 1) + '|\n'

        swimlane_str = f"| {self.name}"
        swimlane_str += ' ' * (segment_width - len(swimlane_str) + 1) + '|'


        events_visual_line = (' ' + self.get_swimlane_marker() * (((segment_width + 1) * (years)) - 12)
                         + '>>>       ' + '|\n')
        events_str = ''

        for event in self.events:
            # ToDo: should go into event renderer
            # Calculate the offset based on the event's date
            offset = (event.date.year - self.roadmap.start_year) * 12 + event.date.month
            offset_segments = offset * 3  # 3 segments per month

            # Replace '=' with '#' to visually represent an event
            if offset_segments < len(events_visual_line) - 1:  # Ensure within bounds
                events_visual_line = (events_visual_line[:offset_segments] +
                                      event.get_event_marker() + events_visual_line[
                                                                                  offset_segments + 1:])


            # Add spaces for the offset
            event_str = '|' +  ' ' * segment_width + '|' + ' ' * offset_segments + str(event)
            event_str += ' ' * ((segment_width + 1) * (years + 1) - len(event_str)) + '|\n'
            events_str += event_str

        # events_visual_line = '|' + ' ' * segment_width + '|' + events_visual_line

        result = swimlane_pad + swimlane_str + events_visual_line + events_str + swimlane_pad

        # for lifeline in self.lifelines:
        #     # Todo: should go into lifeline renderer
        #     lifeline_str = f"| {lifeline.name}"
        #     lifeline_str += ' ' * (segment_width - len(lifeline_str) + 1) + '|'
        #
        #     lifeline_str += (' ' + '.' * (((segment_width + 1) * (years)) - 12)
        #                           + '>>>       ' + '|\n')
        #
        #     result += lifeline_str + swimlane_pad
        #
        # return result

        # GPT-4
        for lifeline in self.lifelines:
            # Check if from_date is provided; otherwise, start at the beginning of the roadmap
            character_per_days = 365 // segment_width

            if lifeline.from_date is not None:
                start_offset = lifeline.from_date - datetime.strptime(str(self.roadmap.start_year), "%Y").date()
                start_offset = start_offset.days // character_per_days
            else:
                start_offset = 1

            # Check if to_date is provided; otherwise, end at the last year of the roadmap
            if lifeline.to_date is not None:
                end_offset = lifeline.to_date - datetime.strptime(str(self.roadmap.start_year), "%Y").date()
                end_offset = end_offset.days // character_per_days
                ending = '†'
            else:
                end_offset = (years * segment_width) - 7
                ending = '>>>'


            # Construct the lifeline string with appropriate padding and periods
            lifeline_str = (f"| {lifeline.name}")
            lifeline_str += ' ' * (segment_width - len(lifeline_str) + 1) + '|'


            leading_space = ' ' * start_offset
            lifeline_str += leading_space
            lifeline_space = '.' * (end_offset - start_offset) + ending
            trailing_space = ' ' * ((years * (segment_width + 1) - len(leading_space + lifeline_space)) - 1)
            lifeline_str += lifeline_space + trailing_space + '|\n'

            # Append the constructed lifeline string to the result with a newline
            result += lifeline_str


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



