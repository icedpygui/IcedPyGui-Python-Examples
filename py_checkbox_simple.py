from icedpygui import IPG, IpgCheckboxParams

ipg = IPG()

x_id = ipg.generate_id()


def on_toggle(id, data, user_data):
    ipg.update_item(x_id, IpgCheckboxParams.IconX, data)


ipg.add_window("main", "CheckBox Demo",
               800, 800, 500, 100)

ipg.add_container(window_id="main", container_id="cont", width_fill=True,
                  height_fill=True, align_x="center", align_y="center")

ipg.add_column(window_id="main", container_id="col", parent_id="cont",
               width=400.0, height=500.0)

ipg.add_checkbox(parent_id="col", label="Check Me!!!",
                 on_toggle=on_toggle,
                 user_data="Some string data")

ipg.add_checkbox(parent_id="col", id=x_id, label="Check Me!!!", is_checked=True)

ipg.start_session()