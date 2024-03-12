from drawio_roadmaps.drawio.drawio_shapes import Line
from drawio_roadmaps.drawio.drawio_helpers import id_generator, layer_id


class SwimlaneRenderer:
    def render(self, swimlane):
        raise NotImplementedError


class AsciiSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane ASCII: {swimlane.name}"


class DrawIOSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane DrawIO XML: {swimlane.name}"

    def render_line(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style):
        line = Line(root=root,
                    layer=layer,
                    x1=begin_x,
                    y1=begin_y,
                    x2=end_x,
                    y2=end_y,
                    width=width,
                    height=height,
                    style=style)
        line.render(root)
        return


class PowerPointSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane Powerpoint XML: {swimlane.name}"


class StringSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane String: {swimlane.name}"