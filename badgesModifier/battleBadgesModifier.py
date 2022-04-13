# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html
from PIL import Image, ImageDraw
import xmltodict
from shutil import copyfile


colors = {
    "badge_10": (241, 0, 0, 255),  # "red"
    "badge_11": (0, 193, 0, 255),  # "green"
    "badge_12": (102, 170, 255, 255),  # "blue"
    "badge_13": (204, 68, 255, 255),  # "purple"
    "badge_14": (255, 215, 0, 255),  # "golden"
}

SRC_XML = "src/gui/flash/atlases/battleAtlas.xml"
SRC_IMAGE = "src/gui/flash/atlases/battleAtlas.dds"
TARGET_XML = "target/gui/flash/atlases/battleAtlas.xml"
TARGET_IMAGE = "target/gui/flash/atlases/battleAtlas.png"


def main():
    atlas = xmltodict.parse(open(SRC_XML, "r", encoding="utf-8").read())

    coordinates = dict()
    for subTexture in atlas["root"]["SubTexture"]:
        if subTexture["name"] in colors.keys():
            coordinates[subTexture["name"]] = (
                int(subTexture["x"]),
                int(subTexture["y"]),
                int(subTexture["width"]),
                int(subTexture["height"]),
            )

    assert len(coordinates) == len(colors)

    image = Image.open(SRC_IMAGE)
    draw = ImageDraw.Draw(image)
    for badgeName, metrics in coordinates.items():
        rectangle = [metrics[0], metrics[1], metrics[0] + metrics[2], metrics[1] + metrics[3]]
        draw.rectangle(rectangle, fill=(0, 0, 0, 0))  # clear rect

        dx = metrics[2] / 4
        dy = metrics[3] / 4

        rectangle[0] += dx
        rectangle[2] -= dx
        rectangle[1] += dy
        rectangle[3] -= dy
        fillColor = colors[badgeName]
        halvedAlphaColor = fillColor[:3] + (128,)
        draw.ellipse(rectangle, fill=fillColor, outline=halvedAlphaColor)

    image.save(TARGET_IMAGE)
    copyfile(SRC_XML, TARGET_XML)


if __name__ == "__main__":
    main()
