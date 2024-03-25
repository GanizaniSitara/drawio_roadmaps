
from enum import Enum

from drawio_roadmaps.renderers.roadmap_renderer import AsciiRoadmapRenderer, DrawIORoadmapRenderer, PowerPointRoadmapRenderer, StringRoadmapRenderer
from drawio_roadmaps.renderers.swimlane_renderer import AsciiSwimlaneRenderer, DrawIOSwimlaneRenderer, PowerPointSwimlaneRenderer, StringSwimlaneRenderer
from drawio_roadmaps.renderers.event_renderer import AsciiEventRenderer, DrawIOEventRenderer, PowerPointEventRenderer, StringEventRenderer

from drawio_roadmaps.renderers.lifeline_renderer import AsciiLifeLineRenderer, DrawIOLifeLineRenderer, PowerPointLifeLineRenderer, StringLifeLineRenderer
from drawio_roadmaps.renderers.lifeline_renderer import DrawIOLifeLineAngledRenderer

class RendererType(Enum):
    ASCII = "ascii"
    DRAWIO = "drawio"
    POWERPOINT = "powerpoint"
    STRING = "string"

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
                    "lifeline": AsciiLifeLineRenderer,
                },
                RendererType.DRAWIO: {
                    "roadmap": DrawIORoadmapRenderer,
                    "swimlane": DrawIOSwimlaneRenderer,
                    "event": DrawIOEventRenderer,
                    "lifeline": DrawIOLifeLineRenderer,
                    "lifeline_angled": DrawIOLifeLineAngledRenderer,
                },
                RendererType.POWERPOINT: {
                    "roadmap": PowerPointRoadmapRenderer,
                    "swimlane": PowerPointSwimlaneRenderer,
                    "event": PowerPointEventRenderer,
                    "lifeline": PowerPointLifeLineRenderer,
                },
                RendererType.STRING: {
                    "roadmap": StringRoadmapRenderer,
                    "swimlane": StringSwimlaneRenderer,
                    "event": StringEventRenderer,
                    "lifeline": StringLifeLineRenderer,
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
