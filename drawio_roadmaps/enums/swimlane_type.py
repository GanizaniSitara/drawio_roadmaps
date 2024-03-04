from enum import Enum

class SwimlaneType(Enum):
    PLATFORM = ('=', "Platform")
    INDEPENDENT = ('—', "Independent")  # Em dash

    def __init__(self, marker, description):
        self.marker = marker
        self.description = description

    @classmethod
    def get_legend_for_swimlane_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
