from drawio_roadmaps.drawio.drawio_shapes import Line
from drawio_roadmaps.drawio.drawio_utils import id_generator_2, layer_id_2


class LifeLineRenderer:
    def render(self, swimlane):
        raise NotImplementedError


class AsciiLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine ASCII: {lifeline.name}"


class DrawIOLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine DrawIO XML: {lifeline.name}"

    def render_lifeline(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        line = Line(root=root,
                    layer=layer,
                    x1=begin_x,
                    y1=begin_y,
                    x2=end_x,
                    y2=end_y,
                    width=width,
                    height=height,
                    style=style,
                    value=kwargs.get('value', ''))
        line.render(root)
        return


class PowerPointLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine Powerpoint XML: {lifeline.name}"


class StringLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine String: {lifeline.name}"

