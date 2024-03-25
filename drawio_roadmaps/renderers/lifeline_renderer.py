from drawio_roadmaps.drawio.drawio_shapes import Line, Label, AngledLine
from drawio_roadmaps.drawio.drawio_utils import id_generator_2, layer_id_2


class LifeLineRenderer:
    def render(self, swimlane):
        raise NotImplementedError


class LifeLineAngledRenderer:
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

    def render_label(self, root, x, y, width, height, value, **kwargs):
        label = Label(
                     value,
                     x=x,
                     y=y,
                     width=width,
                     height=height,
                     **kwargs)
        label.render(root)
        return

class DrawIOLifeLineAngledRenderer(LifeLineAngledRenderer):
    def render(self, lifeline):
        return f"LifeLine DrawIO XML: {lifeline.name}"

    def render_angled_lifeline(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        line = AngledLine(root=root,
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

    def get_angled_lifeline(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        line = AngledLine(root=root,
                    layer=layer,
                    x1=begin_x,
                    y1=begin_y,
                    x2=end_x,
                    y2=end_y,
                    width=width,
                    height=height,
                    style=style,
                    value=kwargs.get('value', ''))
        return line

    def render_label(self, root, x, y, width, height, value, **kwargs):
        label = Label(
                     value,
                     x=x,
                     y=y,
                     width=width,
                     height=height,
                     **kwargs)
        label.render(root)
        return

class PowerPointLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine Powerpoint XML: {lifeline.name}"


class StringLifeLineRenderer(LifeLineRenderer):
    def render(self, lifeline):
        return f"LifeLine String: {lifeline.name}"

