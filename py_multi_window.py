from icedpygui import IPG
from icedpygui import IpgColumnAlignment


ipg = IPG()

# Add Window 1, other windows can be added at any time, as long as
# you add the window then the containers and widgets.
ipg.add_window("main1", "MultWindow 1", 500, 600,
               200, 100)

# Add a column for the 2 widget below
ipg.add_column("main1", container_id="col1", parent_id="main1",
               align_items=IpgColumnAlignment.Center,
               width=800.0, height=800.0)

ipg.add_space(parent_id="col1", width=100.0, height=100.0)

ipg.add_text(parent_id="col1", content="Some text in Window 1")


# Add the second window
ipg.add_window("main2", "MultWindow 2", 500, 600,
               800, 100)

# Add a column for the widgets.  Except for the window ids, the ids
# for the widgets and containers in each window are kept separate so
# the name can be the same.  However, depending on how you set up
# your program, it might get confusing so it's probably a good idea
# to keep all ids unique.
ipg.add_column("main2", container_id="col2", parent_id="main2",
               align_items=IpgColumnAlignment.Center,
               width=800.0, height=800.0)

ipg.add_space(parent_id="col2", width=100.0, height=100.0)

ipg.add_text(parent_id="col2", content="Some Text in Window 2")

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
