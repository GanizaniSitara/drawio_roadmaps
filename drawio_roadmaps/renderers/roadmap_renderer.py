
from abc import ABC, abstractmethod


class RoadmapRenderer(ABC):
    @abstractmethod
    def render(self, roadmap):
        pass


