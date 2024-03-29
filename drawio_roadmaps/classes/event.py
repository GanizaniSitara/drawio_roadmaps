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

    def __str__(self):
        return f"{self.description}"

    def __repr__(self):
        return f"{self.event_type.marker} {self.description} [{self.date.strftime('%Y-%m-%d')} " \
               f"{self.event_type.render_meta.fillColor}]"

    def to_string(self, indent=0):
        return ' ' * indent + repr(self)

    def get_event_marker(self):
        return self.event_type.marker

    def add_link(self, event_link):
        self.links.append(event_link)

    def render(self, segment_width, years):
        renderer = renderer_manager.get_renderer('event')
        return renderer.render_event(self, segment_width, years)

    def tubemap_station(self, root, layer, x, y, style):
        renderer = renderer_manager.get_renderer('event')
        renderer.render_circle(self, root, layer, x, y, style)
        return

    def get_drawio_xml(self):
        renderer = renderer_manager.get_renderer('event')
        return renderer.get_drawio_xml(self)




