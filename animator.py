import pygame
import xml.etree.ElementTree as ET
import os
from kanji_colorize.kanjicolorizer.colorizer import KanjiColorizer
import math
import svg.path


STROKE_WIDTH = 4
STROKE_SPEED = 2
FRAME_RATE = 20

WIDTH = 327
HEIGHT = 327


# Function to parse the SVG file and extract path data
def parse_svg_file(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    path_data = []
    for path in paths:
        path_data.append(path.attrib["d"])
    return path_data


def hex_to_rgb(hex_code):
    # Remove the leading '#' if present
    if hex_code.startswith("#"):
        hex_code = hex_code[1:]

    # Convert the hex code to RGB
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)

    return (red, green, blue)


def complex_to_tuple(complex):
    return (complex.real, complex.imag)


def animate_stroke(path_data, canvas, color):
    path = svg.path.parse_path(path_data)
    length = path.length()
    duration = math.sqrt(length) / STROKE_SPEED
    num_frames = int(math.ceil(duration * FRAME_RATE))
    previous_point = complex_to_tuple(path.point(0))

    for frame in range(1, num_frames + 1):
        next_point = complex_to_tuple(path.point(frame / num_frames))
        # Draw a line from the prev_point to current point
        pygame.draw.line(canvas, color, previous_point, next_point, width=STROKE_WIDTH)
        previous_point = next_point
        # flip() the display to put your work on screen
        pygame.display.flip()


def animate_kanji(svg, canvas):
    assert svg.endswith(".svg")

    doc = ET.parse(svg)
    for path in doc.iterfind(".//{http://www.w3.org/2000/svg}path"):
        # Extract the stroke color from the path element, e.g style="stroke: #bf0909;"
        style = path.get("style")
        color = hex_to_rgb(style[style.find("#") : -1])
        animate_stroke(path.get("d"), canvas, color)
    return canvas


if __name__ == "__main__":
    pygame.init()

    canvas = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    # Create the kanjivgfile
    kanji = "無"
    output_dir = os.path.join("output", "colorized_kanji")
    args = " ".join(["--characters", kanji, "--output", output_dir])
    kc = KanjiColorizer(args)
    kc.write_all()
    svg_file = str(
        os.path.join(output_dir, f"{kanji}.svg")
    )  # Replace with your SVG file path

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Do logical updates here.
        # ...

        canvas.fill("white")  # Fill the display with a solid color

        # Render the graphics here.
        # ...
        animate_kanji(svg_file, canvas)

        canvas = pygame.display.set_mode((WIDTH, HEIGHT))
        clock.tick(60)  # wait until next frame (at 60 FPS)
