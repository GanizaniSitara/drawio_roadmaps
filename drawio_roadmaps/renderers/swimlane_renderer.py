from datetime import datetime

from drawio_roadmaps.drawio.drawio_shapes import Line
from drawio_roadmaps.drawio.drawio_utils import id_generator_2, layer_id_2

from drawio_roadmaps.config import RoadmapConfig as config


class SwimlaneRenderer:
    def render(self, swimlane):
        raise NotImplementedError


class AsciiSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):

        # ToDo: should be handled in config, we should also remember why this is ... :S
        if config.Global.show_quarters:
            segment_width = config.Ascii.segment_width - 1
        else:
            segment_width = config.Ascii.segment_width
        years = swimlane.roadmap.years

        swimlane_pad = '|' + ' ' * segment_width + '|' + ' ' * (years * (segment_width + 1) - 1) + '|\n'

        swimlane_str = f"| {swimlane.name}"
        swimlane_str += ' ' * (segment_width - len(swimlane_str) + 1) + '|'

        events_visual_line = (' ' + swimlane.get_swimlane_marker() * (((segment_width + 1) * (years)) - 12)
                         + '>>>       ' + '|\n')
        events_str = ''

        for event in swimlane.events:
            # ToDo: should go into event renderer
            # Calculate the offset based on the event's date
            offset = (event.date.year - swimlane.roadmap.start_year) * 12 + event.date.month
            offset_segments = offset * 3  # 3 segments per month

            # Replace '=' with '#' to visually represent an event
            if offset_segments < len(events_visual_line) - 1:  # Ensure within bounds
                events_visual_line = (events_visual_line[:offset_segments] +
                                      event.get_event_marker() + events_visual_line[
                                                                                  offset_segments + 1:])

            # Add spaces for the offset
            event_str = '|' +  ' ' * segment_width + '|' + ' ' * offset_segments + str(event)
            event_str += ' ' * ((segment_width + 1) * (years + 1) - len(event_str)) + '|\n'
            events_str += event_str

        # events_visual_line = '|' + ' ' * segment_width + '|' + events_visual_line

        result = swimlane_pad + swimlane_str + events_visual_line + events_str + swimlane_pad

        # GPT-4 unsuccessful had to be done by hand
        for lifeline in swimlane.lifelines:
            # Check if from_date is provided; otherwise, start at the beginning of the roadmap
            character_per_days = 365 // segment_width

            if lifeline.from_date is not None:
                start_offset = lifeline.from_date - datetime.strptime(str(swimlane.roadmap.start_year), "%Y").date()
                start_offset = start_offset.days // character_per_days
            else:
                start_offset = 1

            # Check if to_date is provided; otherwise, end at the last year of the roadmap
            if lifeline.to_date is not None:
                end_offset = lifeline.to_date - datetime.strptime(str(swimlane.roadmap.start_year), "%Y").date()
                end_offset = end_offset.days // character_per_days
                ending = '†'
            else:
                end_offset = (years * segment_width) - 7
                ending = '>>>'

            # Construct the lifeline string with appropriate padding and periods
            lifeline_str = (f"| {lifeline.name}")
            lifeline_str += ' ' * (segment_width - len(lifeline_str) + 1) + '|'

            leading_space = ' ' * start_offset
            lifeline_str += leading_space
            lifeline_space = '.' * (end_offset - start_offset) + ending
            trailing_space = ' ' * ((years * (segment_width + 1) - len(leading_space + lifeline_space)) - 1)
            lifeline_str += lifeline_space + trailing_space + '|\n'

            # Append the constructed lifeline string to the result with a newline
            result += lifeline_str

        return result


class DrawIOSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane DrawIO XML: {swimlane.name}"

    def render_swimline(self, root, layer, begin_x, begin_y, end_x, end_y, width, height, style, **kwargs):
        line = Line(root=root,
                    layer=layer,
                    x1=begin_x,
                    y1=begin_y,
                    x2=end_x,
                    y2=end_y,
                    width=width,
                    height=height,
                    style=style,
                    value=kwargs.get('value', ''))
        line.render(root)
        return


class PowerPointSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane Powerpoint XML: {swimlane.name}"


class StringSwimlaneRenderer(SwimlaneRenderer):
    def render(self, swimlane):
        return f"Swimlane String: {swimlane.name}"