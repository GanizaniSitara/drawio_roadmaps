

class SwimlaneRenderer:
    def render(self, swimlane):
        raise NotImplementedError

class AsciiSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane ASCII: {swimlane.name}"


class DrawIOSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane DrawIO XML: {swimlane.name}"

class PowerPointSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane Powerpoint XML: {swimlane.name}"

class StringSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane String: {swimlane.name}"