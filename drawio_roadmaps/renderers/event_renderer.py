
from drawio_roadmaps.drawio.drawio_shapes import Circle
from drawio_roadmaps.drawio.drawio_utils import id_generator_2, layer_id_2


class EventRenderer:
    def render_event(self, event, segment_width, years):
        raise NotImplementedError

class AsciiEventRenderer(EventRenderer):

    def render_event(self, event, segment_width, years):
        event_str = f"Event: {event.description}\n"
        horizontal_segment = '+' + '-' * segment_width
        event_top = horizontal_segment * years + '+\n'
        event_str += event_top
        return event_str

class StringEventRenderer(EventRenderer):
    def render_event(self, event):
        event_str = f"Event: {event.description} {event.event_type} {event.metadata_drawio.fillColor}\n"
        return event_str

class DrawIOEventRenderer(EventRenderer):
    def render_event(self, event, segment_width, years):
        # Simplified representation; actual implementation will generate XML
        return f"<event name='{event.name}' date='{event.date}'/>"

    def get_drawio_xml(self, event):
        return str(event)

    def render_circle(self, event, root, layer, x, y, style):
        circle = Circle(event.name,
                        layer=layer_id_2(root, name=layer),
                        x=x,
                        y=y,
                        width=18,
                        height=18,
                        style={
                            'fillColor': event.event_type.render_meta.fillColor
                        })
        circle.render(root)
        return


class PowerPointEventRenderer(EventRenderer):
    def __init__(self):
        self.pptx_available = False
        self.MSO_SHAPE = None
        self.RGBColor = None
        self.Pt = None

        try:
            from pptx.enum.shapes import MSO_SHAPE
            from pptx.dml.color import RGBColor
            from pptx.util import Pt

            self.pptx_available = True
            self.MSO_SHAPE = MSO_SHAPE
            self.RGBColor = RGBColor
            self.Pt = Pt
        except ImportError:
            pass

    def render_event(self, event, segment_width, years):
        if not self.pptx_available:
            print("python-pptx library is not installed. Please install it to use the PowerPoint renderer.")
            return

        # Placeholder implementation
        print(f"Rendering event '{event.name}' in PowerPoint format")