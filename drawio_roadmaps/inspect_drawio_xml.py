import drawio_roadmaps.drawio.drawio_serialization as drawio_tools
import lxml.etree as etree
from xml.etree import ElementTree

# x = etree.parse('examples/inspect.drawio')
x = etree.parse('examples/inspect.drawio')
# print(etree.tostring(x, pretty_print=True))

diagram_data = x.findall('.//diagram')[0]#.text
#print(diagram_data)
diagram_data = ElementTree.tostring(diagram_data).decode('utf8')
print(diagram_data)



