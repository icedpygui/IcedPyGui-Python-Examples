import os
import random
from collections import defaultdict
from icedpygui import IPG, IpgColor, IpgStackParam, IpgMousePointer, IpgImageContentFit
from icedpygui import IpgTextParam, IpgImageParam

# The solitaire game is just a demonstration of how to use IPG in a more
# complex way.  It also highlighted a few issues I had while make the game.
# Examples help but until you do a real program, sometimes you can't 
# catch the issues.  

# This game only used the containers and no canvas drawing.  I made it
# a little more difficult from a move validation and restarting the game.
# Later on I plan to make the same game using the canvas but the canvas still
# needs work regarding actively moving things arrow.

class solitaire:
    def __init__(self) -> None:
        self.ipg = IPG()
        self.cwd = os.getcwd()
        self.path = self.cwd + "/resources/cards/"
        self.card_width: float=100.0
        self.card_height: float=150.0
        self.shuffled_indexes: list=[]
        self.cards: dict=defaultdict(dict)
        self.stock: list=[]
        self.waste: list=[]
        self.covers: list=[]
        self.tableau: list=[]
        self.status_id: int=0
        self.deal_amount: int=3
        self.content: str=""
        self.rounds = 0
        self.rounds_id = 0
        self.cards_to_play = "3"
        self.tab_cover_cards_wids = []
        
        self.stock_cover_id: int=0

        self.origin: int=None
        self.target: int=None
        
        self.foundation_top_card_value: list=[0] * 4
        self.foundation_top_card_suite: list=[None] * 4
        
        # styles
        self.white_border = 0

        # if the cards in the tableau going outside of this height,
        # an error will occur.  Increase the window height and this
        # if needed 
        self.stack_height = 470.0 

    def start_game(self):
        self.create_styles()
        # add the main containers
        self.ipg.add_window(window_id="main", 
                            title="Solitaire",
                            width=1000.0,
                            height=700.0,
                            pos_centered=True,
                            # debug=True
                            )
        
        self.ipg.add_row(window_id="main",
                         container_id="main_row",
                         width_fill=True,
                         height_fill=True,
                         spacing=2.0)
        
        self.ipg.add_container(window_id="main",
                               container_id="control_cont",
                               parent_id="main_row",
                               width=175.0,
                               height_fill=True,
                               style_id=self.white_border)
        
        self.ipg.add_column(window_id="main",
                            container_id="control_col",
                            parent_id="control_cont",
                            padding=[20.0],
                            height_fill=True)
        
        self.ipg.add_container(window_id="main",
                               container_id="main_cont",
                               parent_id="main_row",
                               width_fill=True,
                               height_fill=True,
                               style_id=self.white_border)
        
        self.ipg.add_column(window_id="main",
                            container_id="main_col",
                            parent_id="main_cont",
                            width_fill=True,
                            height_fill=True)
        
        self.define_controls()
        self.create_slots()
        self.load_shuffle_cards()
        self.deal_cards()
        self.ipg.start_session()
        
    def restart_play(self, btn_id: int):
        self.rounds = 0
        self.ipg.update_item(self.rounds_id, IpgTextParam.Content, f"Card Play Rounds: {self.rounds}")

        # reshuffle the original card indexes
        random.shuffle(self.shuffled_indexes)
        
        # get the stock cover card amd mouseareas from the cards before re-initializing
        stock_cover_card = self.cards.get(self.stock_cover_id)
        mas = []
        tab_cover_cards = defaultdict(dict)
        for wid in self.cards:
            card = self.cards.get(wid)
            name = card.get("name")
            if name == "stock blank":
                mas.append(card)
            if "foundation" in name:
                mas.append(card)
            if name == "tab_mousearea":
                mas.append(card)
            if name == "tab_cover":
                tab_cover_cards[wid] = card

        # fill the tableau
        self.cards = defaultdict(dict)
        self.tableau = []
        self.content = ""
        index = 0
        cover_index = 0
        for i in range(0, 7):
            self.tableau.append([])
            for j in range(0, 13):
                
                if j <= i:
                    card = self.shuffled_indexes[index] 
                    card["tab_column"] = i
                    card["tab_index"] = j
                    card["tableau"] = True
                    card["foundation"] = False
                    card["stock"] = False
                    card["waste"] = False
                    wid = card.get("wid")
                    self.cards[wid] = card
                    self.tableau[i].append(wid)
                    self.ipg.move_widget(window_id="main",
                                widget_id=wid,
                                target_container_str_id=f"tabcol_{i}_{j}"
                                )
                    index += 1
                    
                if j < i:
                    wid = self.tab_cover_cards_wids[cover_index]
                    cover = tab_cover_cards.get(wid)
                    cover["index"] = index-1
                    cover["tab_column"] = i
                    cover["tab_index"] = j
                    cover["is_cover"] = True
                    cover["tableau"] = True
                    cover_index += 1
                    self.ipg.move_widget(window_id="main",
                                widget_id=wid,
                                target_container_str_id=f"tab_blank_{i}_{j}"
                                )
                    self.cards[wid] = cover
        
        # add cards left to stock
        self.stock = []
        self.waste = []
        
        for idx in range(index, len(self.shuffled_indexes)):
            card = self.shuffled_indexes[idx].copy()
            card["stock"] = True
            card["waste"] = False
            card["tableau"] = False
            card["foundation"] = False

            wid = card.get("wid")
            self.stock.append(wid)
            self.cards[wid] = card
            self.ipg.move_widget(window_id="main",
                                 widget_id=wid,
                                 target_container_str_id="stack_stock_pile"
                                 )    
 
        # restore the stock cover card and mouseares cards
        self.ipg.move_widget("main", self.stock_cover_id, "stack_stock_pile")
        self.cards[self.stock_cover_id] = stock_cover_card

        for ma in mas:
            self.cards[ma.get("wid")] = ma        
                
    def create_styles(self):
        self.white_border = self.ipg.add_container_style( 
                                        border_color=IpgColor.WHITE,
                                        border_width=2.0)

    def define_controls(self):
        self.ipg.add_button(parent_id="control_col",
                            label="Restart Play",
                            on_press=self.restart_play)
        self.rounds_id = self.ipg.add_text(parent_id="control_col",
                          content="Card Play Rounds:")
        self.ipg.add_text(parent_id="control_col",
                          content="Cards to Play:")
        self.ipg.add_pick_list(parent_id="control_col",
                               options=["1", "3"],
                               on_select=self.select_cards_to_play,
                               selected=self.cards_to_play)
        self.ipg.add_space(parent_id="control_col", height=50.0)
        self.ipg.add_text(parent_id="control_col",
                          content="Instructions:\nCards are moved by selecting source and destination using mouse.  If a card fails to move it means the validation failed, wrong color or value.\nTo cancel a move, click any other place on the canvas")
    
    def select_cards_to_play(self, picklist_id: int, value: str):
        self.cards_to_play = int(value)
        
    def create_slots(self):
        self.cards = defaultdict(dict)
        # add row for stock, waste, and foundation cards
        self.ipg.add_row(window_id="main", 
                         container_id="stock_row",
                         parent_id="main_col",
                         height=self.card_height,
                         spacing=10.0,
                         padding=[5.0]
                         )
        
        # add some beginning space
        self.ipg.add_space(parent_id="stock_row",
                           width=20.0)
        
        # add the stock container to the row
        self.ipg.add_container(window_id="main",
                        container_id="stock",
                        parent_id="stock_row",
                        padding=[0.0],
                        style_id=self.white_border)
        
        # add the stack in
        self.ipg.add_stack(window_id="main",
                           container_id="stack_stock_pile",
                           parent_id="stock",
                           width=self.card_width,
                           height=self.card_height)
        wid = self.ipg.add_mousearea(window_id="main",
                                    container_id="mouse_stock_pile",
                                    parent_id="stack_stock_pile",
                                    mouse_pointer=IpgMousePointer.Grab,
                                    on_press=self.card_selected,
                                    )
        stock = {}
        stock["wid"] = wid
        stock["name"] = "stock blank"
        stock["value"] = 0
        stock["suite"] = None
        stock["color"] = None
        stock["foundation"] = False
        stock["tableau"] = False
        stock["stock"] = True
        stock["waste"] = False
        stock["is_cover"] = True
        stock["reload"] = True
        self.cards[wid] = stock
        
        # add the waste container to the row
        self.ipg.add_container(window_id="main",
                                container_id="waste",
                                parent_id="stock_row",
                                width=self.card_width,
                                height=self.card_height,
                                padding=[0.0],
                                style_id=self.white_border)

        # add the stack in
        self.ipg.add_stack(window_id="main",
                           container_id="stack_waste_pile",
                           parent_id="waste",
                           width=self.card_width,
                           height=self.card_height,
                           )

        # add a space between waste and foundation
        self.ipg.add_space(parent_id="stock_row",
                           width=self.card_width
                           )

        # Add the 4 foundation slots
        for i in range(0, 4):
            self.ipg.add_stack(window_id="main",
                           container_id=f"foundation_{i}",
                           parent_id="stock_row",
                           width=self.card_width,
                           height=self.card_height,
                           )
            
            wid = self.ipg.add_mousearea(window_id="main",
                                    container_id=f"foundation_mouse_{i}",
                                    parent_id=f"foundation_{i}",
                                    mouse_pointer=IpgMousePointer.Grab,
                                    on_press=self.card_selected,
                                    )
            fd = {}
            fd["wid"] = wid
            fd["name"] = f"foundation {i}"
            fd["value"] = 0
            fd["suite"] = None
            fd["color"] = None
            fd["foundation"] = True
            fd["tableau"] = False
            fd["fd_index"] = i
            self.cards[wid] = fd
            
            self.ipg.add_container(window_id="main",
                                    container_id=f"foundation_container_{i}",
                                    parent_id=f"foundation_{i}",
                                    width=self.card_width,
                                    height=self.card_height,
                                    padding=[0.0],
                                    style_id=self.white_border)

        # add a container off screen to hide widget that become unused
        self.ipg.add_space(parent_id="stock_row",
                           width=200.0)
        self.ipg.add_stack(window_id="main",
                               container_id="hidden",
                               parent_id="stock_row",
                               show=False)

        # Add a space between the rows
        self.ipg.add_space(parent_id="main_col", height=20.0)
        
        # add a sttus row
        self.ipg.add_row(window_id="main",
                         container_id="status_row",
                         parent_id="main_col")
        self.ipg.add_space(parent_id="status_row", width=20.0)
        self.status_id = self.ipg.add_text(parent_id="status_row", content="Status: Selected None")

        # Add a row for the tableau cards
        self.ipg.add_row(window_id="main",
                         container_id="tableau_row",
                         parent_id="main_col",
                         spacing=10.0
                         )
        
        # Add a space at the beginning of the row
        self.ipg.add_space(parent_id="tableau_row",
                           width=20.0)
        
        # Add the 7 card tableau slots
        for i in range(0, 7):
            # initialize the tableau list
            self.tableau.append([])
            # Add in the stacks
            self.ipg.add_stack(window_id="main",
                                container_id=f"tab_stack_{i}",
                                parent_id="tableau_row",
                                width=self.card_width,
                                height=self.stack_height,
                                )
            wid = self.ipg.add_mousearea(window_id="main",
                                        container_id=f"tab_stack_ma_{i}",
                                        parent_id=f"tab_stack_{i}",
                                        mouse_pointer=IpgMousePointer.Grab,
                                        on_press=self.card_selected,
                                        )
            ma = {}
            ma["wid"] = wid
            ma["name"] = "tab_mousearea"
            ma["tableau"] = True
            ma["stock"] = False
            ma["waste"] = False
            ma["foundation"] = False
            ma["tab_column"] = i
            ma["tab_index"] = -1
            self.cards[wid] = ma
            
    def load_shuffle_cards(self):
        suites = [
            ("hearts", "RED"),
            ("diamonds", "RED"),
            ("clubs", "BLACK"),
            ("spades", "BLACK"),
        ]
        ranks = [
            ("Ace", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
            ("8", 8),
            ("9", 9),
            ("10", 10),
            ("Jack", 11),
            ("Queen", 12),
            ("King", 13),
        ]

        self.shuffled_indexes = []

        for (suite, color) in suites:
            for (name, value) in ranks:
                d = {"wid": None,
                    "suite": suite,
                    "color": color,
                    "name": name,
                    "value": value,
                    "stock": False,
                    "waste": False,
                    "tableau": False,
                    "foundation": False,
                    "tab_column": None,
                    "tab_index": None,
                    "fd_index": 0,
                    "is_cover": False,
                    "is_card": True,
                    }
                self.shuffled_indexes.append(d)
        
        random.shuffle(self.shuffled_indexes)

    def deal_cards(self):
        self.content = ""
        index = 0
        for i in range(0, 7):
            for j in range(0, 13):
                self.ipg.add_column(window_id="main",
                                    container_id=f"tabcol_{i}_{j}",
                                    parent_id=f"tab_stack_{i}",)
                
                # Add a blank at top to hide the card below
                self.ipg.add_space(parent_id=f"tabcol_{i}_{j}",
                                    height=20*j)

                if j <= i:
                    card = self.shuffled_indexes[index] 
                    card["tab_column"] = i
                    card["tab_index"] = j
                    card["tableau"] = True
                    file = f"{self.path}/{card.get('suite')}/{card.get('value')}.png"
                    wid = self.ipg.add_image(parent_id=f"tabcol_{i}_{j}", 
                                        image_path=file,
                                        width=self.card_width, 
                                        height=self.card_height,
                                        content_fit=IpgImageContentFit.Fill,
                                        mouse_pointer=IpgMousePointer.Grab,
                                        on_press=self.card_selected,
                                        )
                    self.shuffled_indexes[index]["wid"] = wid  # needed later when restarting
                    card["wid"] = wid
                    self.cards[wid] = card
                    self.tableau[i].append(wid)
                    index += 1
                    
                if j < i:
                    # add the blank over the card unless last one.
                    self.ipg.add_column(window_id="main",
                                    container_id=f"tab_blank_{i}_{j}",
                                    parent_id=f"tab_stack_{i}",)
                
                    # Add a blank at top to hide the card below
                    self.ipg.add_space(parent_id=f"tab_blank_{i}_{j}",
                                        height=20*j)
                    cover = {}
                    cover["name"] = "tab_cover"
                    cover["index"] = index-1
                    cover["tab_column"] = i
                    cover["tab_index"] = j
                    cover["is_cover"] = True
                    cover["tableau"] = True
                    file = f"{self.path}/card_back.png"
                    wid = self.ipg.add_image(
                            parent_id=f"tab_blank_{i}_{j}", 
                            image_path=file,
                            width=self.card_width, 
                            height=self.card_height,
                            content_fit=IpgImageContentFit.Fill,
                            on_press=self.card_selected,
                            )
                    self.cards[wid] = cover
                    self.tab_cover_cards_wids.append(wid)

        # add cards left to stock
        self.stock = []
        for idx in range(index, len(self.shuffled_indexes)):
            card = self.shuffled_indexes[idx]
            file = f"{self.path}/{card.get('suite')}/{card.get('value')}.png"
            card["stock"] = True

            wid = self.ipg.add_image(parent_id="stack_stock_pile", 
                                image_path=file,
                                width=self.card_width, 
                                height=self.card_height,
                                content_fit=IpgImageContentFit.Fill,
                                mouse_pointer=IpgMousePointer.Grabbing,
                                on_press=self.card_selected,
                                )
            self.stock.append(wid)
            card["wid"] = wid
            self.cards[wid] = card
            
        # add a cover
        file = f"{self.path}/card_back.png"
        wid = self.ipg.add_image(parent_id=f"stack_stock_pile", 
                            image_path=file,
                            width=self.card_width, 
                            height=self.card_height,
                            content_fit=IpgImageContentFit.Fill,
                            mouse_pointer=IpgMousePointer.Grabbing,
                            on_press=self.card_selected,
                            )
        cover = {}
        cover["name"] = "stock_cover"
        cover["is_cover"] = True
        cover["stock"] = True
        cover["foundatiuon"] = False
        cover["waste"] = False
        cover["tableau"] = False
        cover["wid"] = wid
        self.stock_cover_id = wid
        self.cards[wid] = cover

    def card_selected(self, card_id: int):
        if self.origin is None:
            self.origin = card_id
            card = self.cards.get(card_id)
            if card.get("is_cover") and card.get("tableau"):
                # check to see that the turnover card is the last one
                if card.get("tab_index") < len(self.tableau[card.get("tab_column")])-1:
                    return
                self.turn_tab_cover_over()
                self.origin = None
                return
            elif card.get("is_cover") and card.get("stock") and card.get("reload"):
                self.reload_stock()
                self.origin = None
                return
            elif card.get("is_cover") and card.get("stock"):
                self.move_stock_to_waste()
                self.origin = None
                return
            elif card.get("stock") and card.get("stock"):
                self.origin = None
                return
            elif card.get("name") == "tab_mousearea":
                self.origin = None
                return
            
        elif self.target is None:
            self.target = card_id
        else:
            print(self.cards.get(self.origin))
            print(self.cards.get(self.target))
            raise Exception("origin and target are both not None")

        if self.origin is not None and self.target is not None:
            self.move_card()  
            self.ipg.update_item(self.status_id, IpgTextParam.Content, self.content)

    def move_card(self):
        ids = []
        if self.cards.get(self.origin).get("tableau") and self.cards.get(self.target).get("tableau"):
            ids = self.move_tab_to_tab()
        elif self.cards.get(self.origin).get("tableau") and self.cards.get(self.target).get("foundation"):
            ids = self.move_tab_to_foundation()
        elif self.cards.get(self.origin).get("waste") and self.cards.get(self.target).get("tableau"):
            ids = self.move_waste_to_tableau()
        elif self.cards.get(self.origin).get("waste") and self.cards.get(self.target).get("foundation"):
            ids = self.move_waste_to_foundation()
        elif self.cards.get(self.origin).get("stock") and self.cards.get(self.target).get("waste"):
            ids = self.move_stock_to_waste()
        elif self.cards.get(self.origin).get("waste") and self.cards.get(self.target).get("stock"):
            self.content = "Cannot move waste to stock"
            ids = None
        elif self.cards.get(self.origin).get("tableau") and self.cards.get(self.target).get("stock"):
            self.content = "Cannot move a card to stock"
            ids = None
        elif self.cards.get(self.origin).get("Stock") and self.cards.get(self.target).get("stock"):
            self.content = "Cannot move a card back to stock"
            ids = None
        
        if ids is not None:
            for wid, str_id in ids:
                self.ipg.move_widget(window_id="main",
                                    widget_id=wid,
                                    target_container_str_id=str_id,
                                    move_before=None,
                                    move_after=None
                                    )
        self.origin = None
        self.target = None
        
    def turn_tab_cover_over(self):
        # hide the cover card by moving it off screen
        self.ipg.move_widget(window_id="main",
                                widget_id=self.origin,
                                target_container_str_id="hidden"
                                )
           
    def move_tab_to_tab(self):
        origin = self.cards.get(self.origin)
        target = self.cards.get(self.target)
        
        if target.get("is_cover"):
            content = "You cannot move a card to a cover card"
            return None
        
        # if tab empty and card is a king then move
        if target.get("name") == "tab_mousearea" and origin.get("value") == 13:
            # ok adding king to empty slot
            pass
        else:
            if target.get("name") == "tabmousearea" and origin.get("value") != 13:
                self.content = "You cannot move a card to an empty space"
                return None
                
            if origin.get("color") == target.get("color"):
                self.content = "Origin and target card colors must not match"
                return None
            
            if origin.get("value") != target.get("value")-1:
                self.content = "The origin value must be one less than the target value"
                return None

            if target.get("tab_index") < len(self.tableau[target.get("tab_column")])-1:
                self.content = "The selected taget must be the last card in the column"
                return None
        
        # find the index of the selected card
        tab_card_ids = self.tableau[origin.get("tab_column")]
        origin_id = origin.get("wid")
        found = False
        ids_to_move = []
        for i, card_id in enumerate(tab_card_ids):
            if origin_id == card_id:
                found = True
            if found:
                ids_to_move.append(card_id)
        
        tar_container_id = []
        tab_index = target.get("tab_index")
        tar_tab_column = target.get("tab_column")
        origin_tab_column = origin.get("tab_column")
        
        for i, wid in enumerate(ids_to_move):
            card_to_move = self.cards.get(wid)
            
            tar_tab_index =  tab_index + i + 1 # add 1 since moved after
            tar_container_id.append((wid, f"tabcol_{tar_tab_column}_{tar_tab_index}"))
            
            # tableau index adjustments
            self.tableau[origin_tab_column].remove(wid)
            self.tableau[tar_tab_column].append(wid)
            
            # adjust the origin card indexes
            self.cards[wid]["tab_column"] = tar_tab_column
            self.cards[wid]["tab_index"] = tar_tab_index

        return tar_container_id
        
    def move_tab_to_foundation(self):
        target = self.cards.get(self.target)
        origin = self.cards.get(self.origin)
        fd_slot = target.get("fd_index")

        # if foundation empty and card is an ace then continue
        if target.get("value") == 0 and  origin.get("value") == 1:
            pass
        else:
            # check the value
            if target.get("value") != origin.get("value") - 1:
                self.content = f"You cannot move the card {origin.get('name')} with a value of {origin.get('value')} to the foundation slot {fd_slot}"
                return None
            
            if target.get("suite") != origin.get("suite"):
                self.content = f"You cannot move the card having a suite of {origin.get('suite')} to foundation slot {fd_slot}"
                return  None

        origin_id = origin.get("wid")
        tab_col = origin.get("tab_column")
        self.tableau[tab_col].remove(origin_id)
        self.cards[origin_id]["foundation"] = True
        self.cards[origin_id]["tableau"] = False
        self.cards[origin_id]["fd_index"] = fd_slot
        self.cards[origin_id]["tab_column"] = None
        self.cards[origin_id]["tab_index"] = None

        self.content = f"Card {origin.get('name')} was moved to foundation slot {fd_slot}"    
        return [(origin_id, f"foundation_{fd_slot}")]
    
    def move_waste_to_tableau(self):
        origin = self.cards.get(self.origin)
        target = self.cards.get(self.target)
        
        # if tab empty and card is a king then move
        if target.get("tab_index") == -1 and origin.get("value") == 13:
            pass
        else:
            if target.get("name") == "tab_mousearea" and origin.get("value") != 13:
                self.content = "Card cannot be move to an empty space"
                return None
            
            if origin.get("color") == target.get("color"):
                self.content = "Origin and target card colors must not match"
                return None
            
            if origin.get("value") != target.get("value")-1:
                self.content = "The origin value must be one less than the target value"
                return None
        
        tar_tab_column = target.get("tab_column")
        tar_tab_index = target.get("tab_index") + 1 # add 1 since moved after
        tar_container_id = f"tabcol_{tar_tab_column}_{tar_tab_index}"
        
        origin_id = origin.get("wid")
        
        # tableau ids adjustments
        self.tableau[tar_tab_column].append(origin_id)
        
        # adjust the origin card indexes
        self.cards[origin_id]["tab_column"] = tar_tab_column
        self.cards[origin_id]["tab_index"] = tar_tab_index
        self.cards[origin_id]["tableau"] = True
        self.cards[origin_id]["waste"] = None
        self.waste.remove(origin_id)

        return [(origin_id, tar_container_id)]
        
    def move_stock_to_waste(self):
        ids_to_move = []
        
        if len(self.stock) == 0:
            self.ipg.move_widget("main", self.stock_cover_id, "hidden")
            
        if self.cards_to_play == "3":
            if len(self.stock) >= 3:
                ids_to_move = self.stock[-3:] 
                self.stock = self.stock[0:len(self.stock)-3]
            elif len(self.stock) >= 2:
                ids_to_move = self.stock[-2:]
                self.stock = self.stock[0:len(self.stock)-2]
            elif len(self.stock) >= 1:
                ids_to_move = self.stock[-1:]
                self.stock = self.stock[0:len(self.stock)-1]
            else:
                return None
        else:
            if len(self.stock) >= 1:
                ids_to_move = self.stock[-1:]
                self.stock = self.stock[0:len(self.stock)-1]
            else:
                return None
            
        for wid in ids_to_move:
            self.cards.get(wid)["stock"] = False
            self.cards.get(wid)["waste"] = True
            self.ipg.move_widget(window_id="main",
                                widget_id=wid,
                                target_container_str_id="stack_waste_pile",
                                )
  
        self.waste.extend(ids_to_move)
        self.content = "Cards dealt"
        return None
            
    def reload_stock(self):
        # Move the ids back to the stock and reverse the order
        self.stock = self.waste
        self.waste = []
        self.stock.reverse()
        # move the cards back to stock
        for wid in self.stock:
            self.cards.get(wid)["stock"] = True
            self.cards.get(wid)["waste"] = False
            self.ipg.move_widget("main", wid, "stack_stock_pile")
        # Move the cover card on top
        self.ipg.move_widget("main", self.stock_cover_id, "stack_stock_pile")
        self.rounds += 1
        self.ipg.update_item(self.rounds_id, IpgTextParam.Content, f"Card Play Rounds: {self.rounds}")

    def move_waste_to_foundation(self):
        target = self.cards.get(self.target)
        origin = self.cards.get(self.origin)
        fd_slot = target.get("fd_index")

        # if foundation empty and card is an ace then continue
        if target.get("value") == 0 and  origin.get("value") == 1:
            None
        else:
            # check the value
            if target.get("value") != origin.get("value") - 1:
                self.content = f"You cannot move the card {origin.get('name')} with a value of {origin.get('value')} to the foundation slot {fd_slot}"
                return None
            
            if target.get("suite") != origin.get("suite"):
                self.content = f"You cannot move the card having a suite of {origin.get('suite')} to foundation slot {fd_slot}"
                return  None
            
        origin_id = origin.get("wid")
        self.cards[origin_id]["foundation"] = True
        self.cards[origin_id]["waste"] = False
        self.cards[origin_id]["fd_index"] = fd_slot
        self.waste.remove(origin_id)

        self.content = f"Card {origin.get('name')} was moved to foundation slot {fd_slot}"    
        return [(origin_id, f"foundation_{fd_slot}")]
        

game = solitaire()
game.start_game()

