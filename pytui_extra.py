from pytui import Window, Text


class Table:
    DEFAULT_FORMAT = {
        'justify': 'left',
        'justify_character': '.'
    }

    striped = True
    row_color = 0x000000
    alt_row_color = 0x2c2c2c
    highlight_color = 0x808080

    def __init__(self, container: Window, widths) -> None:
        self.column_formats = [self.DEFAULT_FORMAT.copy() for x in widths]
        self.columns = container.vsplit(*widths)[:len(widths)]  # ignore any left over

    def set_column_format(self, column: int, format: dict) -> None:
        self.column_formats[column].update(format)

    def format_cell(self, value: str, format: dict, column: Window) -> str:
        char = format['justify_character']
        pad = (column.width - len(Text(value).strip_ansi())) * char
        if 'left' == format['justify']:
            return value + pad
        elif 'right' == format['justify']:
            return pad + value
        else:
            return pad[:len(pad)//2] + value + pad[len(pad)//2:]

    def style_row(self, row: list[str], text_style: dict = {}) -> list[str]:
        styled = []
        for column, style, value in zip(self.columns, self.column_formats, row):
            styled.append(Text(self.format_cell(str(value), style, column)).style(text_style))
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
        for column in self.columns:
            column.draw()
