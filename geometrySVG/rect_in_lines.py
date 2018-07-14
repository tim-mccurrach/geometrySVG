"""The main purpose of this module is the function rect_in_lines: Given 3
points, forming two lines coming out from a single point, this function
fits a rectangle as close to the center of these points as possible.

This function is very very messy, and needs refactoring. A better way to do
this would be as follows:
1) Assume the two lines lie in the range pi<theta<-pi/2
2) Write a shorter function to solve the problem given the above constraints
3) Write a pair of 1-1 functions mapping lines lying in altenative quadrants to
   lines fitting the constaints in (1) and mapping solutions from 1 back to
   the associated position in other quadrants."""

from math import atan2, cos, floor, pi, sin, sqrt

from .general_utilities import (
    angle_of_line,
    angle_between_lines,
    quadrant_of_angle)


def find_min_point_on_line(angle_of_line, corner, dimensions):
    """Given a line, returns where to position a corner of a rectangle
    on that line, to minimise the radius.

    angle_of_line given in radians between pi and -pi.
    corner will be one of (0,0), (0,1), (1,1), (1,0).
    side_of_line is 1 or -1, for right or left respectively.

    THIS FUNCTION TAKES UPWARDS AS POSITIVE
    """

    # Calculate how far along the line to slide the rectangle
    w, h = dimensions
    A, B = {(0, 0): (1, 1), (1, 0): (-1, 1),
            (0, 1): (1, -1), (1, 1): (-1, -1)}[corner]
    line_direction_x = 1 if cos(angle_of_line) >= 0 else -1
    line_direction_y = 1 if sin(angle_of_line) >= 0 else -1
    C = A if A == line_direction_x else 0
    D = B if B == line_direction_y else 0
    x_coeff = A*w*cos(angle_of_line)+B*h*sin(angle_of_line)
    if x_coeff >= 0:
        x = 0
    else:
        min1 = -1*(h**2 + w**2)**0.5*x_coeff
        den = w*(C-A)*cos(angle_of_line)+h*(D-B)*sin(angle_of_line)
        if den == 0:
            min2 = 0
        else:
            min2 = 0.5*((A*w)**2+(B*h)**2-(C*w)**2-(D*h)**2)/den
        x = min(min1, min2)

    # return the coordinates for poinr on the line
    x_coord = x * cos(angle_of_line)
    y_coord = x * sin(angle_of_line)
    return (x_coord, y_coord)


def max_radius(bottom_left_corner, dimensions):
    """given the bottom left corner and width and height, returns the
    min radius needed to completely enclose the rectangle."""
    b_x, b_y = bottom_left_corner[0], bottom_left_corner[1]
    w, h = dimensions[0], dimensions[1]
    lengths = [((b_x+a*w)**2+(b_y-b*h)**2)**0.5 for
               (a, b) in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    return max(lengths)


def improve_fit(coord, line_1, line_2, pos, dimensions):
    """In some situations a rectangle would be placed at (0,0) but the
    radius needed to enclose the rectangle can still be reduced by
    sliding the rectangle along a line. This function checks if this is the
    case and returns an improved fit if possible."""
    w, h = dimensions[0], dimensions[1]
    adjust_dict = {(0, 0): (0, 0), (1, 0): (-w, 0),
                   (1, 1): (-w, h), (0, 1): (0, h)}
    radius = max_radius(coord, dimensions)
    if pos % 2 == 0:
        corner_dict = {2: (0, 0), 4: (1, 0), 6: (1, 1), 8: (0, 1)}
        corner = [corner_dict[pos], corner_dict[pos]]
        adjust = [adjust_dict[corner[0]], adjust_dict[corner[1]]]
        for index, line in enumerate([line_1, line_2]):
            new_coord = find_min_point_on_line(line, corner[index], dimensions)
            new_coord = (new_coord[0]+adjust[index][0],
                         -new_coord[1]+adjust[index][1])
            new_radius = max_radius(new_coord, dimensions)
            if new_radius < radius:
                coord = new_coord
                radius = new_radius
    return coord, radius


def rect_in_lines(center, c1, c2, reflex, width, height, margin):
    """Given a rectangle of given width and height, return the co-ordinates of
    its bottom left corner, such that it fits in between two given lines. The
    primary use of this function is positioning text to label angles. reflex
    is a bool, center is the point of intersection of the two lines, and c1
    and c2 are two points on the lines."""

    # NEEDS REFACTORING - SEE NOTE IN MODULE DOC_STRING
    line1 = angle_of_line(center, c1)
    line2 = angle_of_line(center, c2)
    angle = angle_between_lines(center, c1, c2, reflex)

    if line2 < line1:
        line1, line2 = line2, line1
        angle *= -1

    # calculate the two quadrants that the angles are in
    q1 = quadrant_of_angle(line1)
    q2 = quadrant_of_angle(line2)
    d = (q1-q2) % 4

    # rx and ry, are relative coordinates from an origin.
    pos = 0  # pos represents positions 1 to 8 starting from the +ve axis
    fp = 0  # fp is the furthest point from the center.

    if reflex:
        if d == 1 or d == 3:  # adjacent quadrants, also considering edge cases
            if line1 >= 0:
                if line2 == pi/2:
                    if height > width:
                        pos = 5
                    else:
                        pos = 7
                elif line2 == pi:
                    if height > width:
                        pos = 1
                    else:
                        pos = 7
                else:
                    pos = 7
            elif line1 >= -pi/2:
                if line2 == 0:
                    if height > width:
                        pos = 5
                    else:
                        pos = 3
                elif round(line2, 8) == round(pi, 8):
                    pos = 3
                else:
                    pos = 5
            elif line1 < - pi/2:
                if line2 == -pi/2:
                    if height > width:
                        pos = 1
                    else:
                        pos = 3
                elif line2 == pi/2:
                    if height > width:
                        pos = 1
                    else:
                        pos = 7
                elif line2 > pi/2:
                    pos = 1
                else:
                    pos = 3

        elif d == 2:  # Opposite quadrants
            if q1 == 3:
                if angle > 0:
                    pos = 8
                else:
                    if line2 == 0:
                        pos = 3
                    else:
                        pos = 4
            elif q1 == 4:
                if angle > 0:
                    if line1 == -pi/2:
                        pos = 1
                    else:
                        pos = 2
                else:
                    if line2 == pi/2:
                        pos = 5
                    else:
                        pos = 6
            elif q1 == 1:  # q2 must be pi
                pos = 7

        elif d == 0:  # The same quadrant
            if width >= height:
                if q1 == 1:
                    pos = 7
                elif q1 == 2:
                    pos = 7
                elif q1 == 3:
                    pos = 3
                elif q1 == 4:
                    pos = 3
            else:
                if q1 == 1:
                    pos = 5
                elif q1 == 2:
                    pos = 1
                elif q1 == 3:
                    pos = 1
                elif q1 == 4:
                    pos = 5
    else:  # Non reflex-angles
        if d == 2:  # opposite quadrants
            if q1 == 1:
                if angle < 0:
                    pos = 8
                else:
                    pos = 4
            elif q1 == 2:
                if angle < 0:
                    pos = 2
                else:
                    pos = 6
            elif q1 == 3:
                if angle < 0:
                    pos = 4
                else:
                    pos = 8
            elif q1 == 4:
                if angle < 0:
                    pos = 6
                else:
                    pos = 2
        elif d == 1 or d == 3:  # adjacent quadrants
            # Fit a horizontal or vertical edge between two lines
            l_angle = max(line1, line2)
            s_angle = min(line1, line2)
            if {q1, q2}.issubset({1, 4}) or {q1, q2}.issubset({2, 3}):
                if l_angle == pi:
                    diag_angle = atan2(height, width)
                    diag_lenth = sqrt(height**2 + width**2)
                    dist = abs(sin(s_angle-diag_angle)*diag_lenth/sin(angle))
                    rx = dist*cos(l_angle)
                    ry = -dist*sin(l_angle)
                else:
                    dist = abs(height*sin(pi/2-l_angle)/sin(angle))
                    ry = -dist*sin(s_angle)
                    rx = dist*cos(s_angle)
                    if s_angle < -pi/2:
                        rx -= width
            else:
                if l_angle == pi:
                        pos = 6
                elif s_angle < 0:
                    dist = abs(width*sin(l_angle)/sin(angle))
                    ry = -dist*sin(s_angle) + height
                    rx = dist*cos(s_angle)
                else:
                    dist = abs(width*sin(s_angle)/sin(angle))
                    ry = -dist*sin(l_angle)
                    rx = dist*cos(l_angle)
        elif d == 0:  # same quadrants
            # Fit diagnonal line between the two lines
            diag_lenth = sqrt(height**2+width**2)
            diag_angle = atan2(height, width)
            l_angle = max(line1, line2)
            s_angle = min(line1, line2)
            if q1 == 1:
                dist = abs(sin(s_angle+diag_angle)*diag_lenth/sin(angle))
                rx = dist*cos(l_angle)
                ry = -dist*sin(l_angle)+height
            elif q1 == 2:
                dist = abs(sin(s_angle-diag_angle)*diag_lenth/sin(angle))
                rx = dist*cos(l_angle)
                ry = -dist*sin(l_angle)
            elif q1 == 3:
                if l_angle == pi:
                    l_angle = -pi
                    l_angle, s_angle = s_angle, l_angle
                dist = abs(sin(pi+s_angle+diag_angle)*diag_lenth/sin(angle))
                rx = dist*cos(l_angle)-width
                ry = -dist*sin(l_angle)
            elif q1 == 4:
                dist = abs(sin(-l_angle+diag_angle)*diag_lenth/sin(angle))
                rx = dist*cos(s_angle)
                ry = -dist*sin(s_angle)

    # assign pos for simple cases
    if pos != 0:
        if pos == 1:
            rx = margin
            ry = height / 2
        elif pos == 2:
            rx = margin
            ry = -margin
        elif pos == 3:
            rx = -width / 2
            ry = -margin
        elif pos == 4:
            rx = -width-margin
            ry = -margin
        elif pos == 5:
            rx = -width-margin
            ry = height / 2
        elif pos == 6:
            rx = -width-margin
            ry = height+margin
        elif pos == 7:
            rx = -width / 2
            ry = height+margin
        elif pos == 8:
            rx = margin
            ry = height+margin
        (rx, ry), radius = improve_fit((rx, ry), line1, line2,
                                       pos, (width, height))
    radius = max_radius((rx, ry), (width, height))
    return (center.x + rx, center.y + ry), radius
