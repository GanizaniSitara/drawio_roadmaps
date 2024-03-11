from lxml import etree
from drawio_roadmaps.drawio.drawio_helpers import id_generator, layer_id


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
            layer = layer_id(root, 'Default')
        container = create_circle(layer, self.x1, self.y1, self.width, self.height, **self.kwargs)
        self.container = container
    def render(self, root):
        self._generate(root)
        root.append(self.container)

    def append_to(self, root):
        root.append(self.container)

