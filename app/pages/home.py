from nicegui import ui


@ui.page('/')
def home():
    ui.markdown("""
# Homelab Dashboard
    """)