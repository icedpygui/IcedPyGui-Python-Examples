from icedpygui import IPG, IpgTextParams


ipg = IPG()


# This callback sets the text content for the color selected.
# The cp_id is the color_picker id not used, so the color_id is
# a global variable obtained from the widget needing changed.
def color_submitted(_cp_id, color):
    value = f"Color selected = {color}"
    ipg.update_item(color_id, IpgTextParams.Content, value=value)


# window added first
ipg.add_window(window_id="main", title="ColorPicker Demo", width=800, height=800,
               pos_x=500, pos_y=100)

# add a container to align widgets center both x and y.
ipg.add_container(window_id="main", container_id="cont", align_x="center",
                  align_y="center", width_fill=True, height_fill=True)

# Since a container only holds one widget, a column is add next.
# The column only centers in the Y direction, so its put into a container.
ipg.add_column(window_id="main", container_id="col", parent_id="cont")

# color picker added
ipg.add_color_picker("col", on_submit=color_submitted)

# The text widget that will be updated is added and the id is obtained.
color_id = ipg.add_text("col", content="Color selected =")

# The starts the rust iced and needs to be executed last.
ipg.start_session()
