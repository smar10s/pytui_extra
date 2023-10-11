pytui extras
============

Additional TUI related things based on [pytui](https://github.com/smar10s/pytui) that I found useful in other projects.

### Install:
Either get `pytui_extra.py` and use module directly, or clone and install with pip, e.g.:

```
git clone https://github.com/smar10s/pytui_extra/
pip install pytui_extra/
```

### Use:

#### Table

A basic table that divides a window into columns using `Window.vsplit` and provides convenience methods for updating and formatting content.

The constructor expects a window to use, followed by an array of column sizes in the same format as `Window.vsplit`: integers are absolute characters, floats are ratios of window size, and `None` represents remaining space ('auto'). 

For example, given a window 10 characters wide:
- `[None, 4, 4]` will create 3 columns sized 2, 4, 4
- `[None, None]` will create 2 columns sized 5, 5
- `[4, 4]` will create 2 columns sized 4, 4 and ignore the remainder
- `[0.2, None, 1]` will create 3 columns sized 2, 7, 1

Columns are striped by default. Set `striped = False` to disable. Set `row_color` and `alt_row_color` to change column background colors.

Data in columns is left justified using `.` as the padding character. This can be changed on a per-column level using `set_column_format`.

Rows can be styled individually using `style_row`. This accepts a list of strings and a `Text.style` compatible dictionary to apply. Values are also justified with the same style applied to the justify character.

`highlight_row` is a convenience method that uses `style_row` to apply a `highlight_color` background. This color can be changed.

Example:

```
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
```
![table](docs/images/table.png)
