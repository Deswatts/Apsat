# dmgbuild 配置文件
import os

app_path = os.path.join(os.environ.get("PWD", "."), "dist", "main.app")
app_name = "Apsat"

files = [app_path]
symlinks = {"Applications": "/Applications"}

icon = os.path.join(os.environ.get("PWD", "."), "assets", "icon.png")

background = None
window_rect = ((200, 200), (640, 400))
icon_size = 128
text_size = 14

default_view = "icon-view"
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False

arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = "bottom"
text_size = 16
icon_locations = {
    app_name: (140, 200),
    "Applications": (500, 200),
}
