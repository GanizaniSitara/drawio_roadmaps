from drawio_roadmaps.renderers.roadmap_renderer import RoadmapRenderer


class StringRoadmapRenderer(RoadmapRenderer):
    def render(self, roadmap):
        return str(roadmap)
