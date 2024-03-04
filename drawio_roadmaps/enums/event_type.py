from enum import Enum

class EventType(Enum):
    UNFUNDED = ('O', "Unfunded Milestone")
    TARGET = ('@', "Target Milestone")
    COMPLETED = ('X', "Completed Milestone")
    RETIREMENT = ('†', "Point of Retirement")
    DECISION = ('#', "Strategy Decision Point")

    def __init__(self, marker, description):
        self.marker = marker
        self.description = description

    @classmethod
    def get_legend_for_event_types(cls):
        return ", ".join([f"{member.marker} {member.description}" for name, member in cls.__members__.items()])
