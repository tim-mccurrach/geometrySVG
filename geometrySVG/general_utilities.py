"""Convenience functions that are used throughout the package, put in a module
for tidyness"""

from math import atan2, floor, pi, sqrt


def XMLAttr(attribute, value):
    """returns attribues in the standard attribute="value" fashion used in HTML
    and SVG/XML. Underscores are converted to hyphens"""
    attribute = str(attribute).replace("_", "-")
    value = str(value).replace("_", "-")
    return attribute+'="'+value+'"'


def angle_of_line(p1, p2):
    """returns the angle of the line going from the first co-ordinate to the
    second. The angle is measured in radians from the positive x-axis.
    (Co-ordinates are given are top and left)."""
    # note y is reversed, since it is generally measured from the top
    return atan2(p1.y - p2.y, p2.x - p1.x)


def distance_points(p1, p2):
    """returns the Euclidean distance between two points"""
    return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


def point_on_line(p1, p2, distance):
    """Returns the coordinates of a point a fixed distance along a line,
    stating at the first set of coordinates given."""
    length = distance_points(p1, p2)
    r = distance / length   # The ratio along the line
    x = (1 - r) * p1.x + r * p2.x
    y = (1 - r) * p1.y + r * p2.y
    return [x, y]


def angle_between_lines(c, p1, p2, reflex):
    """Gives the angle -2pi to 2pi (clockwise/anticlockwise) going from one
    point to a central point, and then back to a third point. The first
    given point is the place you are strarting from. reflex is a bool, to say
    if the longer or shorter should be taken."""
    angle1 = angle_of_line(c, p1)
    angle2 = angle_of_line(c, p2)
    difference = angle2 - angle1
    if abs(difference) > pi:
        if reflex:
            return difference
        else:
            if difference > 0:
                return difference - 2*pi
            else:
                return 2*pi + difference
    else:
        if reflex:
            if difference > 0:
                return difference - 2*pi
            else:
                return 2*pi + difference
        else:
            return difference


def quadrant_of_angle(angle):
    """given an angle in radians between pi and -pi, return the number 1, 2, 3
    or 4 to indicate, which quadrant that angle is in"""
    return (floor((angle + pi)/(pi / 2)) - 2) % 4 + 1


def get_XML_arc_path(point1, point2, center, reflex=None, direction=None):
    """returns the value of d needed, to draw a circular arc from point1, to
    point2 centered on center. Either a direction ('CLOCKWISE'|'ANTICLOCKWISE')
    or reflex (boolean) must be given.
    XML syntax for arc to is:
    a rx, ry, rotation, large-arc-flag, sweep-flag(c or ac), endpoint(x,y)
    """
    if reflex is None and direction is None:
            raise TypeError("At least one of reflex or direction"
                            " must be given")
    radius = distance_points(point1, center)

    large_arc, sweep = get_reflex_direction(point1,
                                            point2,
                                            center,
                                            reflex=reflex,
                                            direction=direction)

    d = "M{} L{} A{},{} 0 {},{} {}".format(str(center),
                                           str(point1),
                                           str(radius),
                                           str(radius),
                                           str(large_arc),
                                           str(sweep),
                                           str(point2))
    return d


def get_reflex_direction(point1, point2, center, direction=None, reflex=None):
    """returns a tuple (0,0)|(0,1)|(1,0)|(1,1) to show if the angle is reflex
    or not (0=acute, 1=reflex) and the direction (1=clockwise,
    0=anti-clockwise)
    """
    if reflex is None and direction is None:
            raise TypeError("At least one of reflex or direction"
                            " must be given")
    radius = distance_points(point1, center)

    if direction is not None:
        angle = angle_between_lines(center, point1, point2, True)
        if direction == "CLOCKWISE":
            clock = 1
            if angle < 0:
                large_arc = 1
            else:
                large_arc = 0
        elif direction == "ANTICLOCKWISE":
            clock = 0
            if angle > 0:
                large_arc = 1
            else:
                large_arc = 0
        else:
            raise ValueError("direction must be CLOCKWISE "
                             "or ANTICLOCKWISE")
    else:
        angle = angle_between_lines(center, point1, point2, reflex)
        if angle == pi or angle == -pi:
            pass
            # Need to do something here
        else:
            if reflex:
                large_arc = 1
            else:
                large_arc = 0
            if angle > 0:
                clock = 0
            else:
                clock = 1

    return large_arc, clock

    def get_direction_of_polygon(*points):
        """determines the direction of a set of points, 'ABCD...' and returns
        1 or 0, depending on if 'ABC' or 'CBA' is an internal angle"""
        pass
