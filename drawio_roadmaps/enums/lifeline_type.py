from enum import Enum
from dataclasses import dataclass

@dataclass
class LifeLineMetadataDrawio:
    strokeColor: str


class LifeLineType(Enum):
    NONE = ("NONE", LifeLineMetadataDrawio(strokeColor="#858585"))
    INVEST = ("INVEST", LifeLineMetadataDrawio(strokeColor="#50C878"))
    MAINTAIN = ("MAINTAIN", LifeLineMetadataDrawio(strokeColor="#A9C5E6"))
    DIVEST = ("DIVEST", LifeLineMetadataDrawio(strokeColor="#FFD700"))
    CEASE = ("CEASE", LifeLineMetadataDrawio(strokeColor="#FF6961"))




    def __init__(self, description, metadata_drawio):
        self.description = description
        self.metadata_drawio = metadata_drawio

    @classmethod
    def get_legend_for_lifeline_types(cls):
        return ", ".join([f"{member.description}" for name, member in cls.__members__.items()])
