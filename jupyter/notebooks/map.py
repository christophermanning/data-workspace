from ipyleaflet import (
    LayerGroup,
    WidgetControl,
    AwesomeIcon,
)
import ipyleaflet

from ipywidgets import HTML, Button, Layout


class Map:
    def __init__(self, center=(41.8, -87.5)):
        self.m = ipyleaflet.Map()
        self.center = center

        self.markers = []

        self.reset_zoom()

        self.map_markers = LayerGroup()
        self.m.add(self.map_markers)

        button = Button(icon="home", tooltip="Reset Zoom", layout=Layout(width="35px"))
        button.on_click(self.reset_zoom)
        self.m.add(WidgetControl(widget=button, position="topleft"))

    def _ipython_display_(self):
        self.add_markers(self.markers)
        display(self.m)

    def reset_zoom(self, params=None):
        self.m.center = self.center
        self.m.zoom = 10

    def add_markers(self, markers):
        self.map_markers.clear_layers()
        for marker in markers:
            self.add_marker(marker)

    def add(self, o):
        self.m.add(o)

    def add_marker(self, marker):
        message = HTML()
        if marker.description:
            message.value = marker.description
        self.map_markers.add(
            ipyleaflet.Marker(
                location=marker.location,
                draggable=False,
                popup=message,
                icon=AwesomeIcon(name=marker.icon, marker_color=marker.color),
            )
        )


class Marker:
    def __init__(self, location, description=None, icon="home", color="blue"):
        self.location = location
        self.description = description
        self.icon = icon
        self.color = color
