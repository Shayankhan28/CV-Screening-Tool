from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


def iter_block_items(document):
    """
    Document ke body ko UPAR SE NEECHE, jis order mein Word file mein likha hai
    usi order mein iterate karta hai - paragraphs aur tables dono.

    Normal python-docx sirf document.paragraphs deta hai, jo tables ko
    IGNORE kar deta hai. Ye function tables ko bhi cover karta hai.
    """
    parent_elm = document.element.body
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def extract_table_text(table):
    """Table ke har row ko ' | ' se joint text mein convert karta hai."""
    rows_text = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        rows_text.append(" | ".join(cells))
    return "\n".join(rows_text)


def extract_text_from_docs(file_path):
    try:
        doc = Document(file_path)
        all_text = ""

        for block in iter_block_items(doc):
            if isinstance(block, Paragraph):
                all_text = all_text + block.text + "\n"
            elif isinstance(block, Table):
                all_text = all_text + extract_table_text(block) + "\n"

        return all_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""


# if __name__ == "__main__":
#     result = extract_text_from_docs("src/data/sample_cvs/report.docx")
#     print(result)