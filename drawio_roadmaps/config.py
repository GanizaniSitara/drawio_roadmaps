import configparser
import os
import platform
import shutil
from pathlib import Path

from drawio_roadmaps.config_colors import ColorScheme, DefaultColorScheme, LondonUndergroundColorScheme

# Color scheme mapping
COLOR_SCHEMES = {
    'default': DefaultColorScheme,
    'london_underground': LondonUndergroundColorScheme,
}


def _find_settings_file():
    """Find settings.ini in common locations."""
    search_paths = [
        Path.cwd() / 'settings.ini',
        Path(__file__).parent.parent / 'settings.ini',
        Path.home() / '.drawio_roadmaps' / 'settings.ini',
    ]
    for path in search_paths:
        if path.exists():
            return path
    return None


def _detect_drawio_executable():
    """Auto-detect DrawIO executable path based on platform."""
    system = platform.system()

    if system == 'Windows':
        candidates = [
            r'C:\Program Files\draw.io\draw.io.exe',
            r'C:\Program Files (x86)\draw.io\draw.io.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Programs\draw.io\draw.io.exe'),
        ]
    elif system == 'Darwin':  # macOS
        candidates = [
            '/Applications/draw.io.app/Contents/MacOS/draw.io',
        ]
    else:  # Linux
        candidates = [
            '/usr/bin/drawio',
            '/snap/bin/drawio',
            '/usr/local/bin/drawio',
        ]

    # Check explicit paths first
    for path in candidates:
        if os.path.isfile(path):
            return path

    # Fall back to PATH lookup
    drawio_in_path = shutil.which('drawio') or shutil.which('draw.io')
    if drawio_in_path:
        return drawio_in_path

    return None


def _load_config():
    """Load configuration from settings.ini with defaults."""
    config = configparser.ConfigParser()

    settings_file = _find_settings_file()
    if settings_file:
        config.read(settings_file)

    return config


# Load configuration
_config = _load_config()

# DrawIO executable path (from settings, env var, or auto-detect)
DRAWIO_EXECUTABLE_PATH = (
    os.environ.get('DRAWIO_EXECUTABLE_PATH') or
    _config.get('drawio', 'executable_path', fallback='').strip() or
    _detect_drawio_executable()
)


class RoadmapConfig:
    class Global:
        show_quarters = _config.getboolean('global', 'show_quarters', fallback=True)

    class DrawIO:
        year_length_px = _config.getint('drawio', 'year_length_px', fallback=240)
        swimlane_height_px = _config.getint('drawio', 'swimlane_height_px', fallback=100)
        _scheme_name = _config.get('drawio', 'color_scheme', fallback='london_underground')
        color_scheme = ColorScheme(COLOR_SCHEMES.get(_scheme_name, LondonUndergroundColorScheme))

        # Layout constants (previously magic numbers)
        typographic_line_gap = _config.getint('drawio', 'typographic_line_gap', fallback=20)
        event_circle_size = _config.getint('drawio', 'event_circle_size', fallback=18)
        lifeline_vertical_spacing = _config.getint('drawio', 'lifeline_vertical_spacing', fallback=25)
        lifeline_label_height = _config.getint('drawio', 'lifeline_label_height', fallback=20)
        lifeline_label_max_chars = _config.getint('drawio', 'lifeline_label_max_chars', fallback=36)

    class Ascii:
        segment_width = _config.getint('ascii', 'segment_width', fallback=36)

    class PowerPoint:
        pass

    class Text:
        pass

