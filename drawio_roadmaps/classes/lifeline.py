from drawio_roadmaps.renderer_manager import RendererManager
from drawio_roadmaps.enums.lifeline_type import LifeLineType

renderer_manager = RendererManager()

class LifeLine:
    def __init__(self, name, roadmap=None, swimlane=None, from_date=None, to_date=None,
                 lifeline_type: LifeLineType = LifeLineType.NONE):
        self.name = name
        self.renderer = renderer_manager.get_renderer("lifeline")
        self.roadmap = roadmap
        self.swimlane = swimlane
        self.roadmap_renderer = None
        self.from_date = from_date
        self.to_date = to_date
        self.type = lifeline_type
        self.render_meta = None
        self.merge_to = None

    def __str__(self, indent=0):
        lifeline_str = ' ' * indent + f"LifeLine: {self.name} [{self.type.metadata_drawio.color}]\n"
        for event in self.events:
            lifeline_str += event.__str__(indent + 4)
        lifeline_str += '\n'
        return lifeline_str

    def set_from(self, from_date):
        self.from_date = from_date

    def set_to(self, to_date):
        self.to_date = to_date

    def set_lifeline_type(self, type):
        self.type = type

    def set_merge_to(self, merge_to):
        self.merge_to = merge_to

    def set_renderer(self, renderer):
        self.renderer = renderer

    def render(self, root):
        result = renderer_manager.get_renderer('lifeline').render(self)
        return result

    def tubemap_lifeline(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        renderer = renderer_manager.get_renderer('lifeline')
        renderer.render_lifeline(root=root,
                                 layer=layer,
                                 begin_x=begin_x,
                                 begin_y=begin_y,
                                 end_x=end_x,
                                 end_y=end_y,
                                 width=width,
                                 height=height,
                                 style=style,
                                 value=kwargs.get('value', ''))
        return

    def tubemap_lifeline_angled(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        # we dont render as the order matters and the merging lifelines need to be added the last
        renderer = renderer_manager.get_renderer('lifeline_angled')
        line = renderer.get_angled_lifeline(root=root,
                                 layer=layer,
                                 begin_x=begin_x,
                                 begin_y=begin_y,
                                 end_x=end_x,
                                 end_y=end_y,
                                 width=width,
                                 height=height,
                                 style=style,
                                 value=kwargs.get('value', ''))
        return line


    def tubemap_lifeline_label(self, root, x, y, width, height, value, **kwargs):
        renderer = renderer_manager.get_renderer('lifeline')
        renderer.render_label(root=root,
                              x=x,
                              y=y,
                              width=width,
                              height=height,
                              value=value,
                              style=kwargs.get('style', ''))
        return