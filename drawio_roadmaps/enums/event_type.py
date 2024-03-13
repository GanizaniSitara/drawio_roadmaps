from enum import Enum
from dataclasses import dataclass

@dataclass
class DrawioRenderMeta:
    fillColor: str = "#FFFFFF"
    dashed: bool = False
    dashPattern: str = "1 1"
    strokeColor: str = "#000000"


class EventType(Enum):
    UNFUNDED = ('O', "Unfunded Milestone", DrawioRenderMeta(fillColor="#FFFFFF", dashed=True, dashPattern="1 1"))
    TARGET = ('@', "Target Milestone", DrawioRenderMeta(fillColor="#FFFFFF"))
    COMPLETED = ('X', "Completed Milestone", DrawioRenderMeta(fillColor="#4169E1"))
    RETIREMENT = ('†', "Point of Retirement", DrawioRenderMeta(fillColor="#FF6961"))
    DECISION = ('#', "Strategy Decision Point", DrawioRenderMeta(fillColor="#FFFF00"))

    # Leaving this here for reference
    # style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=4;spacingTop=55;fontSize=10;
    #       fontFamily=Helvetica;fillStyle=auto;
    #       gradientDirection=radial;gradientColor=#ffffff;
    #       fillColor=#ff0000;" vertex="1" parent="1"

    def __init__(self, marker, description, render_meta):
        self.marker = marker
        self.description = description
        self.render_meta = render_meta

    @classmethod
    def get_legend_for_event_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
