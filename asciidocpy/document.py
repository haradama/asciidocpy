from abc import ABC, abstractmethod


class DocumentElement(ABC):
    @abstractmethod
    def render(self):
        """
        Render the document element to an AsciiDoc string.
        """
        pass


class Section(DocumentElement):
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.content = []

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        prefix = "=" * self.level
        rendered_content = [f"{prefix} {self.title}"] + \
            [item.render() for item in self.content]
        return "\n".join(rendered_content)


class Paragraph(DocumentElement):
    def __init__(self, text):
        self.text = text

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        return self.text


class UnorderedList(DocumentElement):
    def __init__(self, items):
        self.items = items

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        return "\n".join([f"* {item}" for item in self.items])


class OrderedList(DocumentElement):
    def __init__(self, items):
        self.items = items

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        return "\n".join([f". {item}" for item in self.items])


class Table(DocumentElement):
    def __init__(self, header, rows):
        self.header = header
        self.rows = rows

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        header_part = "|===\n| " + \
            " | ".join(self.header) + "\n" if self.header else "|===\n"
        body = "\n".join("| " + " | ".join(map(str, row)) for row in self.rows)
        return header_part + body + "\n|==="


class Image(DocumentElement):
    def __init__(self, src, alt_text, title=None,
                 width=None, height=None, align=None):
        self.src = src
        self.alt_text = alt_text
        self.title = title
        self.width = width
        self.height = height
        self.align = align

    def render(self):
        options = []
        if self.title:
            options.append(f"title=\"{self.title}\"")
        if self.width:
            options.append(f"width={self.width}")
        if self.height:
            options.append(f"height={self.height}")
        if self.align:
            options.append(f"align={self.align}")

        options_str = ",".join(options)
        image_line = f"image::{self.src}[{self.alt_text}"
        if options_str:
            image_line += f", {options_str}"
        image_line += "]"
        return image_line


class Blockquote(DocumentElement):
    def __init__(self, text, author=None, source=None):
        self.text = text
        self.author = author
        self.source = source

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        quote = f"____\n{self.text}\n____"
        if self.author or self.source:
            attrib_line = f"[quote, {self.author}, {self.source}]"
            quote = attrib_line + "\n" + quote
        return quote


class HorizontalLine(DocumentElement):
    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        return "----"


class Reference(DocumentElement):
    def __init__(self, key, authors, title, publisher, year):
        self.key = key
        self.authors = authors
        self.title = title
        self.publisher = publisher
        self.year = year

    def __str__(self) -> str:
        return self.render()

    def render(self) -> str:
        return f"- [[[{self.key}]]] {self.authors}. {self.title}. {self.publisher}. {self.year}."


class Document(DocumentElement):
    def __init__(self):
        self.content = []

    def __str__(self) -> str:
        return self.render()

    def add_section(self, title, level=1) -> Section:
        section = Section(title, level)
        self.content.append(section)
        return section

    def render(self) -> str:
        return "\n".join([item.render() for item in self.content])
