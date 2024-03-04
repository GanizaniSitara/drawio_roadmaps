
from enum import Enum

from drawio_roadmaps.renderers.roadmap_renderers import AsciiRoadmapRenderer, DrawIORoadmapRenderer
from drawio_roadmaps.renderers.swimlane_renderer import AsciiSwimlaneRenderer, DrawIOSwimlaneRenderer
from drawio_roadmaps.renderers.event_renderer import AsciiEventRenderer, DrawIOEventRenderer

class RendererType(Enum):
    ASCII = "ascii"
    DRAWIO = "drawio"

class RendererManager:
    def __init__(self):
        self.renderer_type = RendererType.ASCII  # Default type
        self.renderers = {
            RendererType.ASCII: {
                "roadmap": AsciiRoadmapRenderer,
                "swimlane": AsciiSwimlaneRenderer,
                "event": AsciiEventRenderer,
            },
            RendererType.DRAWIO: {
                "roadmap": DrawIORoadmapRenderer,
                "swimlane": DrawIOSwimlaneRenderer,
                "event": DrawIOEventRenderer,
            },
        }

    def set_renderer_type(self, renderer_type):
        if renderer_type not in self.renderers:
            raise ValueError("Unsupported renderer type")
        self.renderer_type = renderer_type

    def get_renderer(self, component_type):
        return self.renderers[self.renderer_type][component_type]()
