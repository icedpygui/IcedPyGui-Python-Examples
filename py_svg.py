from icedpygui import IPG, IpgContainerAlignment, IpgRowAlignment
from icedpygui import IpgSvgParams
import os

# some global vars
width = 400.0
height = 400.0

# Since user data is include, it will need to be
# added to all whether used on or.
def on_press(btn_id, _user_data):
    print("on press", btn_id)


def on_release(btn_id: int, _user_data):
    print("on release", btn_id)


def on_right_press(btn_id: int, _user_data):
    print("on right press, btn_id")


def on_right_release(id: int, _user_data):
    print("on right release", id)


def on_middle_press(btn_id: int, _user_data):
    print("on middle press", btn_id)


def on_middle_release(btn_id: int, _user_data):
    print("on middle release", btn_id)


def on_enter(btn_id: int, user_data: any):
    print("entered", btn_id, user_data)    


def on_move(btn_id: int, point: dict, _user_data):
    print("on move", btn_id, point)


def on_exit(btn_id, _user_data):
    print("on exit", btn_id)

# The sixe of the svg will only get as big as the size of
# the container it's in.
def increase_size(btn_id):
    global width, height
    width += 10
    height += 10
    ipg.update_item(svg_id, IpgSvgParams.Width, width)
    ipg.update_item(svg_id, IpgSvgParams.Height, height)


def decrease_size(btn_id):
    global width, height
    width -= 10
    height -= 10
    ipg.update_item(svg_id, IpgSvgParams.Width, width)
    ipg.update_item(svg_id, IpgSvgParams.Height, height)

    

ipg = IPG()

ipg.add_window(window_id="main", title="Main", width=600, height=600, 
               pos_centered=True)

ipg.add_container(window_id="main", container_id="cont", 
                  width_fill=True, height_fill=True,
                  align_x=IpgContainerAlignment.Center,
                  align_y=IpgContainerAlignment.Center)

# Setting up the image path
cwd = os.getcwd()
svg_path = cwd + "/resources/tiger.svg"

ipg.add_row(window_id="main", container_id="row", 
            align_items=IpgRowAlignment.Center)

ipg.add_button(parent_id="row", label="Increase Size", on_press=increase_size)
ipg.add_button(parent_id="row", label="Decrease Size", on_press=decrease_size)

svg_id = ipg.add_svg(parent_id="cont",
                        width=400.0,
                        height=400.0,
                        svg_path= svg_path,
                        on_enter=on_enter,
                        on_exit=on_exit,
                        on_move=on_move,
                        on_press=on_press,
                        on_release=on_release,
                        on_middle_press=on_middle_press,
                        on_middle_release=on_middle_release,
                        on_right_press=on_right_press,
                        on_right_release=on_right_release,
                        user_data="Some Data")


ipg.start_session()
