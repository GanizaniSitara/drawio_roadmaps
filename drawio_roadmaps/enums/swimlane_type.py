from enum import Enum
from dataclasses import dataclass

@dataclass
class SwimlaneMetadataDrawio:
    strokeColor: str


class SwimlaneMetadataAscii:
    marker: str


class SwimlaneType(Enum):
    PLATFORM = ('=', "Platform", SwimlaneMetadataDrawio(strokeColor="#FFA500"))
    INDEPENDENT = ('—', "Independent", SwimlaneMetadataDrawio(strokeColor="#800080"))

    def __init__(self, marker, description, metadata_drawio):
        self.marker = marker
        self.description = description
        self.metadata_drawio = metadata_drawio

    @classmethod
    def get_legend_for_swimlane_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
