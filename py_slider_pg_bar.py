from icedpygui.icedpygui import IPG, IpgProgressBarParams, IpgTextParams
from icedpygui import IpgColumnAlignment


ipg = IPG()


# Couple of callbacks for change and release
# The slider_id is not used since we are updating the bar and the text
def slider_on_change(_slider_id, data):
    ipg.update_item(on_change_id, IpgTextParams.Content, f"On Change value is {data}")
    ipg.update_item(bar_id, IpgProgressBarParams.Value, data)


def slider_on_release(_slider_id, data):
    ipg.update_item(on_release_id, IpgTextParams.Content, f"On Release value is {data}")


# Add the window
ipg.add_window(window_id="main", title="Slider Demo", width=500, height=500,
               pos_centered=True)

# Add the column and center the widgets in it.
ipg.add_column("main", container_id="col",
               align_items=IpgColumnAlignment.Center,
               width_fill=True, height_fill=True)

# Add some space for readability
ipg.add_space(parent_id="col", height=50.0)

# Equate the bar to get an id for the callback use.
bar_id = ipg.add_progress_bar(parent_id="col", min=0.0, max=100.0, value=50.0, width=300.0)

# Add a slide to change the value with two callbacks
ipg.add_slider(parent_id="col", min=0.0, max=100.0, step=0.5, value=50.0,
               width=300.0, on_change=slider_on_change, on_release=slider_on_release)

# Add some space for readability
ipg.add_space("col", height=100.0)

# Add a couple of text widget to display some data
on_change_id = ipg.add_text(parent_id="col", content=f"On Change value is 0")

on_release_id = ipg.add_text(parent_id="col", content=f"On Release value is 0")


# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
