from icedpygui import IPG, IpgTextParams


ipg = IPG()


# This callback sets the text content for the color selected.
# The cp_id is the color_picker id, not used, so the color_id is
# a global variable obtained from the widget needing to changed.
def color_submitted(_cp_id: int, color: list):
    value = f"Color selected = {color}"
    # We are changing the content of a text widget
    ipg.update_item(color_id, IpgTextParams.Content, value=value)


# window added first
ipg.add_window(window_id="main", title="ColorPicker Demo", width=600, height=600,
                pos_x=100, pos_y=25)

# add a container to align widgets center both x and y.
ipg.add_container(window_id="main", container_id="cont",
                  width_fill=True, height_fill=True)

# Since a container only holds one widget, a column is add next.
# The column will be center based on the container settings, but the
# items in the column will be defaulted to Start.
ipg.add_column(window_id="main", container_id="col", parent_id="cont")

# color picker added with a callback to set the text widget value
ipg.add_color_picker("col", on_submit=color_submitted)

# The text widget that will be updated is added and the id is obtained.
color_id = ipg.add_text("col", content="Color selected =")

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
