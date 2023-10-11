from pytui import Window, Text
from pytui_extra import Table

# create 80x40 window at 0,0
window = Window(0, 0, 80, 40)

# create table with 3 columns: 2x 4 char wide on the right, with the remainder on the left
table = Table(window, [None, 4, 4])

# right-justify the right columns
table.set_column_format(1, {'justify': 'right'})
table.set_column_format(2, {'justify': 'right'})

# update table with data - slice operators are useful for 'paging'
table.update([
    ['Food', Text('2.4').style({'bg': 0xff0000}), 10],  # apply style to individual cell
    ['Textiles', 5.8, 18],
    ['Radioactives', 17.9, 25],
    table.highlight_row(['Luxuries', 98.1, 2]),         # highlight row
    ['Computers', 67.2, 7],
    ['Machinery', 45.8, 8],
])

# draw table window
table.draw()
