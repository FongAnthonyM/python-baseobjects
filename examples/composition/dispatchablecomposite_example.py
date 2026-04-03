#!/usr/bin/env python
"""dispatchablecomposite_example.py
An example of how to create and use DispatchableComposite.

This example demonstrates:
1. Creating a concrete implementation of DispatchableComposite
2. Implementing both class dispatching and component dispatching
3. Automatic selection of the appropriate subclass based on input
4. Dynamic component creation based on parameters
5. Combining class and component dispatching in a single object
6. Factory pattern implementation with composite structure
"""
from __future__ import annotations

# Standard Libraries #
# Imports #
from typing import Any, ClassVar

# Source Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.composition import BaseComponent, DispatchableComposite


# Definitions #
# Classes #
# Component Classes
class DataSource(BaseComponent):
    """A component that provides data from various sources."""

    def get_data(self) -> Any:
        """Gets data from the source.

        Returns:
            The data from the source.
        """
        return "Base data source"


class FileDataSource(DataSource):
    """A component that provides data from a file."""

    def __init__(self, composite: Any = None, file_path: str = "data.txt") -> None:
        """Initializes a file data source.

        Args:
            composite: The composite object this component belongs to.
            file_path: The path to the file to read data from.
        """
        super().__init__(composite=composite)
        self.file_path = file_path

    def get_data(self) -> Any:
        """Gets data from the file.

        Returns:
            The data from the file.
        """
        return f"Data from file: {self.file_path}"


class DatabaseDataSource(DataSource):
    """A component that provides data from a database."""

    def __init__(self, composite: Any = None, connection_string: str = "localhost:5432") -> None:
        """Initializes a database data source.

        Args:
            composite: The composite object this component belongs to.
            connection_string: The database connection string.
        """
        super().__init__(composite=composite)
        self.connection_string = connection_string

    def get_data(self) -> Any:
        """Gets data from the database.

        Returns:
            The data from the database.
        """
        return f"Data from database: {self.connection_string}"


class APIDataSource(DataSource):
    """A component that provides data from an API."""

    def __init__(self, composite: Any = None, api_url: str = "https://api.example.com") -> None:
        """Initializes an API data source.

        Args:
            composite: The composite object this component belongs to.
            api_url: The URL of the API.
        """
        super().__init__(composite=composite)
        self.api_url = api_url

    def get_data(self) -> Any:
        """Gets data from the API.

        Returns:
            The data from the API.
        """
        return f"Data from API: {self.api_url}"


class DataProcessor(BaseComponent):
    """A component that processes data."""

    def process_data(self, data: Any) -> Any:
        """Processes the data.

        Args:
            data: The data to process.

        Returns:
            The processed data.
        """
        return f"Processed: {data}"


class FilterProcessor(DataProcessor):
    """A component that filters data."""

    def __init__(self, composite: Any = None, filter_criteria: str = "default") -> None:
        """Initializes a filter processor.

        Args:
            composite: The composite object this component belongs to.
            filter_criteria: The criteria to filter by.
        """
        super().__init__(composite=composite)
        self.filter_criteria = filter_criteria

    def process_data(self, data: Any) -> Any:
        """Filter the data.

        Args:
            data: The data to filter.

        Returns:
            The filtered data.
        """
        return f"Filtered by {self.filter_criteria}: {data}"


class TransformProcessor(DataProcessor):
    """A component that transforms data."""

    def __init__(self, composite: Any = None, transform_type: str = "default") -> None:
        """Initializes a transform processor.

        Args:
            composite: The composite object this component belongs to.
            transform_type: The type of transformation to apply.
        """
        super().__init__(composite=composite)
        self.transform_type = transform_type

    def process_data(self, data: Any) -> Any:
        """Transform the data.

        Args:
            data: The data to transform.

        Returns:
            The transformed data.
        """
        return f"Transformed with {self.transform_type}: {data}"


class AggregateProcessor(DataProcessor):
    """A component that aggregates data."""

    def __init__(self, composite: Any = None, aggregation_method: str = "sum") -> None:
        """Initializes an aggregate processor.

        Args:
            composite: The composite object this component belongs to.
            aggregation_method: The method to aggregate by.
        """
        super().__init__(composite=composite)
        self.aggregation_method = aggregation_method

    def process_data(self, data: Any) -> Any:
        """Aggregate the data.

        Args:
            data: The data to aggregate.

        Returns:
            The aggregated data.
        """
        return f"Aggregated with {self.aggregation_method}: {data}"


class DataOutput(BaseComponent):
    """A component that outputs data."""

    def output_data(self, data: Any) -> None:
        """Output the data.

        Args:
            data: The data to output.
        """
        print(f"Output: {data}")


class ConsoleOutput(DataOutput):
    """A component that outputs data to the console."""

    def __init__(self, composite: Any = None, format_type: str = "plain") -> None:
        """Initializes a console output.

        Args:
            composite: The composite object this component belongs to.
            format_type: The format to output in.
        """
        super().__init__(composite=composite)
        self.format_type = format_type

    def output_data(self, data: Any) -> None:
        """Output the data to the console.

        Args:
            data: The data to output.
        """
        print(f"Console output ({self.format_type}): {data}")


class FileOutput(DataOutput):
    """A component that outputs data to a file."""

    def __init__(self, composite: Any = None, file_path: str = "output.txt") -> None:
        """Initializes a file output.

        Args:
            composite: The composite object this component belongs to.
            file_path: The path to the file to write data to.
        """
        super().__init__(composite=composite)
        self.file_path = file_path

    def output_data(self, data: Any) -> None:
        """Output the data to a file.

        Args:
            data: The data to output.
        """
        print(f"File output to {self.file_path}: {data}")


class EmailOutput(DataOutput):
    """A component that outputs data via email."""

    def __init__(self, composite: Any = None, email_address: str = "user@example.com") -> None:
        """Initializes an email output.

        Args:
            composite: The composite object this component belongs to.
            email_address: The email address to send data to.
        """
        super().__init__(composite=composite)
        self.email_address = email_address

    def output_data(self, data: Any) -> None:
        """Output the data via email.

        Args:
            data: The data to output.
        """
        print(f"Email output to {self.email_address}: {data}")


# Composite Classes
class DataPipeline(DispatchableComposite):
    """A base class for data processing pipelines.

    This class demonstrates the DispatchableComposite functionality by combining both class dispatching
    (to select the appropriate pipeline type) and component dispatching (to create the right components).

    Class Attributes:
        component_types_registry: Registry of available component types.

    Attributes:
        data_source: The data source component.
        processor: The data processor component.
        output: The data output component.
    """

    # Class Attributes #
    class_registry_type: ClassVar[type[NamespaceClassRegistry]] = NamespaceClassRegistry
    class_registration: ClassVar[bool] = True
    default_component_types: ClassVar[dict[str, tuple[type[BaseComponent], dict[str, Any]]]] = {
        "data_source": (FileDataSource, {}),
        "processor": (FilterProcessor, {}),
        "output": (ConsoleOutput, {}),
    }

    # Class Methods #
    @classmethod
    def register_class(cls, name: str | None = None, namespace: str | None = None) -> None:
        """Registers this class in the class registry.

        Args:
            name: The name to register the class under. If None, uses the class name.
            namespace: The namespace to register the class under. If None, uses 'pipeline'.
        """
        if cls.class_registry is None:
            cls.create_class_registry()

        assert cls.class_registry is not None
        if name is None:
            name = cls.__name__

        if namespace is None:
            namespace = "pipeline"

        cls.class_registry.register_class(cls, namespace=namespace, name=name)

    @classmethod
    def get_registered_class(cls, namespace: str, name: str) -> type[DataPipeline] | None:
        """Gets a registered class by namespace and name.

        Args:
            namespace: The namespace of the class to retrieve.
            name: The name of the class to retrieve.

        Returns:
            The requested class, or None if not found.
        """
        if cls.class_registry is None:
            return None

        result = cls.class_registry.get_class(namespace, name)
        assert result is None or isinstance(result, type)
        return result

    @classmethod
    def get_class_information(cls, pipeline_type: str | None = None, *args: Any, **kwargs: Any) -> tuple[str, str]:  # type: ignore[override]
        """Gets the class information based on the pipeline type.

        Args:
            pipeline_type: The type of pipeline to create. If None, returns the base class.
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            A tuple containing the namespace and name for class lookup.
        """
        if pipeline_type is None:
            # If no pipeline_type is specified, return information that will resolve to the base class
            return ("pipeline", "DataPipeline")
        return ("pipeline", pipeline_type)

    # Attributes #
    component_types_registry: NamespaceClassRegistry = NamespaceClassRegistry()

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Construct this object.

        Args:
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            **kwargs: Additional keyword arguments.
        """
        component_types = self.dispatch_component_types(**kwargs)

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def dispatch_component_types(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, tuple[type[BaseComponent], dict[str, Any]]]:
        """Dispatch component types using the given arguments.

        This method determines which component types to instantiate based on the provided arguments.

        Args:
            *args: Positional arguments to use in dispatching.
            **kwargs: Keyword arguments to use in dispatching.

        Returns:
            A dictionary of component names, their types, and their keyword arguments.
        """
        # Starts with an empty dictionary for components
        components: dict[str, tuple[type[BaseComponent], dict[str, Any]]] = {}

        # Determine data source component
        if "source_type" in kwargs:
            source_type = kwargs.get("source_type")
            if source_type == "file":
                components["data_source"] = (FileDataSource, {"file_path": kwargs.get("file_path", "data.txt")})
            elif source_type == "database":
                components["data_source"] = (
                    DatabaseDataSource,
                    {"connection_string": kwargs.get("connection_string", "localhost:5432")},
                )
            elif source_type == "api":
                components["data_source"] = (
                    APIDataSource,
                    {"api_url": kwargs.get("api_url", "https://api.example.com")},
                )

        # Determine processor component
        if "processor_type" in kwargs:
            processor_type = kwargs.get("processor_type")
            if processor_type == "filter":
                components["processor"] = (
                    FilterProcessor,
                    {"filter_criteria": kwargs.get("filter_criteria", "default")},
                )
            elif processor_type == "transform":
                components["processor"] = (
                    TransformProcessor,
                    {"transform_type": kwargs.get("transform_type", "default")},
                )
            elif processor_type == "aggregate":
                components["processor"] = (
                    AggregateProcessor,
                    {"aggregation_method": kwargs.get("aggregation_method", "sum")},
                )

        # Determine output component
        if "output_type" in kwargs:
            output_type = kwargs.get("output_type")
            if output_type == "console":
                components["output"] = (ConsoleOutput, {"format_type": kwargs.get("format_type", "plain")})
            elif output_type == "file":
                components["output"] = (FileOutput, {"file_path": kwargs.get("output_file", "output.txt")})
            elif output_type == "email":
                components["output"] = (EmailOutput, {"email_address": kwargs.get("email_address", "user@example.com")})

        # Override default_component_types with our dispatched components
        # This ensures that our dispatched components take precedence over defaults
        return components

    def process(self) -> None:
        """Processes data through the pipeline.

        This method gets data from the data source, processes it, and outputs the result.
        """
        # Gets data from the source
        data = self.components["data_source"].get_data()

        # Processes the data
        processed_data = self.components["processor"].process_data(data)

        # Output the processed data
        self.components["output"].output_data(processed_data)


class ETLPipeline(DataPipeline):
    """A pipeline for Extract, Transform, Load operations."""

    def process(self) -> None:
        """Processes data through the ETL pipeline.

        This method extracts data from the source, transforms it, and loads it to the output.
        """
        print("Running ETL Pipeline:")

        # Extract data from the source
        print("Extracting data...")
        data = self.components["data_source"].get_data()

        # Transform the data
        print("Transforming data...")
        processed_data = self.components["processor"].process_data(data)

        # Loads the processed data
        print("Loading data...")
        self.components["output"].output_data(processed_data)
        print()


class ReportingPipeline(DataPipeline):
    """A pipeline for generating reports."""

    def process(self) -> None:
        """Processes data through the reporting pipeline.

        This method retrieves data, formats it for reporting, and outputs the report.
        """
        print("Running Reporting Pipeline:")

        # Retrieve data
        print("Retrieving data...")
        data = self.components["data_source"].get_data()

        # Formats for reporting
        print("Formatting report...")
        report = self.components["processor"].process_data(data)

        # Output the report
        print("Generating report...")
        self.components["output"].output_data(report)
        print()


class AnalyticsPipeline(DataPipeline):
    """A pipeline for data analytics."""

    def process(self) -> None:
        """Processes data through the analytics pipeline.

        This method collects data, analyzes it, and outputs the insights.
        """
        print("Running Analytics Pipeline:")

        # Collect data
        print("Collecting data...")
        data = self.components["data_source"].get_data()

        # Analyze data
        print("Analyzing data...")
        insights = self.components["processor"].process_data(data)

        # Output insights
        print("Outputting insights...")
        self.components["output"].output_data(insights)
        print()


# Registers component classes
DataPipeline.component_types_registry.register_class(FileDataSource, namespace="source", name="FileDataSource")
DataPipeline.component_types_registry.register_class(DatabaseDataSource, namespace="source", name="DatabaseDataSource")
DataPipeline.component_types_registry.register_class(APIDataSource, namespace="source", name="APIDataSource")

DataPipeline.component_types_registry.register_class(FilterProcessor, namespace="processor", name="FilterProcessor")
DataPipeline.component_types_registry.register_class(
    TransformProcessor,
    namespace="processor",
    name="TransformProcessor",
)
DataPipeline.component_types_registry.register_class(
    AggregateProcessor,
    namespace="processor",
    name="AggregateProcessor",
)

DataPipeline.component_types_registry.register_class(ConsoleOutput, namespace="output", name="ConsoleOutput")
DataPipeline.component_types_registry.register_class(FileOutput, namespace="output", name="FileOutput")
DataPipeline.component_types_registry.register_class(EmailOutput, namespace="output", name="EmailOutput")


# Functions #
# Example Sections #
def basic_dispatchable_composite_usage() -> None:
    """Demonstrates basic usage of DispatchableComposite."""
    print("Basic DispatchableComposite Usage:\n")

    # Creates a basic data pipeline with default components
    print("Creating a basic data pipeline with default components...")
    pipeline = DataPipeline()

    print("Components in the pipeline:")
    for name, component in pipeline.components.items():
        print(f"  - {name}: {type(component).__name__}")

    # Processes data through the pipeline
    print("\nProcessing data through the pipeline:")
    pipeline.process()
    print()


def class_dispatching() -> None:
    """Demonstrates class dispatching based on pipeline type."""
    print("Class Dispatching Based on Pipeline Type:\n")

    # Creates different types of pipelines
    print("Creating different types of pipelines...")

    # The pipeline_type parameter will be used to dispatch to the appropriate subclass
    etl_pipeline = DataPipeline(pipeline_type="ETLPipeline")
    reporting_pipeline = DataPipeline(pipeline_type="ReportingPipeline")
    analytics_pipeline = DataPipeline(pipeline_type="AnalyticsPipeline")

    # Verifies the types of the created pipelines
    print(f"ETL Pipeline type: {type(etl_pipeline).__name__}")
    print(f"Reporting Pipeline type: {type(reporting_pipeline).__name__}")
    print(f"Analytics Pipeline type: {type(analytics_pipeline).__name__}")

    # Processes data through each pipeline
    print("\nProcessing data through each pipeline:")
    etl_pipeline.process()
    reporting_pipeline.process()
    analytics_pipeline.process()


def component_dispatching() -> None:
    """Demonstrates component dispatching based on parameters."""
    print("Component Dispatching Based on Parameters:\n")

    # Creates a pipeline with specific component types
    print("Creating a pipeline with specific component types...")
    pipeline = DataPipeline(
        source_type="database",
        connection_string="mysql://user:pass@localhost/db",
        processor_type="transform",
        transform_type="json_to_csv",
        output_type="file",
        output_file="report.csv",
    )

    print("Components in the pipeline:")
    for name, component in pipeline.components.items():
        print(f"  - {name}: {type(component).__name__}")
        if name == "data_source" and isinstance(component, DatabaseDataSource):
            print(f"    - Connection String: {component.connection_string}")
        elif name == "processor" and isinstance(component, TransformProcessor):
            print(f"    - Transform Type: {component.transform_type}")
        elif name == "output" and isinstance(component, FileOutput):
            print(f"    - Output File: {component.file_path}")

    # Processes data through the pipeline
    print("\nProcessing data through the pipeline:")
    pipeline.process()
    print()


def combined_dispatching() -> None:
    """Demonstrates combined class and component dispatching."""
    print("Combined Class and Component Dispatching:\n")

    # Creates different types of pipelines with specific components
    print("Creating different types of pipelines with specific components...")

    # ETL Pipeline with database source, transform processor, and file output
    etl_pipeline = DataPipeline(
        pipeline_type="ETLPipeline",
        source_type="database",
        connection_string="postgres://user:pass@localhost/etl_db",
        processor_type="transform",
        transform_type="normalize",
        output_type="file",
        output_file="etl_output.csv",
    )

    # Reporting Pipeline with API source, aggregate processor, and email output
    reporting_pipeline = DataPipeline(
        pipeline_type="ReportingPipeline",
        source_type="api",
        api_url="https://api.example.com/reports",
        processor_type="aggregate",
        aggregation_method="average",
        output_type="email",
        email_address="reports@example.com",
    )

    # Analytics Pipeline with file source, filter processor, and console output
    analytics_pipeline = DataPipeline(
        pipeline_type="AnalyticsPipeline",
        source_type="file",
        file_path="analytics_data.json",
        processor_type="filter",
        filter_criteria="last_30_days",
        output_type="console",
        format_type="json",
    )

    # Processes data through each pipeline
    print("\nProcessing data through the ETL pipeline:")
    etl_pipeline.process()

    print("\nProcessing data through the Reporting pipeline:")
    reporting_pipeline.process()

    print("\nProcessing data through the Analytics pipeline:")
    analytics_pipeline.process()


def custom_pipeline_creation() -> None:
    """Demonstrates creating a custom pipeline with manual component creation."""
    print("Custom Pipeline Creation:\n")

    # Creates a custom ETL pipeline
    print("Creating a custom ETL pipeline...")
    custom_pipeline = ETLPipeline()

    # Manually create and add components
    print("Manually creating and adding components...")

    # Creates a custom data source
    custom_source = APIDataSource(api_url="https://custom-api.example.com/data")
    custom_pipeline.add_component("data_source", custom_source)

    # Creates a custom processor
    custom_processor = TransformProcessor(transform_type="custom_transform")
    custom_pipeline.add_component("processor", custom_processor)

    # Creates a custom output
    custom_output = EmailOutput(email_address="custom@example.com")
    custom_pipeline.add_component("output", custom_output)

    print("Components in the custom pipeline:")
    for name, component in custom_pipeline.components.items():
        print(f"  - {name}: {type(component).__name__}")
        if name == "data_source" and isinstance(component, APIDataSource):
            print(f"    - API URL: {component.api_url}")
        elif name == "processor" and isinstance(component, TransformProcessor):
            print(f"    - Transform Type: {component.transform_type}")
        elif name == "output" and isinstance(component, EmailOutput):
            print(f"    - Email Address: {component.email_address}")

    # Processes data through the custom pipeline
    print("\nProcessing data through the custom pipeline:")
    custom_pipeline.process()
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of DispatchableComposite
    basic_dispatchable_composite_usage()

    # Class dispatching based on pipeline type
    class_dispatching()

    # Component dispatching based on parameters
    component_dispatching()

    # Combined class and component dispatching
    combined_dispatching()

    # Custom pipeline creation
    custom_pipeline_creation()
