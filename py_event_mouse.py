from icedpygui import IPG, IpgTextParams
from icedpygui import IpgColumnAlignment


# instantiate IPG
ipg = IPG()

# make a global var to hold some scroll data
scroll_total = 0


# The mouse move callback will fire when the window opens.
# The user_data is not used here, but needed since it was supplied as a parameter
# The mouse_id is not used since we're just updating the text widget.
# The move data is a dictionary as all of the events data are.
def mouse_move(mouse_id, name, point, _user_data):
    ipg.update_item(text_for_moved, IpgTextParams.Content, f"{name} {point}")


# The mouse events have a name parameter that's returned as a convenience for the user.
# Even if not used, you need to have it as a parameter, otherwise you'll get an error.
# In this case, I used the same callback for all of the mouse buttons.  The name will give
# you an option to use one callback are a callback for each type of event.
def mouse_button_pressed(mouse_id, name, user_data):
    ipg.update_item(text_for_pressed, IpgTextParams.Content, f"{name}")
    ipg.update_item(text_for_user_data, IpgTextParams.Content, f"user data = {user_data}")


# Essentially the same as above.
def mouse_button_released(mouse_id, name, user_data):
    ipg.update_item(text_for_released, IpgTextParams.Content, f"{name}")


# The scroll data is a dictionary
def mouse_button_scrolled(mouse_id, name, scroll, _user_data):
    global scroll_total
    scroll_total += scroll.get("y")
    ipg.update_item(text_for_scroll, IpgTextParams.Content, f"{name} {scroll} total = {scroll_total}")


# An event can be added at any time since they are not widgets or containers.
ipg.add_event_mouse(enabled=True,
                    on_move=mouse_move,
                    on_left_press=mouse_button_pressed,
                    on_left_release=mouse_button_released,
                    on_middle_press=mouse_button_pressed,
                    on_middle_release=mouse_button_released,
                    on_right_press=mouse_button_pressed,
                    on_right_release=mouse_button_released,
                    on_middle_scroll=mouse_button_scrolled,
                    user_data="Some Data",
                    )

# Adding a window
ipg.add_window("main", "Mouse Handler Demo", 600, 600,
               pos_centered=True)

# Add a column to hold the widgets
ipg.add_column("main", container_id="col",
               align_items=IpgColumnAlignment.Center,
               width_fill=True, height_fill=True)

# Add some spacing
ipg.add_space(parent_id="col", height=150.0)

# Add all of the text widget for info display
text_for_moved = ipg.add_text(parent_id="col", content="Mouse position will be here")
text_for_pressed = ipg.add_text(parent_id="col", content="Button presses will show here")
text_for_released = ipg.add_text(parent_id="col", content="Button releases will show here")
text_for_scroll = ipg.add_text(parent_id="col", content="Button scroll data will show here")
text_for_user_data = ipg.add_text(parent_id="col", content="Button user data will show here")


# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
