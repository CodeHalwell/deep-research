import gradio as gr
import os
import json
from datetime import datetime
from pathlib import Path
from jinja2 import Template

from dotenv import load_dotenv
from utils.logging import setup_logger

load_dotenv()
logger = setup_logger("document_server", level="DEBUG", log_file="document_server.log")


# Citation formatting templates
CITATION_FORMATS = {
    "apa": "{author} ({year}). {title}. {source}.",
    "mla": "{author}. \"{title}.\" {source}, {year}.",
    "chicago": "{author}. {title}. {source}, {year}.",
}


async def format_citation(
    author: str,
    title: str,
    source: str,
    year: str,
    style: str = "apa",
) -> str:
    """
    Format a citation in the specified style.

    Args:
        author: Citation author(s)
        title: Citation title
        source: Publication source
        year: Publication year
        style: Citation style (apa, mla, chicago)

    Returns:
        Formatted citation string
    """
    try:
        template_str = CITATION_FORMATS.get(style.lower(), CITATION_FORMATS["apa"])
        template = Template(template_str)
        result = template.render(
            author=author,
            title=title,
            source=source,
            year=year,
        )
        logger.info(f"Citation formatted in {style} style")
        return result
    except Exception as e:
        logger.error(f"Error formatting citation: {str(e)}")
        return f"Error: {str(e)}"


async def validate_document(content: str) -> dict:
    """
    Validate document content and provide quality metrics.

    Args:
        content: Document content to validate

    Returns:
        Dictionary with validation results
    """
    try:
        metrics = {
            "word_count": len(content.split()),
            "char_count": len(content),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "has_headings": "##" in content or "#" in content,
            "has_lists": "-" in content or "*" in content,
            "is_valid": True,
            "issues": [],
        }

        # Check for common issues
        if metrics["word_count"] < 100:
            metrics["issues"].append("Document is very short (< 100 words)")

        if not metrics["has_headings"]:
            metrics["issues"].append("No headings detected")

        if metrics["paragraph_count"] < 2:
            metrics["issues"].append("Document has very few paragraphs")

        metrics["is_valid"] = len(metrics["issues"]) == 0

        logger.info(f"Document validated: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error validating document: {str(e)}")
        return {"error": str(e), "is_valid": False}


async def generate_toc(content: str) -> str:
    """
    Generate a table of contents from document headings.

    Args:
        content: Document content

    Returns:
        Table of contents in markdown format
    """
    try:
        lines = content.split('\n')
        toc_items = []

        for line in lines:
            if line.startswith('##'):
                level = 2
                title = line.replace('#', '').strip()
                indent = "  " * (level - 1)
                toc_items.append(f"{indent}- {title}")
            elif line.startswith('#'):
                level = 1
                title = line.replace('#', '').strip()
                indent = "  " * (level - 1)
                toc_items.append(f"{indent}- {title}")

        if not toc_items:
            return "No headings found in document"

        toc = "# Table of Contents\n\n" + "\n".join(toc_items)
        logger.info(f"TOC generated with {len(toc_items)} items")
        return toc
    except Exception as e:
        logger.error(f"Error generating TOC: {str(e)}")
        return f"Error: {str(e)}"


async def format_as_html(
    title: str,
    content: str,
    style: str = "professional",
) -> str:
    """
    Convert markdown content to HTML.

    Args:
        title: Document title
        content: Markdown content
        style: HTML style template (professional, minimal, academic)

    Returns:
        HTML string
    """
    try:
        # Simple markdown to HTML conversion
        html_content = content
        html_content = html_content.replace('\n\n', '</p><p>')
        html_content = html_content.replace('**', '<strong>', 1).replace('**', '</strong>')
        html_content = html_content.replace('*', '<em>', 1).replace('*', '</em>')

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        strong {{ font-weight: bold; }}
        em {{ font-style: italic; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>{html_content}</p>
</body>
</html>"""

        logger.info(f"Document converted to HTML")
        return html
    except Exception as e:
        logger.error(f"Error converting to HTML: {str(e)}")
        return f"Error: {str(e)}"


async def extract_metadata(content: str) -> dict:
    """
    Extract metadata from document content.

    Args:
        content: Document content

    Returns:
        Dictionary with extracted metadata
    """
    try:
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "word_count": len(content.split()),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "sentence_count": len([s for s in content.split('.') if s.strip()]),
            "avg_words_per_paragraph": 0,
        }

        if metadata["paragraph_count"] > 0:
            metadata["avg_words_per_paragraph"] = (
                metadata["word_count"] / metadata["paragraph_count"]
            )

        logger.info(f"Metadata extracted: {metadata}")
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        return {"error": str(e)}


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Document Processing Tools (MCP Server)

        This is a Gradio MCP server providing document processing tools:
        - Citation formatting (APA, MLA, Chicago)
        - Document validation
        - Table of contents generation
        - HTML conversion
        - Metadata extraction
        """
    )
    gr.api(
        format_citation,
        validate_document,
        generate_toc,
        format_as_html,
        extract_metadata,
    )


def start_server():
    demo.launch(
        mcp_server=True,
        server_name=os.getenv("SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("DOCUMENT_SERVER_PORT", 7861)),
    )


if __name__ == "__main__":
    start_server()

