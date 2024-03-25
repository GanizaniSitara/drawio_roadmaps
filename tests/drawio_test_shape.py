
import os

import drawio_roadmaps.drawio.drawio_utils as drawio_utils
import drawio_roadmaps.drawio.drawio_shapes as drawio_shapes
from drawio_roadmaps.config import DRAWIO_EXECUTABLE_PATH


mxGraphModel = drawio_utils.get_diagram_root()
root = mxGraphModel.find("root")

layers = {
            'default': drawio_utils.create_layer('Default', locked=0),
         }

for layer in layers.values():
    root.append(layer)

test_shape = drawio_shapes.create_angled_line(layers['default'].get('id'), 0, 0, 300, 100, 100, 100,
style='endArrow=none;html=1;strokeColor=#FF0080;strokeWidth=8;fontFamily=Expert Sans Reguler;flowAnimation=0')
root.append(test_shape)

drawio_utils.pretty_print_to_console(mxGraphModel)
drawio_utils.encode_and_save_to_file(mxGraphModel, filename='test_shape.drawio')
os.system(f'"{DRAWIO_EXECUTABLE_PATH}" test_shape.drawio')

