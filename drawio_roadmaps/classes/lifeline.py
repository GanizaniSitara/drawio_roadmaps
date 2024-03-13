from drawio_roadmaps.renderer_manager import RendererManager

renderer_manager = RendererManager()

class LifeLine:
    def __init__(self, name, roadmap=None, swimlane=None, from_date=None, to_date=None):
        self.name = name
        self.renderer = renderer_manager.get_renderer("lifeline")
        self.roadmap = roadmap
        self.swimlane = swimlane
        self.roadmap_renderer = None

    def __str__(self, indent=0):
        lifeline_str = ' ' * indent + f"LifeLine: {self.name} [{self.type.metadata_drawio.color}]\n"
        for event in self.events:
            lifeline_str += event.__str__(indent + 4)
        lifeline_str += '\n'
        return lifeline_str

    def set_renderer(self, renderer):
        self.renderer = renderer