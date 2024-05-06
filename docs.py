from icedpygui import IPG, IpgMenuSepTypes, IpgMenuParams, IpgTextParams, IpgContainerAlignment
from collections import OrderedDict
import csv


ipg = IPG()


def load_docs(label):
    global doc_ids
    ipg.update_item(doc_ids[0], IpgTextParams.Content, value=label)
    ipg.update_item(doc_ids[1], IpgTextParams.Content, value="---------------")
    ipg.update_item(doc_ids[1], IpgTextParams.Show, value=True)
    i = 2
    with open('./resources/docs.csv', newline='') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            if line[0] == label:
               l = line[1].replace('\n', '')
               if l.find(":") == -1:
                   l = "    " + l
                   
               ipg.update_item(doc_ids[i], IpgTextParams.Content, value=l)
               ipg.update_item(doc_ids[i], IpgTextParams.Show, value=True)
               i += 1

    # Hide the unsused text widgets 
    for j in range(i-1, 50):
        ipg.update_item(doc_ids[j], IpgTextParams.Show, value=False)


def menu_pressed(menu_id, label):
        load_docs(label)

        

ipg.add_window("main", "Menu", 500, 600,  pos_x=100, pos_y=25)

ipg.add_container(window_id="main", container_id="menu_cont", width_fill=True, align_x=IpgContainerAlignment.Start)

ipg.add_container(window_id="main", container_id="cont", width_fill=True, height_fill=True)

ipg.add_scrollable(window_id="main", container_id="scroll", parent_id="cont", width_fill=True, height=600)

ipg.add_column("main", container_id="col_docs", parent_id="scroll", spacing=0)

items = OrderedDict({"A-C": ["Button", "Card", "Checkbox", "ColorPicker"],
                     "D-L": ["DatePicker", "Events KB", "Events MS", "Events WND", "Image"],
                     "M-S": ["PickList", "PG Bar", "Radio", "RuleHorizontal", "RuleVertical", 
                             "Selectable", "Slider", "Scrollable", "Space"],
                     "T-Z": ["Table", "Text", "TextInput", "Timer", "Toggler", "Window"]})

widths = [90.0]

spacing = [5.0]


# Finally, we add the menu.  The separators are optional parameters.
menu_id = ipg.add_menu("menu_cont", items, widths, spacing,
                       on_select=menu_pressed)

ipg.add_space(parent_id="col_docs", height=20.0)

doc_ids = []
for i in range(0, 50):
    show = False
    if i == 0:
        show = True
    doc_ids.append(ipg.add_text(parent_id="col_docs", content="Docs placed here", show=show))

ipg.start_session()






