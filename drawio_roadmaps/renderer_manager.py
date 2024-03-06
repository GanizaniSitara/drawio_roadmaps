
from enum import Enum

from drawio_roadmaps.renderers.roadmap_renderer import AsciiRoadmapRenderer, DrawIORoadmapRenderer
from drawio_roadmaps.renderers.swimlane_renderer import AsciiSwimlaneRenderer, DrawIOSwimlaneRenderer
from drawio_roadmaps.renderers.event_renderer import AsciiEventRenderer, DrawIOEventRenderer

class RendererType(Enum):
    ASCII = "ascii"
    DRAWIO = "drawio"

class RendererManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RendererManager, cls).__new__(cls)
            cls._instance.renderer_type = RendererType.ASCII  # Default type
            cls._instance.renderers = {
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
        return cls._instance

    def set_renderer_type(self, renderer_type):
        if renderer_type not in self.renderers:
            raise ValueError("Unsupported renderer type")
        self.renderer_type = renderer_type

    def get_renderer(self, component_type):
        renderer_class = self.renderers[self.renderer_type].get(component_type)
        return renderer_class()
