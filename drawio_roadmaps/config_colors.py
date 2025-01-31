
class ColorScheme:
    def __init__(self, scheme_class):
        self.scheme_class = scheme_class

    def __getattr__(self, attr):
        try:
            value = getattr(self.scheme_class, attr)
            if isinstance(value, type):
                return ColorScheme(value)
            return value
        except AttributeError:
            raise AttributeError(f"Color category '{attr}' not found in the selected color scheme.")

class DefaultColorScheme():
    def __init__(self):
        super().__init__("Default")

    class RAG:
        Red = "#FF6961"
        Amber = "#FFBF00"
        Green = "#50C878"

    class Colors:
        Grey = "#858585"
        Blue = "#A9C5E6"
        Purple = "#B19CD9"
        Yellow = "#FFD700"



class LondonUndergroundColorScheme():

    class RAG:
        Red = "#E32017"  # Red, Central line
        Amber = "#EE7C0E"  # Orange, Overground line
        Green = "#00782A"  # Green, District line

    class Colors:
        Brown = "#B36305"  # Brown, Bakerloo
        Yellow = "#FFD300"  # Yellow, Circle
        Pink = "#F3A9BB"  # Pink, Hammersmith and City
        Grey = "#A0A5A9"  # Silver, Jubilee
        Magenta = "#9B0056"  # Magenta, Metropolitan
        Black = "#000000"  # Black, Northern
        Blue_Dark = "#003688"  # Dark Blue, Piccadilly
        Blue = "#0098D4"  # Light Blue, Victoria
        Turquoise = "#95CDBA"  # Turquoise, Waterloo and City
        Turquoise_2 = "#00A4A7"  # Turquoise, DLR
        Green_Lime = "#84B817"  # Lime Green, Trams
        Purple = "#7156A5"  # Purple, Elizabeth Line
        Red_2 = "#E21836"  # Red, Cable Car
