from geometrySVG import SVGCanvas

canvas = SVGCanvas(300, 300, cart_coords=True)

canvas.add_point(30, 40, "A")
canvas.add_point(160, 60, "B")
canvas.add_point(180, 190, "C")

canvas.add_polygon("ABC", name="triangle", fill="none", stroke="black")

canvas.triangle.add_angles(fill="blue",
                           text=["a-9\u00b0", "5a\u00b0", "a\u00b0"],  # \u00b0 is degrees
                           font_family="Times Roman")

a = canvas.generate_SVG(500, 500, style_info=True)

with open("output.svg", "wb") as file:
    file.write(a.encode('utf8'))  # utf8 encoding necessary due to degrees symbol
