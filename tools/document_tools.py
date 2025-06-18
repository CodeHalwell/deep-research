from ..utils.logging import setup_logger
logger = setup_logger("document_tools", level="DEBUG", log_file="document_tools.log")

class DocumentTools:
    """
    A class to handle document-related operations.
    """

    @staticmethod
    def template_engine(template: str, context: dict) -> str:
        """
        Renders a template string with the provided context.

        Args:
            template (str): The template string to render.
            context (dict): A dictionary containing the context for rendering.

        Returns:
            str: The rendered template string.
        """
        from jinja2 import Template

        jinja_template = Template(template)
        return jinja_template.render(context)
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads the content of a file.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            str: The content of the file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Writes content to a file.

        Args:
            file_path (str): The path to the file to write.
            content (str): The content to write to the file.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def append_to_file(file_path: str, content: str) -> None:
        """
        Appends content to a file.

        Args:
            file_path (str): The path to the file to append to.
            content (str): The content to append to the file.
        """
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)