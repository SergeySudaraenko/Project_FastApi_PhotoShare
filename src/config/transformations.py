class Standard:
    name = "standard"
    transformation = {"width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Radius:
    name = "radius"
    transformation = {"radius": "max", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Grayscale:
    name = "grayscale"
    transformation = {"effect": "grayscale", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Cartoonify:
    name = "cartoonify"
    transformation = {"effect": "cartoonify", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Vectorize:
    name = "vectorize"
    transformation = {"effect": "vectorize:colors:2:detail:0.05", "width": 500, "height": 500, "gravity": "faces",
                      "crop": "fill"}


class Transformation:
    name = {"grayscale": Grayscale.transformation, "cartoonify": Cartoonify.transformation,
            "radius": Radius.transformation, "standard": Standard.transformation, "vectorize": Vectorize.transformation}
