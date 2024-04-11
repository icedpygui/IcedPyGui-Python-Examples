from icedpygui import IPG, IpgTextParams
from icedpygui import IpgColumnAlignment

ipg = IPG()

# Ote type of input will follow soon, in the meantime
# you can just convert the text to whatever type you want


# Add the callback for the text_input, 3 are available
# The text_input id is not used because we are just updating the
# text widget.
# When you type in the text, this fires each time
def on_input(_txt_input_id, data):
    ipg.update_item(text_on_input_id, IpgTextParams.Content, value=data)


# This only fires when you pres enter to submit
def on_submit(_txt_input_id, data):
    ipg.update_item(text_on_submit_id, IpgTextParams.Content, value=data)


# This fired when you paste something into the field
# To submit it, press enter.
def on_paste(_txt_input_id, data):
    ipg.update_item(text_on_paste_id, IpgTextParams.Content, value=data)


# add the window
ipg.add_window("main", "Text Input Demo", 800, 800,
               pos_centered=True)

# add the column for the widgets, centered
ipg.add_column("main", container_id="col",
               align_items=IpgColumnAlignment.Center,
               height_fill=True, width_fill=True)

# Add some space at the top
ipg.add_space(parent_id="col", height=150.0)

# Add the text_input widget
ipg.add_text_input(parent_id="col", placeholder="Input Some Text",
                   width=200.0,
                   on_input=on_input,
                   on_submit=on_submit,
                   on_paste=on_paste)

# Add the text widget to display the info
text_on_input_id = ipg.add_text(parent_id="col", content="Text here will be added when typed")

text_on_submit_id = ipg.add_text(parent_id="col", content="Text here will be added when submitted")

text_on_paste_id = ipg.add_text(parent_id="col", content="Text here will be added when pasted")

# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
