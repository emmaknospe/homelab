from nicegui import ui
from pages.home import home


def index():
    home()


ui.run()