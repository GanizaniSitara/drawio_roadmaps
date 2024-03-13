
DRAWIO_EXECUTABLE_PATH = "C:\\Program Files\\draw.io\\draw.io.exe"

class RoadmapConfig:
    # Todo Move this to the roadmap definition/data
    # maybe make it optional or in some roadmap config when loading from DB
    class Global:
        show_quarters = True

    class Text:
        pass

    class DrawIO:
        pass

    class PowerPoint:
        pass

    class Ascii:
        segment_width = 36