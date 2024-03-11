from enum import Enum
from dataclasses import dataclass

@dataclass
class SwimlaneRenderMeta:
    color: str

class SwimlaneType(Enum):
    PLATFORM = ('=', "Platform", SwimlaneRenderMeta(color="#FF0000"))
    INDEPENDENT = ('—', "Independent", SwimlaneRenderMeta(color="#0F00F0"))  # Em dash

    def __init__(self, marker, description, render_meta):
        self.marker = marker
        self.description = description
        self.render_meta = render_meta

    @classmethod
    def get_legend_for_swimlane_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
