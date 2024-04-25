from icedpygui import IPG
from icedpygui import IpgContainerAlignment, IpgColumnAlignment, IpgTextParams


def button_pressed(btn_id):
    print(btn_id)


def checked(_chk_id: int, checked: bool):
    if checked:
        ipg.update_item(checked_text_id,
                        IpgTextParams.Content,
                        "I'm checked")

    else:
        ipg.update_item(checked_text_id,
                        IpgTextParams.Content,
                        "I'm not checked")


ipg = IPG()

ipg.add_window(window_id="main", title="Demo Window",
               width=600, height=500,
               pos_centered=True)

ipg.add_container("main", container_id="cont",
                  align_x=IpgContainerAlignment.Center,
                  align_y=IpgContainerAlignment.Center,
                  width_fill=True, height_fill=True)

ipg.add_column(window_id="main", container_id="col", parent_id="cont",
               align_items=IpgColumnAlignment.Center)

ipg.add_button(parent_id="col", label="Press Me!", on_press=button_pressed)

ipg.add_checkbox(parent_id="col", label="Check Me!!!", on_toggle=checked)

checked_text_id = ipg.add_text(parent_id="col",
                               content="This will change when I'm checked")

ipg.start_session()
