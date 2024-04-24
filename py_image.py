from icedpygui import IPG, IpgImageParams, IpgTextParams
from icedpygui import IpgColumnAlignment
import os


ipg = IPG()

# Note: The image is put into a mouse area container, within IPG, where these
# callbacks can be executed.  If you are using the event_mouse,
# things will get confusing.  Therefore, you'll need to disable
# the event_mouse on image entering and then enabling it on image exit.


# Setting up the image path
cwd = os.getcwd()
path_happy = cwd + "/resources/rustacean-flat-happy.png"
path_orig = cwd + "/resources/rustacean-orig-noshadow.png"

# Global var for the ids.
image_ids = []


# Callback for when the image is selected
def image_selected(image_id):
    # Get the index of the image which is the index of the text widget
    index = image_ids.index(image_id)
    ipg.update_item(text_ids[index], IpgTextParams.Content, "You Pressed Me!")


# Callback for when the mouse is moving over the image.
def on_mouse_move(image_id, point):
    index = image_ids.index(image_id)
    x = '{:{}.{}}'.format(point.get('x'), 10, 4)
    y = '{:{}.{}}'.format(point.get('y'), 10, 4)
    ipg.update_item(text_points[index], IpgTextParams.Content, f"x={x}\ny={y}\n")


# On exit, reset the text widget
def on_mouse_exit(image_id):
    index = image_ids.index(image_id)
    ipg.update_item(text_points[index], IpgTextParams.Content, "Point")


# On right_press, original shows
def show_original(image_id):
    index = image_ids.index(image_id)
    ipg.update_item(image_ids[index], IpgImageParams.ImagePath, path_orig)


# On middle press, happy shows
def show_happy(image_id):
    index = image_ids.index(image_id)
    ipg.update_item(image_ids[index], IpgImageParams.ImagePath, path_happy)


# Add the window
ipg.add_window(window_id="main", title="Date Picker Demo", width=800, height=800,
               pos_x=500, pos_y=100)

# Add a column to hold the widgets
ipg.add_column(window_id="main", container_id="col", parent_id="main",
               width_fill=True, height_fill=True,
               align_items=IpgColumnAlignment.Center)

# Add a space for readability
ipg.add_space(parent_id="col", height=50.0)

# Add some text info
ipg.add_text("col",
             "Pressing the left mouse button, while over an image, will display a message.  "
             "Pressing the right mouse button, while over the "
             "image, will change the image and the middle to change back.  "
             "While the mouse is over an image the the mouse position will be displayed.",
             width=600.0)

# adding a row for the line of images
ipg.add_row(window_id="main", container_id="row1", parent_id="col")

# Looping to add the images, each will have the same callback
# but they could be different depending on your needs.
for i in range(0, 5):
    image_ids.append(ipg.add_image(parent_id="row1", image_path=path_happy,
                                   width=100.0, height=50.0,
                                   on_press=image_selected,
                                   on_move=on_mouse_move,
                                   on_exit=on_mouse_exit,
                                   on_right_press=show_original,
                                   on_middle_press=show_happy,
                                   ))

# add a row for the information
ipg.add_row(window_id="main", container_id="row2", parent_id="col")

# Using some global variables for the ids needed for the callbacks
text_ids = []
text_points = []

# Add the text below each image.  There are a number of ways this could be done,
# Another way is to add a column with the image, info, and points then put the columns into row.
for i in range(0, 5):
    text_ids.append(ipg.add_text(parent_id="row2", content="Press image above me", width=100.0))

# adding a final row for the points display
ipg.add_row(window_id="main", container_id="row3", parent_id="col")

for i in range(0, 5):
    text_points.append(ipg.add_text(parent_id="row3", content="Point", width=100.0))


# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
