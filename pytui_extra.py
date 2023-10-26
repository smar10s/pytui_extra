from typing import Callable, Optional
from pytui import Window, Text, Terminal, Keyboard


class Table:
    DEFAULT_FORMAT = {
        'justify': 'left',
        'justify_character': ' '
    }

    def __init__(
        self,
        container: Window,
        widths,
        header: Optional[list[str]] = None,
        header_style={'bold': True},
        header_format={'justify': 'center'},
    ) -> None:
        self.striped = True
        self.row_color = 0x000000
        self.alt_row_color = 0x2c2c2c
        self.highlight_color = 0x808080
        self.draw_header = False

        if header:
            row, container = container.hsplit(1)
            self.draw_header = True
            self.header_columns = row.vsplit(*widths)[:len(widths)]  # ignore any left over
            for value, column in zip(header, self.header_columns):
                column.append_line(Text(self.format_cell(value, header_format, column)).style(header_style))

        self.columns = container.vsplit(*widths)[:len(widths)]  # ignore any left over
        self.column_formats = [self.DEFAULT_FORMAT.copy() for x in widths]

    def set_column_format(self, column: int, format: dict) -> None:
        self.column_formats[column].update(format)

    def format_cell(self, value: str, format: dict, column: Window) -> str:
        char = format['justify_character'] if 'justify_character' in format else ' '
        pad = (column.width - len(Text(value).strip_ansi())) * char
        if 'left' == format['justify']:
            return value + pad
        elif 'right' == format['justify']:
            return pad + value
        else:
            return pad[:len(pad)//2] + value + pad[len(pad)//2:]

    def style_row(self, row: list[str], style: dict = {}) -> list[str]:
        styled = []
        for column, format, value in zip(self.columns, self.column_formats, row):
            styled.append(Text(self.format_cell(str(value), format, column)).style(style))
        return styled

    def highlight_row(self, row: list[str]) -> list[str]:
        return self.style_row(row, {'bg': self.highlight_color})

    def update(self, rows: list) -> None:
        self.clear()
        for i, row in enumerate(rows):
            if self.striped:
                row = self.style_row(row, {'bg': self.alt_row_color if i % 2 else self.row_color})
            for column, format, value in zip(self.columns, self.column_formats, row):
                column.append_line(self.format_cell(str(value), format, column))

    def clear(self) -> None:
        for column in self.columns:
            column.clear()

    def draw(self) -> None:
        if self.draw_header:
            for column in self.header_columns:
                column.draw()
            self.draw_header = False    # draw header once only since it does not change
        for column in self.columns:
            column.draw()


class InputPrompt:
    """An input prompt using a Window and Keyboard.

    Characters typed are echoed back in the window, scrolling as necessary.

    Tabs and enter are not echoed, instead a callback handler is called with
    the current buffer as argument.
    """

    def __init__(
        self,
        window: Window,
        keyboard: Keyboard,
        on_enter: Callable[[str, list[str]], None],
        on_tab: Callable[[str, list[str]], None] = None,
        prefix: str = '# ',
        cursor: str = Text('_').style({'blink': True})
    ) -> None:
        """Creates a new input prompt for a given window and keyboard.

        Args:
            window: The window that will render the prompt and anything typed.
            keyboard: A keyboard instance to capture input.
            on_enter: A callback invoked with the current buffer on enter.
            on_tab: A callback invoked with the current buffer on tab.
            prefix: The prefix shown before any input. May be styled.
            cursor: The cursor shown. May be styled.
        """
        self.buffer = ''
        self.window = window
        self.keyboard = keyboard
        self.on_tab = on_tab
        self.on_enter = on_enter
        self.prefix = prefix
        self.cursor = cursor
        self.terminal = Terminal()

    def listener(self, key: str) -> None:
        if key == Keyboard.BACKSPACE:
            self.buffer = self.buffer[:-1]
        elif key == Keyboard.TAB:
            if self.on_tab:
                self.on_tab(self.buffer, self.buffer.split())
        elif key == Keyboard.ENTER:
            self.on_enter(self.buffer, self.buffer.split())
            self.buffer = ''
        else:
            self.buffer += key
        self.refresh()

    def refresh(self) -> None:
        (terminal, window) = (self.terminal, self.window)
        (prefix, buffer, cursor) = (self.prefix, self.buffer, self.cursor)
        window.clear()
        for line in Text(prefix + buffer + cursor).wrap(window.width):
            window.append_line(line)
        window.draw()
        terminal.flush()

    def listen(self) -> None:
        """Start listening for input."""
        self.terminal.hide_cursor()
        self.keyboard.listen(self.listener)
        self.refresh()
