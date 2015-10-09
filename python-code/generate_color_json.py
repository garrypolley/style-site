#! /usr/bin/env python
import inspect
import json
import os

from operator import itemgetter

from admin_colors import admin_bg_color
from admin_colors import admin_text_color
from buyer_colors import buyer_bg_color
from buyer_colors import buyer_text_color
from old_supplier_colors import old_supplier_bg_color
from old_supplier_colors import old_supplier_text_color
from supplier_colors import supplier_bg_color
from supplier_colors import supplier_text_color

CURRENT_DIR = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe()
            )
        )
    ).split('/python-code')[0]


#### Code stolen from: https://github.com/TheDutchCoder/ColorConvert/blob/master/colorconvert.py ###

# Global color channel values.
_hr = None
_hg = None
_hb = None

_r = None
_g = None
_b = None

_h = None
_s = None
_l = None

_alpha = 1.0
_alpha_enabled = True


def hueToRgb(v1, v2, vH):
    """Assists with converting hsl to rgb values.
    Attributes:
        self: The Regionset object.
        v1:   The first part of the hsl collection
        v2:   The second part of the hsl collection
        vH:   The thrid part of the hsl collection
    """

    if vH < 0:
        vH += 1

    if vH > 1:
        vH -= 1

    if ((6 * vH) < 1):
        return (v1 + (v2 - v1) * 6 * vH)

    if ((2 * vH) < 1):
        return v2

    if ((3 * vH) < 2):
        return (v1 + (v2 - v1) * ((2 / 3) - vH) * 6)

    return v1


def hexToRgb(hr, hg, hb):
    """Converts a hex value to an rgb value.
    Attributes:
        self: The Regionset object.
        r:    The value of the red channel   (00 - ff)
        g:    The value of the green channel (00 - ff)
        b:    The value of the blue channel  (00 - ff)
    """

    global _r
    global _g
    global _b

    global _alpha

    r = (int(hr, 16))
    g = (int(hg, 16))
    b = (int(hb, 16))

    if _r is None:

        _r = r
        _g = g
        _b = b

    return {'r': r, 'g': g, 'b': b, '_alpha': _alpha}


def rgbToHex(r, g, b, a):
    """Converts an rgb(a) value to a hex value.
    Attributes:
        self: The Regionset object.
        r:    The value of the red channel   (0 - 255)
        g:    The value of the green channel (0 - 255)
        b:    The value of the blue channel  (0 - 255)
        a:    The value of the alpha channel (0.0 - 1.0)
    """

    global _alpha

    # Get the alpha channel and store it globally (if present).
    if a is not None:
        _alpha = a

    # Convert the channels' values to hex values.
    r = hex(r)[2:].zfill(2)
    g = hex(g)[2:].zfill(2)
    b = hex(b)[2:].zfill(2)

    # If a short notation is possible, splice the values.
    if (r[0:1] == r[1:2]) and (g[0:1] == g[1:2]) and (b[0:1] == b[1:2]):
        r = r[1:]
        g = g[1:]
        b = b[1:]

    return {'r': r, 'g': g, 'b': b}


def rgbToHsl(r, g, b, a=None):
    """Converts an rgb(a) value to an hsl(a) value.
    Attributes:
        self: The Regionset object.
        r:    The value of the red channel   (0 - 255)
        g:    The value of the green channel (0 - 255)
        b:    The value of the blue channel  (0 - 255)
        a:    The value of the alpha channel (0.0 - 1.0)
    """

    global _h
    global _s
    global _l

    global _alpha

    # Get the alpha channel and store it globally (if present).
    if a is not None:
        _alpha = a

    r = float(r) / 255.0
    g = float(g) / 255.0
    b = float(b) / 255.0

    # Calculate the hsl values.
    cmax = max(r, g, b)
    cmin = min(r, g, b)

    delta = cmax - cmin

    # Hue
    if (cmax == r) and (delta > 0):
        h = 60 * (((g - b) / delta) % 6.0)

    elif (cmax == g) and (delta > 0):
        h = 60 * (((b - r) / delta) + 2.0)

    elif (cmax == b) and (delta > 0):
        h = 60 * (((r - g) / delta) + 4.0)

    elif (delta == 0):
        h = 0

    # Lightness
    l = (cmax + cmin) / 2.0

    # Saturation
    if (delta == 0):
        s = 0

    else:
        s = (delta / (1 - abs((2 * l) - 1)))

    s = s * 100.0
    l = l * 100.0

    # Store the hsl values globally.
    if _h is None:

        _h = h
        _s = s
        _l = l

    return {'h': h, 's': s, 'l': l, '_alpha': _alpha}

#### END STOLEN CODE ####

def convert_to_hsl(color):
    if color.startswith('#'):
        color = color.replace('#', '')
        if len(color) == 3:
            rgbValue = hexToRgb(color[0], color[1], color[2])
        else:
            rgbValue = hexToRgb(color[:2], color[2:4], color[4:])

        return rgbToHsl(rgbValue['r'], rgbValue['g'], rgbValue['b'])

    elif color.startswith('r'):
        color_array = color.split('(')[1].replace(')', '').split(',')
        r = color_array[0]
        g = color_array[1]
        b = color_array[2]
        a = color_array[3] if len(color_array) == 4 else None

        return rgbToHsl(r, g, b, a)

    return {'h': 0, 's': 0, 'l': 0, '_alpha': 0}

def generate_data_dict(data, sort_func):
    sort_func = int if sort_func == None else sort_func
    data_array = [x for x in data.split('\n') if x != '']

    data_list = []

    i = 0;
    index = 0

    for value in data_array:
        if i % 2 == 0:
            background_color, color_value = value.split(': ')
            color_value = color_value.replace(';', '')
            hsl_value = convert_to_hsl(color_value.split(' ')[0])
            data_list.append({'color': color_value, 'h': hsl_value['h'], 's': hsl_value['s'], 'l': hsl_value['l']})
        else:
            data_list[index]['count'] = value
            index += 1
        i+=1

    return sorted(data_list, key=sort_func, reverse=True)

def sort_by_count(data):
    return int(data['count'])


sort_by_color = itemgetter('h', 's', 'l')

def write_to_file(data, name):
    with open('{cur_dir}/assets/js/{name}.data.js'.format(cur_dir=CURRENT_DIR, name=name), 'w+') as f:
        json_string = json.dumps(data, indent=2)

        formatted_name = name.split('_')
        formatted_name = formatted_name[0] + "".join(map(str.capitalize, formatted_name[1:]))

        f.write('var {var_name} = {json_data};'.format(var_name=formatted_name, json_data=json_string))


write_to_file(generate_data_dict(admin_bg_color, sort_by_count), 'admin_bg_color')
write_to_file(generate_data_dict(admin_text_color, sort_by_count), 'admin_text_color')
write_to_file(generate_data_dict(buyer_bg_color, sort_by_count), 'buyer_bg_color')
write_to_file(generate_data_dict(buyer_text_color, sort_by_count), 'buyer_text_color')
write_to_file(generate_data_dict(old_supplier_bg_color, sort_by_count), 'old_supplier_bg_color')
write_to_file(generate_data_dict(old_supplier_text_color, sort_by_count), 'old_supplier_text_color')
write_to_file(generate_data_dict(supplier_bg_color, sort_by_count), 'supplier_bg_color')
write_to_file(generate_data_dict(supplier_text_color, sort_by_count), 'supplier_text_color')

write_to_file(generate_data_dict(admin_bg_color, sort_by_color), 'admin_color_sorted_bg_color')
write_to_file(generate_data_dict(admin_text_color, sort_by_color), 'admin_color_sorted_text_color')
write_to_file(generate_data_dict(buyer_bg_color, sort_by_color), 'buyer_color_sorted_bg_color')
write_to_file(generate_data_dict(buyer_text_color, sort_by_color), 'buyer_color_sorted_text_color')
write_to_file(generate_data_dict(old_supplier_bg_color, sort_by_color), 'old_supplier_color_sorted_bg_color')
write_to_file(generate_data_dict(old_supplier_text_color, sort_by_color), 'old_supplier_color_sorted_text_color')
write_to_file(generate_data_dict(supplier_bg_color, sort_by_color), 'supplier_color_sorted_bg_color')
write_to_file(generate_data_dict(supplier_text_color, sort_by_color), 'supplier_color_sorted_text_color')
