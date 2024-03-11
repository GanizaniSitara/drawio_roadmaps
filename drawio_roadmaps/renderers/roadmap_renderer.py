from drawio_roadmaps.drawio.drawio_shapes import Circle
from drawio_roadmaps.drawio.drawio_helpers import id_generator, layer_id
from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType
from drawio_roadmaps.drawio import drawio_shared_functions

from drawio_roadmaps.config import DRAWIO_EXECUTABLE_PATH
from drawio_roadmaps.config import RoadmapConfig as config

from lxml import etree
import os


class RoadmapRenderer:
    def render(self, roadmap):
        raise NotImplementedError


class StringRoadmapRenderer():
    def render(self, roadmap):
        return str(roadmap)


class AsciiRoadmapRenderer():
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
            result += swimlane.render(segment_width=self.segment_width, years=roadmap.years)
            result += roadmap_delim

        return result


# ToDo: Move out of here to drawio objects file

def create_rectangle(parent, x, y, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        mxcell.set('value', kwargs.get('value', ''))
        mxcell.set('style', kwargs.get('style', ''))
        mxcell.set('parent', parent)
        mxcell.set('vertex', '1')

        mxGeometry = etree.Element('mxGeometry')
        mxGeometry.set('x', str(x))
        mxGeometry.set('y', str(y))
        mxGeometry.set('width', str(width))
        mxGeometry.set('height', str(height))
        mxGeometry.set('as', 'geometry')
        mxcell.append(mxGeometry)
        return mxcell
    except Exception as e:
        print(e)
        RuntimeError('Error creating rectangle')


def create_line(parent, x1, y1, x2, y2, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        if 'value' in kwargs:
            mxcell.set('value', kwargs.get('value', ''))
        mxcell.set('style', kwargs.get('style', ''))
        mxcell.set('parent', parent)
        mxcell.set('edge', '1')
        mxGeometry = etree.Element('mxGeometry')
        mxGeometry.set('width', str(width))
        mxGeometry.set('height', str(height))
        mxGeometry.set('relative', '1')
        mxGeometry.set('as', 'geometry')
        mxSourcePoint = etree.Element('mxPoint')
        mxSourcePoint.set('x', str(x1))
        mxSourcePoint.set('y', str(y1))
        mxSourcePoint.set('as', 'sourcePoint')
        mxGeometry.append(mxSourcePoint)
        mxTargetPoint = etree.Element('mxPoint')
        mxTargetPoint.set('x', str(x2))
        mxTargetPoint.set('y', str(y2))
        mxTargetPoint.set('as', 'targetPoint')
        mxGeometry.append(mxTargetPoint)
        mxcell.append(mxGeometry)
        return mxcell
    except Exception as e:
        print(e)
        RuntimeError('Error creating line')


class Label:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;' +
                                'labelBackgroundColor=#ffffff;')
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)


class Label:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;' +
                                'labelBackgroundColor=#ffffff;')
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)


class Rectangle:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;' +
                                'strokeColor=#000000;')
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)


class DrawIORoadmapRenderer:

    def render(self, roadmap):

        mxGraphModel = self.get_diagram_root()
        root = mxGraphModel.find("root")
        self.append_layers(root)

        years = [str(x) for x in range(roadmap.start_year, roadmap.start_year + roadmap.years)]
        year_lenght_px = 240
        diagram_width = year_lenght_px + year_lenght_px * len(
            years)  # start with swimlane headers equating to width of 1
        swimlane_height = 100

        # ToDo: draw swimlanes headers
        swimlane_header = Rectangle(roadmap.swimlane_column_title, 0, 0, year_lenght_px, swimlane_height,
                                    style='fillColor=#ffffff;strokeColor=#000000;')
        swimlane_header.render(root)

        for index, year in enumerate(years):
            xy_cursor = (year_lenght_px * (index + 1), 0)
            year_label = Rectangle(year,
                                   x=xy_cursor[0],
                                   y=xy_cursor[1],
                                   width=year_lenght_px,
                                   height=swimlane_height,
                                   style='fillColor=#ffffff;strokeColor=#000000;')
            year_label.render(root)

        for index, swimlane in enumerate(roadmap.swimlanes):
            # allow for the header
            xy_cursor = (0, (index + 1) * swimlane_height)

            lane = Rectangle('', xy_cursor[0] + year_lenght_px, xy_cursor[1],
                             year_lenght_px * (len(years)),
                             swimlane_height, style='fillColor=#ffffff;strokeColor=#000000;')
            lane.render(root)

            swimlane_label = Rectangle(swimlane.name, xy_cursor[0], xy_cursor[1], year_lenght_px, swimlane_height)
            swimlane_label.render(root)

            xy_timeline_begin = (xy_cursor[0] + year_lenght_px + 50  # start of line magic gap
                                 , xy_cursor[1] + int(swimlane_height / 2))

            xy_timeline_end = (
            xy_cursor[0] + year_lenght_px + year_lenght_px * (len(years)) - 50  # end of line magic gap
            , xy_cursor[1] + int(swimlane_height / 2))

            timeline = create_line(layer_id(root, 'Default'), xy_timeline_begin[0], xy_timeline_begin[1],
                                   xy_timeline_end[0], xy_timeline_end[1], 2, 2,
                                   style='strokeColor=#FF9933;strokeWidth=5;endArrow=doubleBlock;')
            root.append(timeline)

            for event in swimlane.events:
                x = xy_cursor[0] + \
                    year_lenght_px + \
                    year_lenght_px * (event.date.year - roadmap.start_year) + \
                    year_lenght_px / 12 * (event.date.month - 1)

                # ToDo: hardcoded half circle height @ 9px (total size 18px)
                # should go to config, although unlikely to change
                # so 9 in the line below for half tube station height

                y = xy_cursor[1] + int(swimlane_height / 2) - 9
                event.tubemap_station(root=root,
                                      layer="Default",
                                      x=x,
                                      y=y,
                                      style={
                                          'fillColor': event.event_type.render_meta.fillColor
                                      })

        # "Pretty Print" to console is not really required but we like to pretty pring the XML just for comparison
        # Encoding required for use in Confluence/Web
        # Open desktop drawio for convenience

        drawio_shared_functions.pretty_print_to_console(mxGraphModel)
        drawio_shared_functions.encode_and_save_to_file(mxGraphModel)
        os.system(f'"{DRAWIO_EXECUTABLE_PATH}" output.drawio')

        return "DrawIO roadmap generated successfully!"

    @staticmethod
    def create_layer(self, name):
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        mxcell.set('value', name)
        mxcell.set('style', 'locked=0')
        mxcell.set('parent', '0')
        return mxcell

    def append_layers(self, root):
        # back to front order, lowest layer first
        layers = {'default': self.create_layer(self, name='Default')}
        for layer in layers.values():
            root.append(layer)
        return root

    @staticmethod
    def get_diagram_root():
        mxGraphModel = etree.Element('mxGraphModel')
        mxGraphModel.set('dx', '981')
        mxGraphModel.set('dy', '650')
        mxGraphModel.set('grid', '1')
        mxGraphModel.set('gridSize', '10')
        mxGraphModel.set('guides', '1')
        mxGraphModel.set('tooltips', '1')
        mxGraphModel.set('connect', '1')
        mxGraphModel.set('arrows', '1')
        mxGraphModel.set('fold', '1')
        mxGraphModel.set('page', '1')
        mxGraphModel.set('pageScale', '1')
        mxGraphModel.set('pageWidth', '816')
        mxGraphModel.set('pageHeight', '1056')
        mxGraphModel.set('math', '0')
        mxGraphModel.set('shadow', '0')

        root = etree.Element('root')
        mxGraphModel.append(root)
        # to cell is always there all the other layers inherit from it
        mxcell = etree.Element('mxCell')
        mxcell.set('id', '0')
        root.append(mxcell)
        # background layer is always there, we don't draw on it
        background = etree.Element('mxCell')
        background.set('id', '1')
        background.set('style', 'locked=1')
        background.set('parent', '0')
        background.set('visible', '1')
        background.set('value', 'Background')
        root.append(background)
        return mxGraphModel


class PowerPointRoadmapRenderer:
    def __init__(self):
        self.pptx_available = False
        self.Presentation = None
        self.Inches = None
        self.Pt = None
        self.RGBColor = None
        self.MSO_CONNECTOR = None

        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt
            from pptx.dml.color import RGBColor
            from pptx.enum.shapes import MSO_CONNECTOR

            self.pptx_available = True
            self.Presentation = Presentation
            self.Inches = Inches
            self.Pt = Pt
            self.RGBColor = RGBColor
            self.MSO_CONNECTOR = MSO_CONNECTOR
        except ImportError:
            pass

    def render(self, roadmap):
        if not self.pptx_available:
            print("python-pptx library is not installed. Please install it to use the PowerPoint renderer.")
            return "PowerPoint roadmap generation failed. Missing dependencies."

        prs = self.Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide layout

        # Add a text box for the title
        title_textbox = slide.shapes.add_textbox(self.Inches(0.5), self.Inches(0.5), self.Inches(9), self.Inches(1))
        title_textbox.text = "Roadmap"
        title_textbox.text_frame.paragraphs[0].font.size = self.Pt(24)
        title_textbox.text_frame.paragraphs[0].font.bold = True

        year_length_px = self.Inches(2)
        swimlane_height = self.Inches(0.5)
        start_x = self.Inches(0.5)
        start_y = self.Inches(1.5)

        years = [str(x) for x in range(roadmap.start_year, roadmap.start_year + roadmap.years)]

        for index, swimlane in enumerate(roadmap.swimlanes):
            slide.shapes.add_textbox(start_x, start_y + index * swimlane_height, year_length_px, swimlane_height)
            textbox = slide.shapes.add_textbox(start_x, start_y + index * swimlane_height, year_length_px,
                                               swimlane_height)
            textbox.text = swimlane.name
            textbox.text_frame.paragraphs[0].font.size = self.Pt(12)

            timeline_start_x = start_x + year_length_px
            timeline_end_x = timeline_start_x + year_length_px * len(years)
            timeline_y = start_y + index * swimlane_height + swimlane_height / 2

            line = slide.shapes.add_connector(self.MSO_CONNECTOR.STRAIGHT, timeline_start_x, timeline_y, timeline_end_x,
                                              timeline_y)
            line.line.color.rgb = self.RGBColor(0, 0, 0)

            for event in swimlane.events:
                event.render(year_length_px, roadmap.years)

        prs.save("roadmap.pptx")
        return "PowerPoint roadmap generated successfully!"
