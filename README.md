A python package for generating SVG files for use in school geometry problems. 
## Introduction
This package was born out of a need to algorithmically create diagrams involving lines and polygons, with angles labeled on the diagrams. If not placed carefully text overlaps with lines which at best looks untidy and at worst un-readable. Even if text is not overlapping with lines, if it is not placed as close as possible to the point of the angle, the arc around the text can become very large. This package initially aims to adress this problem, and other typical school geometry features as it expands.
## Quick start
After the package has been imported an instance of the SVGCanvas object must be created. 

    from geometrySVG import SVGCanvas
    # Create canvas object specifying height and width
    canvas = SVGCanvas(300,300,cart_coords=True)

An optional argument `cart_coords`is provided since by default SVG measures coordinates (x,y) from the top-left in a similar fashion to HTML. `cart_coords=True` means that coordinates (x,y) are measured from the bottom-left as is normal when dealing with cartestian coordinates. 

After defining a canvas we must now add points to the canvas. Points are not visible SVG elements, but references used to create SVG elements. 

    canvas.add_point(30, 40, "A")
    canvas.add_point(160, 60, "B")
    canvas.add_point(180, 190, "C")

Each point must be given a name, which will be a single character. Now that we have added some points we can use a variety of methods to create shapes on the diagram.

    canvas.add_polygon("ABC")

Finally, when we have drawn our diagram, we can output the SVG for the whole canvas as a string, to use however you please.

    # generate SVG 
    result=canvas.generate_SVG(200, 200)
    # do something with it
    print(result)

**Important note:** This package was originally intended to create inline SVG in an HTML file, and does not include all of the style information. If you would like to write directly to an SVG file, use `style_info=True` e.g

    result=canvas.generate_SVG(200, 200, style_info=True)
    with open("output3svg", "w") as file:
        file.write(result)

## Key Methods
The following methods are provided to add lines and shapes to the canvas:

* `SVGCanvas.add_line(*points, **kwargs)` Adds a single line to the canvas. There must be exactly 2 points given, otherwise an error is raised.
* `SVGCanvas.add_lines(*points, **kwargs)` Adds a series of lines that are joined end to end. E.g `add_lines("ABC")` is equivalent to `add_line("AB")` and `add_line("BC")`

* `SVGCanvas.add_polyon(*points, name=None, **kwargs)` This adds a closed polygon from the points. At least 3 points must be given to define a polygon otherwise an error is raised. The name attribute is provided in order to later access the polygon. It can be accessed as a property, to access the polygon methods. e.g.:

    canvas.add_polygon("ABCDE", name="pentagon")
    canvas.pentagon.add_angles()


**Points**
In all methods points can either be provided as a single string, or separated into individual points. For example
`canvas.add_lines("ABC")` is equivalent to `canvas.add_lines("A","B","C")`

**Adding SVG attributes**
All methods have an optional `**kwargs` which can be used for adding SVG attributes to the elements. For example:
`canvas.add_polygon("ABC", fill="red")`
Many SVG attributes include hyphens. To use these, simply replace the hyphen with an underscore and it will be converted to a hyphen. For example to set `stroke-width` simply do:
`canvas.add_line("AB", stoke_width=4)` 
