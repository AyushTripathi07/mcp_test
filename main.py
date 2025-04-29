import os
import pymupdf
from typing import Any
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("doc_summarizer")

# 📄 Extract full text from a PDF
@mcp.tool()
def extract_pdf_text(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    text = "".join([page.get_text() for page in doc])
    return text.strip() or "No readable text found."

# 📸 Extract full text with OCR (for scanned/image-based docs)
@mcp.tool()
def extract_pdf_text_ocr(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    all_text = ""
    for page in doc:
        tp = page.get_textpage_ocr()
        text = page.get_text(textpage=tp)
        all_text += text
    return all_text.strip() or "No OCR text found."

# 📄 Extract text from a specific page
@mcp.tool()
def extract_pdf_page_text(file_path: str, page_num: int) -> str:
    doc = pymupdf.open(file_path)
    if page_num < 0 or page_num >= doc.page_count:
        return f"Invalid page number. PDF has {doc.page_count} pages."
    return doc[page_num].get_text().strip() or "No text found on this page."

# 🖼️ Extract all images from the PDF
@mcp.tool()
def extract_pdf_images(file_path: str, output_dir: str = "output_images") -> list[str]:
    doc = pymupdf.open(file_path)
    output = []
    os.makedirs(output_dir, exist_ok=True)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            pix = pymupdf.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            img_path = f"{output_dir}/page_{page_index + 1}_img_{img_index}.png"
            pix.save(img_path)
            output.append(img_path)
            pix = None
    return output if output else ["No images found in document."]

# 🧱 Extract vector graphics (drawings) from each page
@mcp.tool()
def extract_pdf_drawings(file_path: str) -> dict[int, list[dict[str, Any]]]:
    doc = pymupdf.open(file_path)
    drawing_data = {}
    for i, page in enumerate(doc):
        drawings = page.get_drawings()
        if drawings:
            drawing_data[i] = drawings
    return drawing_data or {"info": "No vector drawings found."}

# 📑 Extract metadata like title, author, etc.
@mcp.tool()
def get_pdf_metadata(file_path: str) -> dict[str, Any]:
    doc = pymupdf.open(file_path)
    metadata = doc.metadata
    metadata["page_count"] = doc.page_count
    return metadata

# 📚 Get PDF outline / bookmarks (like TOC)
@mcp.tool()
def get_pdf_outline(file_path: str) -> list[dict[str, Any]] | str:
    doc = pymupdf.open(file_path)
    toc = doc.get_toc()
    if not toc:
        return "No outline/bookmarks found."
    return [{"level": lvl, "title": title, "page": pg - 1} for lvl, title, pg in toc]

# 📊 Count pages
@mcp.tool()
def count_pdf_pages(file_path: str) -> int:
    return pymupdf.open(file_path).page_count

# 👀 Get first few lines (snippet)
@mcp.tool()
def get_pdf_snippet(file_path: str, lines: int = 10) -> str:
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text.splitlines()) >= lines:
            break
    snippet = "\n".join(text.splitlines()[:lines])
    return snippet.strip() or "No snippet available."


# 🏁 Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")