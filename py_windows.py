from icedpygui import IPG, IpgWindowThemes

ipg = IPG()

# The debug is set to True in this case to allow you to see the outline of
# the widgets.  This is useful for trouble shooting widget placement.
# The second window was added after the first windows widgets were added,
# but the windows can be added at any time, as long as they are added before 
# before their widgets.


#  The default position is center so a specific position is used to avoid overlaying.
ipg.add_window("window1", "Window 1", 400, 400,
               300, 100,
               theme=IpgWindowThemes.Nord)

# A container is added first since all widgets must be placed into a container, column, or row.
# A container can have only one widget.  Use a column or row for more than one.
ipg.add_container(window_id="window1", container_id="cont1",
                  width_fill=True, height_fill=True)

ipg.add_text(parent_id="cont1", content="Window 1")

# *********************************************************************************

# Second window added with the light theme
ipg.add_window("window2", "Window 2", 400, 400,
               800, 100,
               theme=IpgWindowThemes.SolarizedLight)

ipg.add_container("window2", container_id="col2",
                  width_fill=True, height_fill=True)

ipg.add_text(parent_id="col2", content="Window 2")


# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
