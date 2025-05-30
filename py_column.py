from icedpygui import IPG, IpgColor, IpgColumnParam, IpgAlignment


# Moves the text to the center position
def align_center(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.AlignX, 
            value=IpgAlignment.Center)

     
# Moves the text to the end position
def align_end(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.AlignX, 
            value=IpgAlignment.End)
    
    
# Moves the text back to the start position
def align_start(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.AlignX, 
            value=IpgAlignment.Start)
    

# Moves text off start because padding on the left side
# padding = [top, right, bottom, left]
def padding(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.Padding, 
            value=[0.0, 0.0, 0.0, 50.0])  
    
# change container width
def width(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.Width, 
            value=200.0)
    
    
# change container height
def height(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.Height, 
            value=300.0)
 
# change container height
def spacing(btn_id):
    ipg.update_item(
            wid=col_id, 
            param=IpgColumnParam.Spacing, 
            value=20.0)
    
    
ipg = IPG()

cont_style = ipg.add_container_style(
                    border_width=2.0,
                    border_color=IpgColor.WHITE)



# Add the windows
ipg.add_window(
        window_id="main", 
        title="Container Styling", 
        width=600, 
        height=600,  
        pos_centered=True,
        debug=True)

ipg.add_row(
        window_id="main",
        container_id="row",
        width_fill=True)


# Add a column to hold the text widgets
col_id = ipg.add_column(
                window_id="main",
                container_id="col_txt",
                parent_id="row",
                align=IpgAlignment.Start,
                width_fill=True,height=400.0
                )

ipg.add_text(
        parent_id="col_txt",
        content="Some Text")

ipg.add_text(
        parent_id="col_txt",
        content="Some Text")

ipg.add_text(
        parent_id="col_txt",
        content="Some Text")


ipg.add_column(
        window_id="main",
        container_id="col_right",
        parent_id="row",
        width_fill=True,
        height=400.0
        )

# Add a button the center the alignment 
ipg.add_button(
        parent_id="col_right",
        label="Align Center",
        on_press=align_center)

# Add a button align end 
ipg.add_button(
        parent_id="col_right",
        label="Align End",
        on_press=align_end)

# Add a button align back to the start 
ipg.add_button(
        parent_id="col_right",
        label="Align Start",
        on_press=align_start)

# Add a button add padding of the contained items
ipg.add_button(
        parent_id="col_right",
        label="Padding",
        on_press=padding)

# Add a button change the container width
ipg.add_button(
        parent_id="col_right",
        label="Width",
        on_press=width)

# Add a button change the container height
ipg.add_button(
        parent_id="col_right",
        label="Height",
        on_press=height)

# Add a button change the solumn spacing
ipg.add_button(
        parent_id="col_right",
        label="Spacing",
        on_press=spacing)

# last thing is to start the session
ipg.start_session()