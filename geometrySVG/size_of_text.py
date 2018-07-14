"""When adding angles to a shape, it is important to know the size that the text
will be in order that it can be best positioned. This is the primary purpose of this module"""

import os.path

from .afm import AFM
from .rect_in_lines import rect_in_lines
from .general_utilities import get_reflex_direction

afm_fname = os.path.join(os.path.dirname(__file__), 'fonts', 'ptmr8a.afm')
with open(afm_fname, 'rb') as fh:
    afm = AFM(fh)


def size_of_text(text, text_kwargs):
    """Calculates the size of the text given in pixels. Returns both height and
    width, and also the offset of the lowest point in the string from the
    baseline, and the offset of the left-most point in the string from the
    starting position of the text."""
    if text_kwargs is None:
        text_kwargs = {}
    if "font_size" not in text_kwargs:
        text_kwargs["font_size"] = 20
    font_size = text_kwargs["font_size"]
    bbox = afm.get_str_bbox(text)
    width = (bbox[2]-bbox[0])*font_size/1000
    height = (bbox[3]-bbox[1])*font_size/1000
    dx = bbox[0]*font_size/1000
    dy = bbox[1]*font_size/1000
    return (width, height, dx, dy)


def position_radius_of_text(point1, center, point2, width, height, dx, dy,
                            reflex, direction, margin):
    """given the height and width of a rectangle and two lines, this function
    returns the position of the bottom-left most point of the rectangle, and
    the radius of a circle needed to completely inclose the rectangle in the
    lines."""
    reflex = get_reflex_direction(point1, point2, center, reflex=reflex,
                                  direction=direction)[0]
    (x, y), r = rect_in_lines(center, point1, point2, reflex, width, height, 1)
    x -= (dx - margin)
    y += (dy - margin)
    return x, y, r
