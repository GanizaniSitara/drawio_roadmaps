
DRAWIO_EXECUTABLE_PATH = "C:\\Program Files\\draw.io\\draw.io.exe"

class RoadmapConfig:
    class Global:
        show_quarters = True

    class Text:
        pass

    class DrawIO:
        year_length_px = 240
        swimlane_height_px = 100
        pass

    class PowerPoint:
        pass

    class Ascii:
        segment_width = 36


class ColorSchemes:
    true_hex = {
        "Bakerloo": "#B36305",
        "Central": "#E32017",
        "Circle": "#FFD300",
        "District": "#00782A",
        "Hammersmith and City": "#F3A9BB",
        "Jubilee": "#A0A5A9",
        "Metropolitan": "#9B0056",
        "Northern": "#000000",
        "Piccadilly": "#003688",
        "Victoria": "#0098D4",
        "Waterloo and City": "#95CDBA",
        "DLR": "#00A4A7",
        "Overground": "#EE7C0E",
        "Tramlink": "#84B817",
        "Cable Car": "#E21836",
        "Crossrail": "#7156A5"
    }

    web_safe_hex = {
        "Bakerloo": "#996633",
        "Central": "#CC3333",
        "Circle": "#FFCC00",
        "District": "#006633",
        "Hammersmith and City": "#CC9999",
        "Jubilee": "#868F98",
        "Metropolitan": "#660066",
        "Northern": "#000000",
        "Piccadilly": "#000099",
        "Victoria": "#0099CC",
        "Waterloo and City": "#66CCCC",
        "DLR": "#009999",
        "Overground": "#FF6600",
        "Tramlink": "#66CC00",
        "Cable Car": None,
        "Crossrail": None
    }