from icedpygui import IPG
from icedpygui import IpgColumnAlignment


ipg = IPG()

# Add the window
ipg.add_window("main", "Rule Demo", 500, 600,
               pos_centered=True)

# Add a container for alignment
ipg.add_container("main", "cont", width_fill=True, height_fill=True)

# Add a column to hold the wigets
ipg.add_column("main", container_id="col", parent_id="cont",
               align_items=IpgColumnAlignment.Center)

# Add some spacing
ipg.add_space(parent_id="col", width=500, height=20.0)

# Add the rules
ipg.add_rule_vertical("col", height=250)
ipg.add_rule_horizontal("col", width=250)

ipg.add_text(parent_id="col", content="There a vertical and horizontal divider above me, centered.")

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
