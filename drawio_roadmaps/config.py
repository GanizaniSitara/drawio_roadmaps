from drawio_roadmaps.config_colors import ColorScheme, DefaultColorScheme, LondonUndergroundColorScheme

DRAWIO_EXECUTABLE_PATH = "C:\\Program Files\\draw.io\\draw.io.exe"

class RoadmapConfig:
    class Global:
        show_quarters = True

    class DrawIO:
        year_length_px = 240
        swimlane_height_px = 100
        color_scheme = ColorScheme(LondonUndergroundColorScheme)
        pass

    class Ascii:
        segment_width = 36

    class PowerPoint:
        pass

    class Text:
        pass

