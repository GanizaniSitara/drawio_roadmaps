

class SwimlaneRenderer:
    def render(self, swimlane):
        raise NotImplementedError

class AsciiSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        # Implement ASCII rendering logic for swimlane
        return f"Swimlane ASCII: {swimlane.name}"


class DrawIOSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        # Implement DrawIO XML rendering logic for swimlane
        return f"Swimlane DrawIO XML: {swimlane.name}"
