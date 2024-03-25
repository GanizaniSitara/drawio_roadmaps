from lxml import etree
from drawio_roadmaps.drawio.drawio_utils import id_generator_2, layer_id_2


def create_angled_line(parent, x1, y1, x2, y2, width, height, **kwargs):
    # the further away from the origin, the bigger the angle
    # we dont' use this now as we want the angle consistent
    # for typography purposes (?)
    # angle = (x2-x1)/(y2-y1)

    if not 'points_array' in kwargs:
        kwargs['points_array'] = []
        kwargs['points_array'].append(((x2-(abs(y1-y2) *0.75)), y1))

    # print(kwargs['points_array'])

    mxcell = etree.Element('mxCell')
    mxcell.set('id', id_generator_2())
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
    mxcell.append(mxGeometry)

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

    mxArray = etree.Element('Array')
    mxArray.set('as', 'points')
    for i, point in enumerate(kwargs['points_array']):
        mxPoint = etree.Element('mxPoint')
        mxPoint.set('x', str(point[0]))
        mxPoint.set('y', str(point[1]))
        mxArray.append(mxPoint)
        mxGeometry.append(mxArray)

    return mxcell

class AngledLine:
    def __init__(self, root, layer, x1, y1, x2, y2, width, height, **kwargs):
        self.root = root
        self.layer = layer
        self.style =  {
            'html': '1',
            'rounded': '0',
            'endFill': '1',
        }
        style = kwargs.get('style', {})
        self.style.update(style)
        self.style = '' + ';'.join(f'{key}={value}' for key, value in self.style.items()) + ';'
        self.kwargs = {}
        self.kwargs['style'] = self.style
        self.kwargs['value'] = kwargs.get('value', '')
        # style="endArrow=doubleBlock;html=1;rounded=0;strokeWidth=5;endFill=1;fillColor=#fad7ac;strokeColor=#b48e04;

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height
        self.container = None

    def __str__(self):
        if self.container is None:
            self._generate()
        result = etree.tostring(self.container, pretty_print=True).decode('utf-8')
        return result

    def _generate(self, root=None):
        if root is None:
            layer = '00000000'
        else:
            layer = layer_id_2(root, name=self.layer)
        container = create_angled_line(layer, self.x1, self.y1, self.x2, self.y2, self.width, self.height,
                                **self.kwargs)
        self.container = container

    def render(self, root):
        self._generate(root)
        root.append(self.container)

    def append_to(self, root):
        root.append(self.container)


def create_circle(parent, x, y, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator_2())
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
        self.style = {
            'whiteSpace': 'wrap',
            'html': '1',
            'aspect': 'fixed',
            'strokeWidth': '4',
            'spacingTop': '55',
            'fontSize': '10',
            'fontFamily': 'Helvetica',
        }
        self.dashed = {
            'dashed':'1',
            'dashPattern':'1 1',
            'strokeColor': '#ff0000'
        }
        self.radial = {
            'fillStyle':'auto',
            'gradientDirection':'radial',
            'gradientColor':'#ffffff'
        }

        ## self.style.update(self.radial)
        self.style.update(kwargs.get('style'))
        self.style =  'ellipse;' + ';'.join(f'{key}={value}' for key, value in self.style.items()) + ';'
        self.kwargs = {}
        self.kwargs['style'] = \
            ('ellipse;whiteSpace=wrap;html=1;aspect=fixed;' +
             'strokeWidth=4;spacingTop=55;fontSize=10;fontFamily=Helvetica;')
        print(self.style)
        print(self.kwargs['style'])
        self.kwargs['style'] = self.style
        #assert self.style == self.kwargs['style']
        self.kwargs['value'] = name
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height
        self.container = None

    def __str__(self):
        if self.container is None:
            self._generate()
        result = etree.tostring(self.container, pretty_print=True).decode('utf-8')
        return result

    def _generate(self, root=None):
        if root is None:
            layer = '00000000'
        else:
            layer = layer_id_2(root, 'Default')
        container = create_circle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        self.container = container

    def render(self, root):
        self._generate(root)
        root.append(self.container)

    def append_to(self, root):
        root.append(self.container)


def create_line(parent, x1, y1, x2, y2, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator_2())
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

class Line:
    def __init__(self, root, layer, x1, y1, x2, y2, width, height, **kwargs):
        self.root = root
        self.layer = layer
        self.style =  {
            'html': '1',
            'rounded': '0',
            'endFill': '1',
        }
        style = kwargs.get('style', {})
        self.style.update(style)
        self.style = '' + ';'.join(f'{key}={value}' for key, value in self.style.items()) + ';'
        self.kwargs = {}
        self.kwargs['style'] = self.style
        self.kwargs['value'] = kwargs.get('value', '')
        # style="endArrow=doubleBlock;html=1;rounded=0;strokeWidth=5;endFill=1;fillColor=#fad7ac;strokeColor=#b48e04;

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height
        self.container = None

    def __str__(self):
        if self.container is None:
            self._generate()
        result = etree.tostring(self.container, pretty_print=True).decode('utf-8')
        return result

    def _generate(self, root=None):
        if root is None:
            layer = '00000000'
        else:
            layer = layer_id_2(root, name=self.layer)
        container = create_line(layer, self.x1, self.y1, self.x2, self.y2, self.width, self.height,
                                **self.kwargs)
        self.container = container

    def render(self, root):
        self._generate(root)
        root.append(self.container)

    def append_to(self, root):
        root.append(self.container)


def create_rectangle(parent, x, y, width, height, **kwargs):
    try:
        mxcell = etree.Element('mxCell')
        mxcell.set('id', id_generator_2())
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


class Label:

    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = {'value': name}
        self.style = {
            'html': '1',
            'strokeColor': 'none',
            'fillColor': 'none',
            'align': 'center',
            'fontFamily': 'Helvetica',
            'verticalAlign': 'middle',
            #'whiteSpace': 'wrap',
            'rounded': '0',
            'fontSize': '14',
            'labelBackgroundColor': '#ffffff'
        }

        self.style.update(kwargs.get('style', {}))
        self.kwargs['style'] = 'text;' + ';'.join(f'{key}={value}' for key, value in self.style.items())

        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def render(self, root):
        layer = layer_id_2(root, 'Default')
        container = create_rectangle(layer, self.x, self.y, self.width, self.height, **self.kwargs)
        root.append(container)


class Rectangle:
    def __init__(self, name, x, y, width, height, **kwargs):
        self.kwargs = kwargs
        self.kwargs['value'] = name
        self.style = {
            'html': '1',
            'strokeColor': 'none',
            'fillColor': 'none',
            'align': 'center',
            'fontFamily': 'Helvetica',
            'verticalAlign': 'middle',
            'whiteSpace': 'wrap',
            'rounded': '0',
            'fontSize': '14',
            'strokeColor': '#000000',  # Note: 'strokeColor' appears twice, the last occurrence overrides the first
        }

        self.style.update(kwargs.get('style', {}))

        self.kwargs['style'] = 'text;' + ';'.join(f'{key}={value}' for key, value in self.style.items())

        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height

    def render(self, root):
        layer = layer_id_2(root, 'Default')
        container = create_rectangle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        root.append(container)
