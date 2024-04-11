from icedpygui import IPG
import random

ipg = IPG()

# Add the window
ipg.add_window(window_id="main", title="Table Demo", width=500, height=600,
               pos_centered=True)

# Add the container, since the table requires a width and height,
# the container can shrink(default) to fit.
ipg.add_container(window_id="main", container_id="cont")

# Initialize the lists.
col1 = []
col2 = []
col3 = []
col4 = []

# Add some random data of different types
for i in range(0, 50):
    # make a float random number
    col1.append(random.randrange(10, 99) + random.randrange(10, 99) / 100)
    col2.append(random.choice(["one", "two", "three", "four", "five", "six", "seven"]))
    col3.append(random.randrange(10, 99))
    col4.append(random.choice([True, False]))

# Create the table, the requirement is a list of dictionaries.
# Rust does not have dictionaries but a similar type is called a HashMap.
# The reason for the list of dictionaries is that you cannot extract a
# mixed dictionary into a Rust HashMap.  The HashMap has to have predefined
# types.  In this case they are <String, Vec<f64>>, <String, Vec<String>>,
# <String, Vec<i64>>, and <String, Vec<bool>>.  As one iterates through the list,
# each type is tested to see if it can be extracted in one of the types above.  If found,
# the extraction occurs and life is wonderful.  If no existing type is found, then an error occurs.
# Currently, not every variation is covered but that can be improved in future versions.
# This probably covers the vast majorities needs.  If you need that mixed column, convert
# the list to a string.  When the final version is displayed, it's converted to  a string anyway.
data = [{"Col1": col1},
        {"Col2": col2},
        {"Col3": col3},
        {"Col4": col4}]

# The table is added.
ipg.add_table("cont", "My Table", data, width=700.0, height=600.0)


# Required to be the last widget sent to Iced,  If you start the program
# and nothing happens, it might mean you forgot to add this command.
ipg.start_session()
