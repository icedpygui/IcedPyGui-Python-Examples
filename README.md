# IcedPyGui (IPG)
Python wrapper for Rust Iced Gui

<div align="center">
   
   # Iced + Python == IcedPyGui (IPG)

https://github.com/icedpygui/IcedPyGui-Python-Examples/assets/163431522/ae248470-82ee-4260-a63e-2f80af2593ee

</div>

## Releases/Revisions
* Upcoming release 0.2.0 estimated to be July 30
* Iced has undergone significant changes since 0.12.0 release, so a lot of changes along with adding styling.

## Features

* Supported Iced widgets
    * Button 
    * Checkbox 
    * Canvas - next release
    * ColorPalette - next release
    * Column - container
    * ComboBox - Needs modification to work in IPG, but PicKList good substitute
    * Container - container
    * Events - keyboard, mouse, timer, and window
    * Fonts - Future
    * Image
    * Modal
    * MouseArea
    * Overlays - next release
    * PaneGrid - Future
    * PickList 
    * ProgressBar
    * QRCodes - next release
    * Radio buttons - mutiple, grouped in one line of code
    * Row - container
    * Rule
    * Scrollable - container (modified in IPG) 
    * Slider
    * Shader - future
    * Space
    * Stack - next release
    * Styling - Some widget styling, more to come
    * SVG
    * TextEditor - Future, needs modification to work in IPG
    * TextInput
    * Text
    * Toggler
    * Tooltip - Only widget now, container ability future
    * Windows multiple
* Iced_aw widgets
    * Card
    * ColorPicker - future
    * Menu
* IPG widgets
    * DatePicker - compact and resizable
    * SelectableText - all mouse buttons supported
    * Table - Currently simple, easily loaded with a list of dictionaries, supports adding widgets button, checkbox, image, and svg.

* Python issues to be addressed
    * Need to incorporate using with statement in python.  Using with would allow one to not have to supply the window or parent id if those follow closely.  For example:
    ``` python
        with window(...):
            with container(...):
                add_widget(...)
    ```
    * @dataclass needs to be supported (support soon)

## Installation (PiPy)
* Code not published to PiPy yet.  Download one of the wheels attached to the [release page](https://github.com/icedpygui/IcedPyGui-Python-Examples/releases) or see below for installation via rust
* Open one of the example using your favorite IDE.
* Create and activate a virtual environment
 ```python
pip install --force-reinstall path to wheel
 ```

## Installation (Rust)

See the Rust code at [IcedPyGui](https://github.com/icedpygui/IcedPyGui).

## Overview
* IcedPyGui is based on [Rust Iced](https://github.com/iced-rs/iced) v0.12.1.
* Widgets for [Iced_aw](https://github.com/iced-rs/iced_aw) v0.8.0 are used too .
* [Pyo3](https://github.com/pyo3/pyo3) is used as the python wrapper.
* [Maturin](https://github.com/PyO3/maturin) is used to build and publish the module .
* The syntax and the design of the callbacks were inspired by the python wrapper of Dear ImGui, [DearPyGui(DPG)](https://github.com/hoffstadt/DearPyGui).
* The icon above was a merge of Python and Iced icons by [Deep Dream Generator](https://deepdreamgenerator.com)


## Intro
IcedPyGui is based on Iced which is written in Rust.  I think Rust is a great language but has a fairly steep learning curve.  Therefore putting rust and python together seems like a good fit.  You get the speed and code security of rust and the simplicity of python.

Iced is a great GUI for Rust but it's still early in the development cycle, more good things will follow and these will be incorprated as Iced grows.    

Some would probably say it's too early for a python wrap but I though I would give it a try since I wanted a project that would help me improve my Rust skills, which I've only been using a for a short time.

This project is the first I have published and so I expect I'll learn a lot and hopefully you can bare with me.

Rust's strict typing is mostly shielded from the python user but if you venture too far, you'll get burned with an error, so behave yourselves :)

Iced doesn't use the concept of user data being passed around but when using DearPyGui, sometimes the ability to send user data was very helpful.  Therefore, this concept was added to IPG.

The user data is special because it is only passed through to rust and  back out as a PyObject or PyAny.  Therefore any python data can be used since it is never extracted into a rust type.    

# A few important rules or points and then you program with IPG!
   
* Import IPG as indicated below in the demo code and any parameter class needed for the widgets.

* Instantiate the Rust structure then add your containers and widgets.

* The last line of code to execute must be ipg.start_seesion().  Any code after that will not be executed because Iced is now running.  You can place it anywhere, just make sure its last executed.  If you start your program and nothing happens, it might mean that you aren't executing start_session() or you forgot to add it in, been there, done that.    

* Every widget needs to have a parent container previously defined and every container needs to have a window and optionally a parent container defined.  If the container is placed into a window then no parent_id is required.

* Therefore at least one window needs to be added first and at least one container needs to be added to the window before any widgets are added.  As long as you have defined a parent, you can add a widget.

#### Let's get started with out first prrogram:

Further below you'll find the full code to be tested in your IDE.  Sometimes the these code snippets don't paste properly into the IDE if the parameter names are in them.  But since these snippets are for learning, they need to be there for better understanding.  So look further down for the full code to copy and paste.

First we import IPG from icedpygui.  This is a Rust  structure to be instantiated.
We will be using a container and a column, these have alignment parameters so we need to import the parameter classes so that we don't have to type in strings which result in irritating typos.  We'll also be updating a text widget to show some results, therefore the text parameter class is needed.

```python
from icedpygui import IPG
from icedpygui import IpgContainerAlignment, IpgColumnAlignment, IpgTextParams
```

Let's instantiate the Rust structure and add some containers.  Since this is a short program, we'll dispense with using a class.  See the examples for cases where we used a class but nothing special pertains to IPG when they are used, except for a @dataclass which will be supported in the near future.

```python
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
```

So, the window was added using a window_id, title, size and position, followed by a container and column.  The ids are a key part of IPG and can be consider the glue that holds everything together.  Each time there is a add command, a corresponding structure is initialized and stored in a Mutex using a HashMap with an integer id.  Once Iced is started, a recursive routine is called to create the nested tree for all of the containers and widgets which is used by Iced to display them.  Therefore, widgets can only be added during the add or construct phase.  This might seem restrictive but if you have a widget that you need later, just add it with the show parameter as false.  When the time comes for it's use, just change the parameter show to true and you now have it.  You can modify all of the widgets during a callback procedure where the command update_item() is used. You will see this in the demo code below. 

Note how the ids are used.  A container must have a window_id because Iced is a multi-window GUI, we need to know which window to put it in.  In addition, if a container goes into another container, then the parent_id is needed.

A quick word on width_fill parameter.  Almost all containers and widgets have a width and height.  The parameter width and height take a float number.  The width_fill and height_fill is bool and overrides the float.  The fill parameters will cause the width of the container or widget to fill the avalable space.  This works pretty good in most cases but there are some cases where there is a conflict as you'll see in some of the examples. 

The column was added because the container holds only one widget and we need a container that holds more.  We could have not used a container but only a column but then we would need to add spaces to get the column centered horizontally since a column only centers vertically.  So the container made it easier.

To make things a little bit more exciting, let's add 3 widgets to the column container.

### Adding widgets

```rust
ipg.add_button(parent_id="col", label="Press Me!", on_press=button_pressed)

ipg.add_checkbox(parent_id="col", label="Check Me!!!", on_toggle=checked)

checked_text_id = ipg.add_text(parent_id="col",
                               content="This will change when I'm checked")

```

The button and checkbox widgets were next added and given a parent_id, which is the container_id that you want to put the widget in.  The callbacks are functions you want to execute when, for example, a button is pressed.  So in the case above, we have callback functions, button_pressed and checked.  Note, some IDE's automatically insert a () after a function name is typed in.  This will give you an error because these are references to the function and are not to be executed at this time.  So make sure the () is not present.

As you make have noted, widget don't get an id but are assigned an id during the construction of the Rust structure which returns an integer.  The text widget which was added last is an example where the id of the widget is needed for updating the text widget with some new content.

#### Defining callbacks:

Below we defined two callbacks, button_pressed and checked,  All callbacks have from 1 to 3 parameters based on the output of the widget.  The button has only one (2 if user_data used) and the checkbox has a minimum of 2, id and a bool to indicate if checked or not and a 3rd, if user_data used.  You can look at the docs to determine the returning values, but they are mostly obvious based on what the widget does.

```rust
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

```

The button is simple because it only returns the id of itself.  So in most cases, you'll be doing something else like processing some data or changing some other widget.  In this case, we'll just print out the id number.  

We have used the term btn_id above versus id because id is used by python and it's good to indicate what the id is coming from so that you can remember which id to use in your function, like in the checkbox callback.  You are not using the checkbox id but the text id.

Another note on naming the callback parameters.  They can be named anything, order is most important.

For the checkbox callback, we could just print the checked status but that really never happens in a real programs so let's display the info in a text widget by using the command update_item().

The update_item is going to be your goto function to change the way the gui looks and to process your data while Iced is running.  The update_item function takes 3 arguments, an integer id of the widget you want to update, the class name of the parameter you want to change, and the value you want to set it too.  Unless you are updating the calling widget, you'll need the id of the widget you want to update.  The class name is the same as the parameter name of the widget so you can look at the docs for which to select.

So in the checked function, we do an if else statement for the boolean and change the text accordingly.  The user_data is not covered here but the are many in the examples and they are straight forward to use.

Finally, we're ready to start the engine on the gui with one last line of code, the magic.

```rust

ipg.start_session()

```
Let's put it all together to cut down on the cutting a pasting.

```rust
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

```

Hopefully you were able to run the program successfully.  If not, try one of the examples and see if it will work.  All of the examples are run before publishing to make sure the code works.  Unlike standard functions, a GUI is a bit difficult to test since you are visually making sure it all goes as expected. 


## Issues / Questions / Feedback

Feedback/Discussions/Questions are welcomed! You can come chat in the [Discord server](https://discord.com/channels/1233081452447666270/1233085181448032458).

If you have errors not cleared up in questions in the Discord server, go to the [IcedPyGui](https://github.com/icedpygui/IcedPyGui/issues) click on the issues tab and create a new one.  Follow the template.
