from pytui import Window, Text
from pytui_extra import Table


# create 40x10 window at top left
window = Window(0, 0, 40, 10)

# create a table with three columns: two 6 char wide on the right, with the remainder on the left
table = Table(
    window,
    [None, 6, 6],

    # include optional header
    header=['Items', 'Price', 'Count'],
    header_style={'bg': 0x232D51, 'fg': 0xA2AADD, 'bold': True},

    # change default styles
    row_style={'bg': 0x1B1E2D, 'fg': 0xA2AADD},
    alt_row_style={'bg': 0x181A28, 'fg': 0xA2AADD},
    highlight_style={'bg': 0x232D51, 'fg': 0xA2AADD},
)

# right-justify the right columns
table.set_column_format(1, {'justify': 'right'})
table.set_column_format(2, {'justify': 'right'})

# update table with data - slice operators are useful for 'paging'
table.update([
    ['Food', Text('2.4').style({'fg': 0xff0000}), 10],  # apply style to individual cell
    ['Textiles', 5.8, 18],
    ['Radioactives', 17.9, 25],
    table.highlight_row(['Luxuries', '98.1', '2']),         # highlight row
    ['Computers', 67.2, 7],
    ['Machinery', 45.8, 8],
])

# draw table
table.draw()
