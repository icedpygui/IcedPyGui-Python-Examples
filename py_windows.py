from icedpygui import IPG, IpgWindowThemes, IpgWindowParams, IpgColumnAlignment

ipg = IPG()

# The debug is set to True in this case to allow you to see the outline of
# the widgets.  This is useful for trouble shooting widget placement.
# The second window was added after the first windows widgets were added,
# but the windows can be added at any time, as long as they are added before 
# before their widgets.


def change_wnd_theme(pl_id, selected, wnd_id):
    if selected == "Dark":
        ipg.update_item(wnd_id, IpgWindowParams.Theme, IpgWindowThemes.Dark)
    if selected == "Nord":
        ipg.update_item(wnd_id, IpgWindowParams.Theme, IpgWindowThemes.Nord)
    if selected == "SolarizedLight":
        ipg.update_item(wnd_id, IpgWindowParams.Theme, IpgWindowThemes.SolarizedLight)
    if selected == "TokyoNightLight":
        ipg.update_item(wnd_id, IpgWindowParams.Theme, IpgWindowThemes.TokyoNightLight)


#  The default position is center so a specific position is used to avoid overlaying.
wnd_id_1 = ipg.add_window("window1", "Window 1", 400, 400,
                          300, 100,
                          theme=IpgWindowThemes.Nord)

# A container is added first since all widgets must be placed into a container, column, or row.
# A container can have only one widget.  Use a column or row for more than one.
ipg.add_column(window_id="window1", container_id="col_1",
               width_fill=True, height_fill=True,
               align_items=IpgColumnAlignment.Center)

options = ["Dark", "Nord", "SolarizedLight", "TokyoNightLight"]
ipg.add_pick_list(parent_id="col_1", options=options, placeholder="Select Theme",
                  on_select=change_wnd_theme, user_data=wnd_id_1)

# *********************************************************************************

# Second window added with the light theme
wnd_id_2 = ipg.add_window("window2", "Window 2", 400, 400,
                          800, 100,
                          theme=IpgWindowThemes.SolarizedLight)

ipg.add_column(window_id="window2", container_id="col_1",
               width_fill=True, height_fill=True,
               align_items=IpgColumnAlignment.Center)

options = ["Dark", "Nord", "SolarizedLight", "TokyoNightLight"]
ipg.add_pick_list(parent_id="col_1", options=options, placeholder="Select Theme",
                  on_select=change_wnd_theme, user_data=wnd_id_2)

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
