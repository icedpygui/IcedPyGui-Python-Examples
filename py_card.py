from icedpygui import IPG, IpgButtonStyles, IpgCardStyles, IpgCardParams

# Needed first, see other demos for using a class
ipg = IPG()


# Callback function for changing the card style
# The update function is (wid, param, value)
# wid = widget id
def update_card(btn_id):
    global card_id
    # The card_id is the first card in the series.  The only one that is changed.
    ipg.update_item(card_id, IpgCardParams.Head, "This is a new head with Danger style")
    ipg.update_item(card_id, IpgCardParams.Body, "This is a new body.")
    ipg.update_item(card_id, IpgCardParams.Foot, "This is a new foot")
    ipg.update_item(card_id, IpgCardParams.Style, IpgCardStyles.Danger)


# minimizes the first card, the button at the bottom left will maximize it.
def minimize_card(card_id):
    ipg.update_item(card_id, IpgCardParams.IsOpen, False)


# Pressing the bottom button will maximize the card, returning it to the top.
# Note the callback is from the button so the card_id has to be global.
# Normally, you would use a class or dataclass to store these ids.
def maximize_card(btn_id):
    global card_id
    ipg.update_item(card_id, IpgCardParams.IsOpen, True)


# window added first
ipg.add_window(window_id="main", title="Card Demo", width=800, height=800,
               pos_x=500, pos_y=100)

# add a container for the first button to center it.
ipg.add_container(window_id="main", container_id="btn_cont", align_x="center",
                  align_y="center", width_fill=True)

# add a button with a callback on_press to update the first card.
ipg.add_button("btn_cont",
               label="Pressing this will change the updatable items in the first card\n if you close card 1, "
                     "restore it by pressing on the bottom button.",
               on_press=update_card)

# add another container to center the column of cards to follow
ipg.add_container(window_id="main", container_id="cont", align_x="center",
                  align_y="center", width_fill=True, height_fill=True)

# put a scrollable in the container since the column will be larger than the container
ipg.add_scrollable(window_id="main", container_id="scroller", parent_id="cont", height_fill=True)

# put the column in the scrollable.  Note that the height of the scrollable is fill
# and then the column has to be shorter that the scrollable.  This seems to work
# most of the time but in some situations you'll need touse the window debug setting
# to see how things line up and getting the contents to scroll.  Just remember the
# scrollable has to be larger than the container, column, or row.
ipg.add_column(window_id="main", container_id="col", parent_id="scroller",
               align_items="center", width=400.0, spacing=0.0)

# Add a row at the bottom to hold the button
ipg.add_row("main", "bottom_row", parent_id="main",
            width_fill=True, spacing=0.0)

# add the button, this could have been hidden and when the card is minimized, the show it.
ipg.add_button("bottom_row", "Card 1", style=IpgButtonStyles.Primary,
               on_press=maximize_card)

# define the head and body of the cards.
head = "Python Iced_aw Card"
body = ("\nThis is the body of the card.  \nNote how the style is add style=IpgCardStyles.Primary.  This method should "
        "cut down on typo errors versus having to type in parameters that need to match exactly.")

# Styles are set by importing the appropriate module, in this case IpgCardStyles, and selecting
# the needed style from your IDE dropdown list.
card_id = ipg.add_card("col", head, "Primary: " + body, foot="Foot",
                       style=IpgCardStyles.Primary,
                       on_close=minimize_card)
ipg.add_card("col", head, "Secondary: " + body, foot="Foot",
             style=IpgCardStyles.Secondary)
ipg.add_card("col", head, "Success: " + body, foot="Foot",
             style=IpgCardStyles.Success)
ipg.add_card("col", head, "Danger: " + body, foot="Foot",
             style=IpgCardStyles.Danger)
ipg.add_card("col", head, "Warning: " + body, foot="Foot",
             style=IpgCardStyles.Warning)
ipg.add_card("col", head, "Info: " + body, foot="Foot",
             style=IpgCardStyles.Info)
ipg.add_card("col", head, "Light: " + body, foot="Foot",
             style=IpgCardStyles.Light)
ipg.add_card("col", head, "Dark: " + body, foot="Foot",
             style=IpgCardStyles.Dark)
ipg.add_card("col", head, body="White: " + body, foot="Foot",
             style=IpgCardStyles.White)
ipg.add_card("col", head, "Default: " + body, foot="Foot",
             style=IpgCardStyles.Default)

# if you use no style, them this is what you get, which is Default.
ipg.add_card("col", head, "Default: If you use no style setting.\n" + body, foot="Foot")

# Finally start the session, last command to be executed
ipg.start_session()
