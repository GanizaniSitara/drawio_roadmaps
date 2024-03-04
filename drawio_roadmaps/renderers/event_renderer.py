
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


class DrawIOEventRenderer(EventRenderer):
    def render_event(self, event, segment_width, years):
        # Simplified representation; actual implementation will generate XML
        return f"<event name='{event.name}' date='{event.date}'/>"
