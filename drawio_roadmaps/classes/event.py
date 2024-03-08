from datetime import datetime, date
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.renderer_manager import RendererManager

renderer_manager = RendererManager()



class Event:
    def __init__(self, description, date_input, event_type: EventType = None):
        self.name = description
        self.renderer = renderer_manager.get_renderer("event")

        self.description = description
        self.event_type = event_type if event_type is not None else EventType.UNFUNDED
        if isinstance(date_input, date):
            self.date = date_input
        elif isinstance(date_input, str):
            self.date = datetime.strptime(date_input, '%Y-%m-%d').date()
        else:
            raise ValueError("The date must be a string in 'YYYY-MM-DD' format or a datetime.date instance.")
        self.links = []

    def __repr__(self):
        market = self.event_type.marker if self.event_type else '='
        return f"{market} {self.description} - {self.date.strftime('%Y-%m-%d')}"

    def __str__(self, indent=0):
        return ' ' * indent + f"{self.event_type.marker} {self.description}"

    def get_event_marker(self):
        return self.event_type.marker

    def add_link(self, event_link):
        self.links.append(event_link)

    def render(self, segment_width, years):
        renderer = renderer_manager.get_renderer('event')
        return renderer.render_event(self, segment_width, years)


