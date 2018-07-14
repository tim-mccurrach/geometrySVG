"""This module contains the main class SVGCanvas, as well as a few other key
classes"""

from math import pi

from .general_utilities import (get_XML_arc_path,
                                get_reflex_direction,
                                point_on_line,
                                XMLAttr
                                )
from .size_of_text import size_of_text, position_radius_of_text


class Point():
    """For use in SVGCanvas. Defines the 'references' that other elements
    will use in their own definitions.
    """

    def __init__(self, x, y, name="", label=""):
        self.x = x
        self.y = y
        self.name = name

    def __call__(self):
        return self.x, self.y

    def __str__(self):
        return str(self.x)+","+str(self.y)


class SVGComponent():
    """Each line, point, text, element in the final SVG will be an SVGComponent
    instance."""

    def __init__(self, label, content=None, defaults=None, **kwargs):
        self.label = label
        self.content = content
        if defaults is None:
            self.attributes = kwargs
        else:
            self.attributes = {**defaults, **kwargs}

    def returnSVG(self):
        """returns the SVG-XML needed for the final SVG produced"""
        result = "<"+self.label + " "
        result += " ".join([XMLAttr(key, val) for key, val in
                            self.attributes.items()])
        if self.content is None:
            result += " />"
        else:
            result += ">"+str(self.content)+"</"+self.label+">"
        return result


class SVGPolygon():
    """A polygon can consist of several SVG elements, an outline and fill, as
    well as angles, and these must all be written in the correct order. This
    class acts in a similar way to the SVGComponent class, but the returnSVG
    method, ensures the order is correct."""

    def __init__(self, canvas, *points, **kwargs):
        # An SVGPolygon instance must have its own copy of all of the points
        self.canvas = SVGCanvas(canvas.width,
                                canvas.height,
                                canvas.x_min,
                                canvas.y_min,
                                canvas.cart_coords)
        self.canvas.points = canvas.points
        self.points = canvas._get_points(*points)
        self.fkwargs = {**kwargs}
        self.fkwargs['stroke_width'] = 1
        self.ekwargs = {**kwargs}
        self.ekwargs['stroke_width'] = 1
        self.canvas.add_closed_path(self.points, **self.fkwargs)

    def returnSVG(self):
        """outputs first the filled in part of the polygon. Then adds in the
        angles, then finally the border."""
        self.canvas.add_closed_path(self.points, **self.ekwargs)
        return "".join(x.returnSVG() for x in self.canvas.components)

    def add_angle(self, point, internal=True, **kwargs):
        point_index = [p.name for p in self.points].index(point)
        n = len(self.points)
        points = [self.points[(point_index-1) % n],
                  self.points[point_index],
                  self.points[(point_index+1) % n]]
        self.canvas.add_angle(points, reflex=False, **kwargs)

    def add_angles(self, text=None, **kwargs):
        if text is None:
            for point in self.points:
                self.add_angle(point.name, **kwargs)
        else:
            for i, point in enumerate(self.points):
                self.add_angle(point.name, text=text[i], **kwargs)


class SVGCanvas():
    """Defines methods for creating standard school Geometry SVG diagrams, and
    a method, produceSVG() for outputing the SVG"""

    def __init__(self, width, height, x_min=0, y_min=0, cart_coords=True):
        """width and height, are for the viewport, not the final element"""
        self.x_min = x_min
        self.y_min = y_min
        self.width = width
        self.height = height
        self.cart_coords = cart_coords  # Use standard cartesian grid system
        self.points = {}
        self.components = []
        self.named_components = {}

    def __getattr__(self, name):
        if name in self.named_components:
            return self.components[self.named_components[name]]
        else:
            raise ValueError("There is no attribute or component "
                             "named {}".format(item))

    def generate_SVG(self, width, height, style_info=False, **kwargs):
        """Returns the complete SVG needed for all components
        added to the class instance. kwargs contains any other attributes
        to be added to the <svg> tag."""
        result=""
        if style_info:
            result += (r'<?xml version="1.0" standalone="no"?>'
                       '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
                       '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
        result += '<svg width="{}" height="{}" viewBox="{}" {}>{}</svg>'
        viewBox = " ".join(str(x) for x in [self.x_min,
                                            self.y_min,
                                            self.width,
                                            self.height])
        # Add in optional arguments
        defaults = {"preserveAspectRatio": "none"}

        kwargs = {**defaults, **kwargs}
        if style_info:
            kwargs['xmlns'] = "http://www.w3.org/2000/svg"
            kwargs['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
        additional_attributes = " ".join(XMLAttr(a, v) for a, v
                                         in kwargs.items())


        # Generate SVG XML for components
        components = "".join(comp.returnSVG() for comp in self.components)

        # Return completed SVG
        return result.format(width, height, viewBox,
                             additional_attributes, components)

    def add_point(self, x, y, name, label=""):
        """This does NOT add a visible point. It creates a Point class, that
        can be referenced when creating components. To create any visible
        component, a point must be referenced by name."""
        if self.cart_coords:
            y = self.height + self.y_min - y
        self.points[name] = Point(x, y, name, label)

    def _get_points(self, *points, min=0):
        """This allows you to pass a Point instance, or a string such as "A",
        or "ABC" represnting points, and it will return the relevant Points
        instances.
        """
        result = []
        for item in points:
            if isinstance(item, Point):
                result.append(item)
            else:
                for point in item:
                    if isinstance(point, Point):
                        result.append(point)
                    else:
                        result.append(self.points[point])
        if min > 0:
            if len(points) < 2:
                raise ValueError("*points must have at least "
                                 "{} points".format(min))
        return result

    def add_line(self, *points, **kwargs):
        """creates a 'line' component."""
        if len([*points]) != 2:
            raise ValueError("Only 2 points should be given")
        point1, point2 = self._get_points(*points)
        self.components.append(SVGComponent("line",
                                            x1=point1.x,
                                            y1=point1.y,
                                            x2=point2.x,
                                            y2=point2.y,
                                            **kwargs))

    def add_lines(self, *points, **kwargs):
        """creates a string of lines, joined end to end."""
        points = self._get_points(*points)
        for i in range(len(points)-1):
            self.add_line(points[i], points[i+1], **kwargs)

    def add_closed_path(self, *points, **kwargs):
        """adds a closed polygon"""
        points = self._get_points(*points)
        d = "M"+" ".join(str(p) for p in points)+"z"
        self.components.append(SVGComponent("path", d=d, **kwargs))

    def add_text(self, text, *point, **kwargs):
        """The bottom-left hand of the text is position at point, which can
        either be a point such as "A" or a pair of numbers x,y.
        """
        if len(point) == 1:
            x, y = self._get_points(*point)[0]()
        elif len(point) == 2:
            x, y = point
        else:
            raise TypeError("*point must either be a single point, or a pair"
                            "of numbers x, y")
        self.components.append(SVGComponent("text", x=x, y=y, content=text,
                                            **kwargs))

    def add_sector(self, point1, point2, point3,
                   reflex=None, direction=None, **kwargs):
        """Either a direction ('CLOCKWISE'|'ANTICLOCKWISE') or reflex
        (boolean) must be given.
        XML syntax for arc to is:
        a rx, ry, rotation, large-arc-flag, sweep-flag(c or ac), endpoint(x,y)
        """
        point1, center, point2 = self._get_points(point1, point2, point3)

        d = "M{} L{}".format(str(point1), str(center))
        d += get_XML_arc_path(point1, point2, center, reflex, direction)
        d += "z"

        self.components.append(SVGComponent("path", d=d, **kwargs))

    def add_angle(self, *points, radius=None, text=None, auto=True,
                  text_kwargs=None, reflex=None, direction=None,
                  margin=1, **kwargs):
        if text_kwargs is None:
            text_kwargs = {}
        # Figure out the relevant details
        point1, center, point2 = self._get_points(*points)
        if text is None:
            if auto:
                radius = 40  # NEED TO FIX THIS!!!!
        else:
            width, height, dx, dy = size_of_text(text, text_kwargs)
            # add in margin
            width += margin
            height += margin

            x, y, r = position_radius_of_text(point1, center, point2,
                                              width=width, height=height,
                                              dx=dx, dy=dy, reflex=reflex,
                                              direction=direction,
                                              margin=margin)
            if auto:
                radius = r
        point_1, point_2 = (Point(*point_on_line(center, x, radius))
                            for x in [point1, point2])
        self.add_sector(point_1, center, point_2, reflex=reflex,
                        direction=direction, **kwargs)
        if text is not None:
            self.add_text(text, x, y, **text_kwargs)

    def add_polygon(self, *points, name=None, **kwargs):
        self.components.append(SVGPolygon(self, *points, **kwargs))
        if name is not None:
            # store a number to indicate the component index associated with
            # the name
            self.named_components[name] = len(self.components)-1
