from drawio_roadmaps.enums.swimlane_type import SwimlaneType
from drawio_roadmaps.renderer_manager import RendererManager

renderer_manager = RendererManager()

class Swimlane:
    def __init__(self, name, roadmap=None, swimlane_type: SwimlaneType = SwimlaneType.PLATFORM):
        self.name = name
        self.renderer = renderer_manager.get_renderer("swimlane")

        self.events = []  # Events under this swimlane
        self.type = swimlane_type
        self.roadmap = roadmap

    def __str__(self, indent=0):
        swimlane_str = ' ' * indent + f"Swimlane: {self.name} [{self.type.render_meta.color}]\n"
        for event in self.events:
            swimlane_str += event.__str__(indent + 4)
        swimlane_str += '\n'
        return swimlane_str

    def set_renderer(self, renderer):
        self.renderer = renderer

    def render(self, segment_width, years):
        swimlane_pad = '|' + ' ' * segment_width + '|' + ' ' * (years * (segment_width + 1) - 1) + '|\n'

        swimlane_str = f"| {self.name}"
        swimlane_str += ' ' * (segment_width - len(swimlane_str) + 1) + '|'


        events_visual_line = (' ' + self.get_swimlane_marker() * (((segment_width + 1) * (years)) - 12)
                         + '>>>       ' + '|\n')
        events_str = ''

        for event in self.events:
            # Calculate the offset based on the event's date
            offset = (event.date.year - self.roadmap.start_year) * 12 + event.date.month
            offset_segments = offset * 3  # 3 segments per month

            # Replace '=' with '#' to visually represent an event
            if offset_segments < len(events_visual_line) - 1:  # Ensure within bounds
                events_visual_line = (events_visual_line[:offset_segments] +
                                      event.get_event_marker() + events_visual_line[
                                                                                  offset_segments + 1:])


            # Add spaces for the offset
            event_str = '|' +  ' ' * self.roadmap.segment_width + '|' + ' ' * offset_segments + str(event)
            event_str += ' ' * ((segment_width + 1) * (years + 1) - len(event_str)) + '|\n'
            events_str += event_str

        # events_visual_line = '|' + ' ' * segment_width + '|' + events_visual_line

        result = swimlane_pad + swimlane_str + events_visual_line + events_str + swimlane_pad

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

    def add_timeline(self, timeline):
        self.timelines.append(timeline)



