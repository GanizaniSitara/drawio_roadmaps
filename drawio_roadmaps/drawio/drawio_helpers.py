import random
import string


def id_generator(size=22, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '-_'):
    return ''.join(random.choice(chars) for _ in range(size))


def layer_id(root, name):
    for node in root.findall('.//mxCell[@parent="0"]'):
        if node.get('value') == name:
            return node.get('id')
    raise RuntimeError('Layer ' + name + ' not found')
