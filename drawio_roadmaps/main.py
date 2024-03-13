import sys

from drawio_roadmaps.loaders.loaders import RoadmapLoaderFactory
from drawio_roadmaps.renderer_manager import RendererManager, RendererType


# ToDo: Loaders need sorting out and moving out to the loaders module. No need for them to sit here.


def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <source_type> <renderer_type> <source_path>")
        return

    source_type = sys.argv[1]
    renderer_type = sys.argv[2]
    source_path = sys.argv[3]

    loader = RoadmapLoaderFactory.get_loader(source_type)
    roadmap = loader.load(source_path)

    renderer_manager = RendererManager()

    if renderer_type.lower() == "ascii":
        renderer_manager.set_renderer_type(RendererType.ASCII)
    elif renderer_type.lower() == "drawio":
        renderer_manager.set_renderer_type(RendererType.DRAWIO)
    elif renderer_type.lower() == "powerpoint":
        renderer_manager.set_renderer_type(RendererType.POWERPOINT)
    elif renderer_type.lower() == "string":
        renderer_manager.set_renderer_type(RendererType.STRING)
    else:
        print(f"Invalid renderer type: {renderer_type}")
        return

    print(roadmap.render())

if __name__ == "__main__":
    main()