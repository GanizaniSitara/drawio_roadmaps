from enum import Enum
from dataclasses import dataclass

from drawio_roadmaps.config_colors import ColorScheme
from drawio_roadmaps.config import RoadmapConfig

color_scheme = ColorScheme(RoadmapConfig.DrawIO.color_scheme.scheme_class)

@dataclass
class SwimlaneMetadataDrawio:
    strokeColor: str


class SwimlaneMetadataAscii:
    marker: str


class SwimlaneType(Enum):
    PLATFORM = ('=', "Platform", SwimlaneMetadataDrawio(strokeColor=color_scheme.Colors.Yellow))
    INDEPENDENT = ('—', "Independent", SwimlaneMetadataDrawio(strokeColor=color_scheme.Colors.Purple))

    def __init__(self, marker, description, metadata_drawio):
        self.marker = marker
        self.description = description
        self.metadata_drawio = metadata_drawio

    @classmethod
    def get_legend_for_swimlane_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
