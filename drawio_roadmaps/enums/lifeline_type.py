from enum import Enum

from drawio_roadmaps.config_colors import ColorScheme
from drawio_roadmaps.config import RoadmapConfig

color_scheme = ColorScheme(RoadmapConfig.DrawIO.color_scheme.scheme_class)

class LifeLineMetadataDrawio:
    def __init__(self, strokeColor):
        self.strokeColor = strokeColor

class LifeLineType(Enum):
    NONE = ("NONE", LifeLineMetadataDrawio(strokeColor=color_scheme.Colors.Grey))
    INVEST = ("INVEST", LifeLineMetadataDrawio(strokeColor=color_scheme.RAG.Green))
    MAINTAIN = ("MAINTAIN", LifeLineMetadataDrawio(strokeColor=color_scheme.Colors.Blue))
    DIVEST = ("DIVEST", LifeLineMetadataDrawio(strokeColor=color_scheme.RAG.Amber))
    CEASE = ("CEASE", LifeLineMetadataDrawio(strokeColor=color_scheme.RAG.Red))

    def __init__(self, description, metadata_drawio):
        self.description = description
        self.metadata_drawio = metadata_drawio

    @classmethod
    def get_legend_for_lifeline_types(cls):
        return ", ".join([f"{member.description}" for name, member in cls.__members__.items()])
