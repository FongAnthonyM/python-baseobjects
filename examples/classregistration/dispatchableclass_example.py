#!/usr/bin/env python
"""dispatchableclass_example.py
An example of how to create and use DispatchableClass.

This example demonstrates:
1. Creating a concrete implementation of DispatchableClass
2. Implementing the get_class_information method
3. Automatic dispatching to appropriate subclasses based on input
4. Using the class registry for dynamic class selection
5. Factory pattern implementation using DispatchableClass
"""

# Imports #
# Standard Libraries #
from typing import Any, ClassVar, Dict, Optional, Tuple, Type

# Source Packages #
from baseobjects.classregistration import BaseClassRegistry, DispatchableClass


# Definitions #
# Classes #
class SimpleClassRegistry(BaseClassRegistry):
    """A simple implementation of BaseClassRegistry.

    This registry uses class names as keys to store and retrieve classes. This class dictates how classes are registered
    and retrieved.
    """

    def register_class(self, cls: type, name: str | None = None, **kwargs: Any) -> None:
        """Registers a class with the given name.

        Args:
            cls: The class to register.
            name: The name to register the class under. If None, uses the class name.
            **kwargs: Additional keyword arguments (not used in this implementation).
        """
        if name is None:
            name = cls.__name__

        self[name] = cls

    def get_class(self, name: str, default: Any = None) -> type:
        """Gets a class from the registry by name.

        Args:
            name: The name of the class to retrieve.
            default: The default value to return if the class is not found.

        Returns:
            The requested class, or the default value if not found.
        """
        return self.get(name, default)


class FileHandler(DispatchableClass):
    """Base class for file handlers.

    This class demonstrates how to implement DispatchableClass. When instantiated with a filename, it automatically
    selects the appropriate subclass based on the file extension.
    """

    # Class Attributes #
    class_registry_type: ClassVar[type[BaseClassRegistry]] = SimpleClassRegistry
    class_registration: ClassVar[bool] = True

    # Class Methods #
    @classmethod
    def register_class(cls, name: str | None = None) -> None:
        """Register this class in the class registry.

        Args:
            name: The name to register the class under. If None, uses the class name.
        """
        if cls.class_registry is None:
            cls.create_class_registry()

        if name is None:
            name = cls.__name__

        cls.class_registry.register_class(cls, name=name)

    @classmethod
    def get_registered_class(cls, name: str) -> type["FileHandler"] | None:
        """Get a registered class by name.

        Args:
            name: The name of the class to retrieve.

        Returns:
            The requested class, or None if not found.
        """
        if cls.class_registry is None:
            return None

        return cls.class_registry.get_class(name)

    @classmethod
    def get_class_information(cls, filename: str, *args: Any, **kwargs: Any) -> tuple[str]:
        """Get the class information based on the filename.

        This method extracts the file extension from the filename and returns it as the key to look up the appropriate
        handler class.

        Args:
            filename: The name of the file to handle.
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            A tuple containing the file extension as the key for class lookup.
        """
        if "." in filename:
            extension = filename.split(".")[-1].lower()
            return (extension,)
        return ("txt",)  # Default to text handler if no extension

    # Instance Attributes #
    filename: str

    # Magic Methods #
    def __init__(self, filename: str, *args: Any, **kwargs: Any) -> None:
        """Initialize a file handler with a filename.

        Args:
            filename: The name of the file to handle.
            *args: Positional arguments which may be used by subclasses (not used).
            **kwargs: Keyword arguments which may be used by subclasses (not used).
        """
        self.filename = filename

    # Instance Methods #
    def read(self) -> str:
        """Read the file content.

        Returns:
            The content of the file as a string.
        """
        return f"Reading {self.filename} with generic handler"

    def write(self, content: str) -> None:
        """Write content to the file.

        Args:
            content: The content to write to the file.
        """
        print(f"Writing to {self.filename} with generic handler")


class TextFileHandler(FileHandler):
    """Handler for text files (.txt)."""

    def read(self) -> str:
        """Read the text file content.

        Returns:
            The content of the text file as a string.
        """
        return f"Reading text file {self.filename}"

    def write(self, content: str) -> None:
        """Write content to the text file.

        Args:
            content: The content to write to the text file.
        """
        print(f"Writing to text file {self.filename}")
        print(f"Content: {content}")


class CSVFileHandler(FileHandler):
    """Handler for CSV files (.csv)."""

    def read(self) -> str:
        """Read the CSV file content.

        Returns:
            The content of the CSV file as a string.
        """
        return f"Reading CSV file {self.filename} with comma delimiter"

    def write(self, content: str) -> None:
        """Write content to the CSV file.

        Args:
            content: The content to write to the CSV file.
        """
        print(f"Writing to CSV file {self.filename} with comma delimiter")
        print(f"Content: {content}")


class JSONFileHandler(FileHandler):
    """Handler for JSON files (.json)."""

    def read(self) -> str:
        """Read the JSON file content.

        Returns:
            The content of the JSON file as a string.
        """
        return f"Reading JSON file {self.filename} and parsing JSON structure"

    def write(self, content: str) -> None:
        """Write content to the JSON file.

        Args:
            content: The content to write to the JSON file.
        """
        print(f"Writing to JSON file {self.filename} with proper JSON formatting")
        print(f"Content: {content}")


class XMLFileHandler(FileHandler):
    """Handler for XML files (.xml)."""

    def read(self) -> str:
        """Read the XML file content.

        Returns:
            The content of the XML file as a string.
        """
        return f"Reading XML file {self.filename} and parsing XML structure"

    def write(self, content: str) -> None:
        """Write content to the XML file.

        Args:
            content: The content to write to the XML file.
        """
        print(f"Writing to XML file {self.filename} with proper XML formatting")
        print(f"Content: {content}")


class ImageFileHandler(FileHandler):
    """Handler for image files (.jpg, .png, .gif)."""

    def __init__(self, filename: str, image_format: str | None = None) -> None:
        """Initialize an image file handler with a filename and format.

        Args:
            filename: The name of the image file to handle.
            image_format: The format of the image (jpg, png, gif). If None, determined from filename.
        """
        super().__init__(filename)
        if image_format is None:
            if "." in filename:
                self.image_format = filename.split(".")[-1].lower()
            else:
                self.image_format = "unknown"
        else:
            self.image_format = image_format

    def read(self) -> str:
        """Read the image file content.

        Returns:
            A description of reading the image file.
        """
        return f"Reading {self.image_format} image file {self.filename}"

    def write(self, content: str) -> None:
        """Write content to the image file.

        Args:
            content: The content to write to the image file.
        """
        print(f"Writing to {self.image_format} image file {self.filename}")
        print(f"Content: {content}")


# Register the file handlers
FileHandler.class_registry = SimpleClassRegistry()
FileHandler.class_registration = True

# Register the handlers with their extensions
FileHandler.class_registry.register_class(TextFileHandler, name="txt")
FileHandler.class_registry.register_class(CSVFileHandler, name="csv")
FileHandler.class_registry.register_class(JSONFileHandler, name="json")
FileHandler.class_registry.register_class(XMLFileHandler, name="xml")
FileHandler.class_registry.register_class(ImageFileHandler, name="jpg")
FileHandler.class_registry.register_class(ImageFileHandler, name="png")
FileHandler.class_registry.register_class(ImageFileHandler, name="gif")


# Functions #
# Example Sections #
def basic_dispatching() -> None:
    """Demonstrates basic dispatching based on file extension."""
    print("Basic Dispatching:\n")

    # Create file handlers for different file types
    print("Creating file handlers for different file types...")

    files = [
        "document.txt",
        "data.csv",
        "config.json",
        "settings.xml",
        "photo.jpg",
        "logo.png",
        "animation.gif",
        "unknown_file",  # No extension
    ]

    for filename in files:
        # The FileHandler constructor will automatically dispatch to the appropriate subclass
        handler = FileHandler(filename)

        # Print the type of handler that was selected
        print(f"\nFile: {filename}")
        print(f"Handler type: {type(handler).__name__}")

        # Use the handler
        print(f"Reading result: {handler.read()}")
        handler.write("Sample content")

    print()


def manual_handler_selection() -> None:
    """Demonstrates manually selecting a handler class."""
    print("Manual Handler Selection:\n")

    # Get handler classes from the registry
    print("Getting handler classes from the registry...")

    txt_handler_class = FileHandler.class_registry.get_class("txt")
    csv_handler_class = FileHandler.class_registry.get_class("csv")
    json_handler_class = FileHandler.class_registry.get_class("json")

    # Create instances manually
    print("Creating instances manually...")

    txt_handler = txt_handler_class("manual_document.txt")
    csv_handler = csv_handler_class("manual_data.csv")
    json_handler = json_handler_class("manual_config.json")

    # Use the handlers
    print("\nUsing the manually created handlers:")

    print(f"\nText handler: {txt_handler.read()}")
    txt_handler.write("Manual text content")

    print(f"\nCSV handler: {csv_handler.read()}")
    csv_handler.write("Manual CSV content")

    print(f"\nJSON handler: {json_handler.read()}")
    json_handler.write("Manual JSON content")

    print()


def custom_dispatching_logic() -> None:
    """Demonstrates creating a subclass with custom dispatching logic."""
    print("Custom Dispatching Logic:\n")

    # Define a new file handler with custom dispatching logic
    class AdvancedFileHandler(FileHandler):
        """An advanced file handler with custom dispatching logic."""

        @classmethod
        def get_class_information(
            cls, filename: str, content_type: str | None = None, *args: Any, **kwargs: Any,
        ) -> tuple[str]:
            """Get the class information based on the filename and content type.

            This method uses the content_type parameter if provided, otherwise falls back
            to the file extension.

            Args:
                filename: The name of the file to handle.
                content_type: The type of content (txt, csv, json, xml, etc.).
                *args: Additional positional arguments (not used).
                **kwargs: Additional keyword arguments (not used).

            Returns:
                A tuple containing the content type or file extension as the key for class lookup.
            """
            if content_type is not None:
                return (content_type.lower(),)

            # Fall back to the parent class's logic
            return super().get_class_information(filename, *args, **kwargs)

    # Create instances with explicit content types
    print("Creating instances with explicit content types...")

    # These will use the content_type parameter for dispatching, not the file extension
    txt_handler = AdvancedFileHandler("data.bin", content_type="txt")
    csv_handler = AdvancedFileHandler("config.dat", content_type="csv")
    json_handler = AdvancedFileHandler("settings.cfg", content_type="json")

    # Print the type of handler that was selected
    print("\nFile: data.bin, Content Type: txt")
    print(f"Handler type: {type(txt_handler).__name__}")
    print(f"Reading result: {txt_handler.read()}")

    print("\nFile: config.dat, Content Type: csv")
    print(f"Handler type: {type(csv_handler).__name__}")
    print(f"Reading result: {csv_handler.read()}")

    print("\nFile: settings.cfg, Content Type: json")
    print(f"Handler type: {type(json_handler).__name__}")
    print(f"Reading result: {json_handler.read()}")

    # Now create an instance without a content type (will use file extension)
    print("\nCreating an instance without a content type (will use file extension)...")

    xml_handler = AdvancedFileHandler("data.xml")

    print("\nFile: data.xml")
    print(f"Handler type: {type(xml_handler).__name__}")
    print(f"Reading result: {xml_handler.read()}")

    print()


def file_processor_application() -> None:
    """Demonstrates a complete file processing application using DispatchableClass."""
    print("File Processor Application:\n")

    # Define a file processor that uses the file handlers
    class FileProcessor:
        """A file processor that can process multiple files."""

        def __init__(self) -> None:
            """Initialize a file processor."""
            self.results = {}

        def process_file(self, filename: str, content: str | None = None) -> str:
            """Process a file by reading or writing.

            Args:
                filename: The name of the file to process.
                content: The content to write to the file. If None, reads the file.

            Returns:
                The result of processing the file.
            """
            # Create a handler for the file (will automatically dispatch to the correct handler)
            handler = FileHandler(filename)

            if content is None:
                # Read mode
                result = handler.read()
                self.results[filename] = result
                return result
            else:
                # Write mode
                handler.write(content)
                self.results[filename] = f"Wrote to {filename}"
                return f"Wrote to {filename}"

        def process_files(self, files: dict[str, str | None]) -> dict[str, str]:
            """Process multiple files.

            Args:
                files: A dictionary mapping filenames to content. If content is None, reads the file.

            Returns:
                A dictionary mapping filenames to processing results.
            """
            for filename, content in files.items():
                self.process_file(filename, content)
            return self.results

        def get_results(self) -> dict[str, str]:
            """Get the results of processing files.

            Returns:
                A dictionary mapping filenames to processing results.
            """
            return self.results

    # Create a file processor
    print("Creating a file processor...")
    processor = FileProcessor()

    # Process some files
    print("Processing files...")
    files_to_process = {
        "readme.txt": None,  # Read mode
        "data.csv": "id,name,age\n1,John,30\n2,Jane,25",  # Write mode
        "config.json": '{"server": "localhost", "port": 8080}',  # Write mode
        "settings.xml": "<settings><theme>dark</theme></settings>",  # Write mode
        "logo.png": None,  # Read mode
    }

    results = processor.process_files(files_to_process)

    # Print the results
    print("\nProcessing results:")
    for filename, result in results.items():
        print(f"  - {filename}: {result}")

    print()


# Main #
if __name__ == "__main__":
    # Demonstrate basic dispatching
    basic_dispatching()

    # Demonstrate manual handler selection
    manual_handler_selection()

    # Demonstrate custom dispatching logic
    custom_dispatching_logic()

    # Demonstrate a complete file processor application
    file_processor_application()
