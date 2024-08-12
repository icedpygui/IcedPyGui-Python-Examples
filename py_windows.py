from icedpygui import IPG, IpgWindowTheme, IpgWindowParam, IpgAlignment

ipg = IPG()


def change_wnd_theme(pl_id, selected, wnd_id):
    if selected == "Dark":
        ipg.update_item(wnd_id, IpgWindowParam.Theme, IpgWindowTheme.Dark)
    if selected == "Nord":
        ipg.update_item(wnd_id, IpgWindowParam.Theme, IpgWindowTheme.Nord)
    if selected == "SolarizedLight":
        ipg.update_item(wnd_id, IpgWindowParam.Theme, IpgWindowTheme.SolarizedLight)
    if selected == "TokyoNightLight":
        ipg.update_item(wnd_id, IpgWindowParam.Theme, IpgWindowTheme.TokyoNightLight)


debug = False


# Setting the debug for the window to True helps to align the widgets
# in complex situations.  I usually put it on the screen and toggle it
# to help figure out the widget placements.
def set_debug(_btn_id):
    global debug
    debug = not debug
    ipg.update_item(wnd_id_1, IpgWindowParam.Debug, debug)


#  The default position is center so a specific position is used to avoid overlaying.
wnd_id_1 = ipg.add_window("window1", "Window 1", 400, 400,
                           pos_x=100, pos_y=25,
                          theme=IpgWindowTheme.Nord)

# A column container is added first since all widgets must be placed into a container, column, or row.
# A container can have only one widget.  Use a column or row for more than one.
ipg.add_column(window_id="window1", container_id="col_1",
               width_fill=True, height_fill=True,
               align_items=IpgAlignment.Center)

# Adding some extra spacing
ipg.add_space(parent_id="col_1")

# Adding instructions
ipg.add_text(parent_id="col_1", content="Select a Theme then press the Debug button to see the oulines of the widgets")

ipg.add_space(parent_id="col_1", height=20)

options = ["Dark", "Nord", "SolarizedLight", "TokyoNightLight"]
ipg.add_pick_list(parent_id="col_1", options=options, placeholder="Select Theme",
                  on_select=change_wnd_theme, user_data=wnd_id_1)

# A space is added which will be shown when the debug button is pressed
ipg.add_space(parent_id="col_1", width=100, height=100)
ipg.add_button(parent_id="col_1", label="Debug", on_press=set_debug)
# *********************************************************************************

# Second window added with the light theme
wnd_id_2 = ipg.add_window("window2", "Window 2", 400, 400,
                           pos_x=600, pos_y=25,
                          theme=IpgWindowTheme.SolarizedLight)

ipg.add_column(window_id="window2", container_id="col_1",
               width_fill=True, height_fill=True,
               align_items=IpgAlignment.Center)

ipg.add_space(parent_id="col_1", height=50)

options = ["Dark", "Nord", "SolarizedLight", "TokyoNightLight"]
ipg.add_pick_list(parent_id="col_1", options=options, placeholder="Select Theme",
                  on_select=change_wnd_theme, user_data=wnd_id_2)

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
