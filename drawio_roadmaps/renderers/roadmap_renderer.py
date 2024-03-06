from drawio_roadmaps.enums.event_type import EventType
from drawio_roadmaps.enums.swimlane_type import SwimlaneType

#from drawio_roadmaps.utils import drawio_tools
from drawio_roadmaps.utils import drawio_shared_functions

from drawio_roadmaps.config import DRAWIO_EXECUTABLE_PATH

from lxml import etree
import os


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

# ToDo: Move out of here to drawio objects file

import string
import random
def id_generator(size=22, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_'):
    return ''.join(random.choice(chars) for _ in range(size))

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


def layer_id(root, name):
    for node in root.findall('.//mxCell[@parent="0"]'):
        if node.get('value') == name:
            return node.get('id')
    raise RuntimeError('Layer ' + name + ' not found')


class Label:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;'+
                                'labelBackgroundColor=#ffffff;')
        self.x1=x
        self.y1=y
        self.width=width
        self.height=height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)

class Label:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;'+
                                'labelBackgroundColor=#ffffff;')
        self.x1=x
        self.y1=y
        self.width=width
        self.height=height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)

class Rectangle:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        #self.kwargs['value'] = name
        self.kwargs['style'] = ('text;html=1;strokeColor=none;fillColor=none;align=center;fontFamily=Verdana;' +
                                'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;'+
                                'strokeColor=#000000;')
        self.x1=x
        self.y1=y
        self.width=width
        self.height=height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)

def create_circle(parent, x, y, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator())
        mxcell.set('value', kwargs.get('value', ''))
        mxcell.set('style', kwargs.get('style', ''))
        mxcell.set('vertex', '1')
        mxcell.set('parent', parent)
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
        RuntimeError('Error creating circle')

class Circle:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.kwargs['style'] = ('ellipse;whiteSpace=wrap;html=1;aspect=fixed;' +
                                'strokeWidth=4;spacingTop=55;fontSize=10;fontFamily=Helvetica;')
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def render(self, root):
        layer = layer_id(root, 'Default')
        container = create_circle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)


class DrawIORoadmapRenderer():
    def render(self, roadmap):
        mxGraphModel = self.get_diagram_root()
        root = mxGraphModel.find("root")
        self.append_layers(root)

        years = [str(x) for x in range(roadmap.start_year, roadmap.start_year + roadmap.years)]
        year_lenght_px= 240
        diagram_width = year_lenght_px + year_lenght_px * len(years) #start with swimlane headers equating to width of 1
        swimlane_height = 100

        # ToDo: draw swimlanes headers

        for index, swimlane in enumerate(roadmap.swimlanes):
            xy_cursor = (0, (index + 1) * swimlane_height)



            lane = Rectangle(layer_id(root, 'Default'), xy_cursor[0] + year_lenght_px, xy_cursor[1],
                                        year_lenght_px * (len(years) + 1),
                                        swimlane_height, style='fillColor=#ffffff;strokeColor=#000000;')
            lane.render(root)

            swimlane_label = Label(swimlane.name, xy_cursor[0], xy_cursor[1], year_lenght_px, swimlane_height)
            swimlane_label.render(root)

            xy_timeline_begin = (xy_cursor[0] + year_lenght_px + 50 # start of line magic gap
                                 , xy_cursor[1] + int(swimlane_height / 2))

            xy_timeline_end = (xy_cursor[0] + year_lenght_px + year_lenght_px * (len(years) + 1) - 50 # end of line magic gap
                               , xy_cursor[1] + int(swimlane_height / 2))

            timeline = create_line(layer_id(root, 'Default'), xy_timeline_begin[0], xy_timeline_begin[1], xy_timeline_end[0], xy_timeline_end[1], 2, 2, style='strokeColor=#cfcdc0;')
            root.append(timeline)

            for index, event in enumerate(swimlane.events):
                # need to calculate cursot based ont year and month relative to start of the roadmap, given standard
                # width (year_lenght_px)
                x_event = xy_cursor[0] + year_lenght_px + year_lenght_px * (event.date.year - roadmap.start_year) + year_lenght_px / 12 * (event.date.month - 1)
                # ToDo: hardcoded circle height at 18 for the moment "Station Height"
                y_event = xy_cursor[1] + int(swimlane_height / 2) - 9
                event_label = Circle(event.name, x_event, y_event, 18, 18)
                event_label.render(root)


        drawio_shared_functions.pretty_print(mxGraphModel)

        drawio_shared_functions.finish(mxGraphModel)
        os.system(f'"{DRAWIO_EXECUTABLE_PATH}" output.drawio')

        return "Success!"



    def create_layer(self, name):
        mxcell = etree.Element('mxCell')
        mxcell.set('id', drawio_shared_functions.id_generator())
        mxcell.set('value', name)
        mxcell.set('style', 'locked=0')
        mxcell.set('parent', '0')
        return mxcell

    def append_layers(self, root):
        # back to front order, lowest layer first
        layers = {}
        layers['default'] = self.create_layer('Default')
        for layer in layers.values():
            root.append(layer)
        return root

    def get_diagram_root(self):
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
        # backround layer is always there, we don't draw on it
        background = etree.Element('mxCell')
        background.set('id', '1')
        background.set('style', 'locked=1')
        background.set('parent', '0')
        background.set('visible', '1')
        background.set('value', 'Background')
        root.append(background)
        return mxGraphModel


