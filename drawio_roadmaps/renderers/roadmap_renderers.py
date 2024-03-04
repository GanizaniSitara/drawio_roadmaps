from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType



class RoadmapRenderer:
    def render(self, roadmap):
        raise NotImplementedError


class AsciiRoadmapRenderer():
    def render(self, roadmap):
        pad = "#" * (roadmap.segment_width + 2) + '\n'
        title = f"Roadmap: {roadmap.name}\n"
        roadmap_str = pad + title + pad + EventType.get_legend_for_event_types() + '\n' \
                      + SwimlaneType.get_legend_for_swimlane_types() + '\n'

        horizontal_segment = '+' + '-' * roadmap.segment_width
        roadmap_delim = horizontal_segment * (roadmap.years + 1) + '+\n'
        roadmap_str += roadmap_delim

        header_segment = '| ' + ' ' * (roadmap.segment_width - 1)
        roamap_pad = header_segment * (roadmap.years + 1) + '|\n'
        roadmap_str += roamap_pad

        # put columne title in first segment and pad till segment width
        roadmap_header_text = '| ' + roadmap.swimlane_column_title
        roadmap_header_text += ' ' * (roadmap.segment_width - len(roadmap_header_text)) + ' |'

        # in second and following segments, center the text, which will be the years
        for year in range(roadmap.start_year, roadmap.end_year):
            year_str = f"{year}"
            year_str = year_str.center(roadmap.segment_width)
            roadmap_header_text += year_str + '|'
        roadmap_str += roadmap_header_text + '\n'
        roadmap_str += roamap_pad
        roadmap_str += roadmap_delim

        for swimlane in roadmap.swimlanes:
            roadmap_str += swimlane.render(segment_width=roadmap.segment_width, years=roadmap.years)
            roadmap_str += roadmap_delim

        return roadmap_str


class DrawIORoadmapRenderer():
    def render(self, roadmap):
        pass
        # Implement DrawIO XML rendering logic
