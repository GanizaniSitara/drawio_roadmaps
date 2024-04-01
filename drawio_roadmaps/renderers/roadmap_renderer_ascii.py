from drawio_roadmaps.config import RoadmapConfig as config
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType
from drawio_roadmaps.renderers.roadmap_renderer import RoadmapRenderer


class AsciiRoadmapRenderer(RoadmapRenderer):
    def __init__(self):
        # The quarters don't line up properly so extend if showing quarter
        # also likely to have more dense data so this is likely beneficial anyway
        if config.Global.show_quarters:
            self.segment_width = config.Ascii.segment_width - 1
        else:
            self.segment_width = config.Ascii.segment_width

    def render(self, roadmap):
        result = ""

        # Draw the title and legend
        pad = "#" * (self.segment_width + 2) + '\n'
        title = f"Roadmap: {roadmap.name}\n"
        title_and_legend = pad + title + pad + EventType.get_legend_for_event_types() + '\n' \
                           + SwimlaneType.get_legend_for_swimlane_types() + '\n'
        result += title_and_legend

        # Draw the header
        horizontal_segment = '+' + '-' * self.segment_width
        roadmap_delim = horizontal_segment * (roadmap.years + 1) + '+\n'
        result += roadmap_delim

        header_segment = '| ' + ' ' * (self.segment_width - 1)
        roamap_pad = header_segment * (roadmap.years + 1) + '|\n'
        result += roamap_pad

        # put columne title in first segment and pad till segment width
        roadmap_header_text = '| ' + roadmap.swimlane_column_title
        roadmap_header_text += ' ' * (self.segment_width - len(roadmap_header_text)) + ' |'

        # in second and following segments, center the text, which will be the years
        for year in range(roadmap.start_year, roadmap.end_year):
            year_str = f"{year}"
            year_str = year_str.center(self.segment_width)
            roadmap_header_text += year_str + '|'
        result += roadmap_header_text + '\n'

        if config.Global.show_quarters:
            result += roamap_pad
            result += '| ' + ' ' * (self.segment_width - 1) + '|'
            # Draw the quarter markers
            for year in range(roadmap.years):
                for quarter in range(1, 5):
                    quarter_marker = f"Q{quarter}"
                    result += '   ' + quarter_marker + '   |'

            result += '\n'
        else:
            result += roamap_pad
        result += roadmap_delim

        for swimlane in roadmap.swimlanes:

            result += swimlane.render()
            result += roadmap_delim

        return result
