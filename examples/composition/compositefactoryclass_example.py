#!/usr/bin/env python
"""compositefactoryclass_example.py
Example demonstrating the usage of CompositeFactoryClass.

This module provides examples for creating a factory-like structure where subclasses act as presets
for a head class, returning an instance of the head class configured with specific components.
"""
from __future__ import annotations

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from typing import Any, ClassVar

# Source Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.composition import BaseComponent, CompositeFactoryClass


# Definitions #
# Components #
class DataSource(BaseComponent):
    """A base component for data sources."""
    def get_data(self) -> str:
        """Gets data from the source.

        Returns:
            The data from the source.
        """
        return "Generic data"


class CSVDataSource(DataSource):
    """A component for CSV data sources."""
    def get_data(self) -> str:
        """Gets data from the CSV source.

        Returns:
            The data from the CSV source.
        """
        return "CSV data: id,name,value"


class JSONDataSource(DataSource):
    """A component for JSON data sources."""
    def get_data(self) -> str:
        """Gets data from the JSON source.

        Returns:
            The data from the JSON source.
        """
        return '{"id": 1, "name": "JSON", "value": 100}'


class DataProcessor(BaseComponent):
    """A base component for data processing."""
    def process(self, data: str) -> str:
        """Processes the data.

        Returns:
            The processed data.
        """
        return f"Processed {data}"


# Factories #
class DataFactory(CompositeFactoryClass):
    """The head class for data factories."""

    # Class Attributes #
    class_registration: ClassVar[bool] = True  # Start registration, making this the head class.

    # Instance Methods #
    def run(self) -> str:
        """Executes the data pipeline.

        Returns:
            The output of the data pipeline.
        """
        source = self.components["source"]
        assert isinstance(source, DataSource)
        data = source.get_data()

        processor = self.components["processor"]
        assert isinstance(processor, DataProcessor)
        return processor.process(data)


class CSVFactory(DataFactory):
    """A preset for a CSV data factory.

    Instantiating CSVFactory returns an instance of DataFactory configured with CSV components.
    """

    # Attributes #
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "source": (CSVDataSource, {}),
        "processor": (DataProcessor, {}),
    }


class JSONFactory(DataFactory):
    """A preset for a JSON data factory.

    Instantiating JSONFactory returns an instance of DataFactory configured with JSON components.
    """

    # Attributes #
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "source": (JSONDataSource, {}),
        "processor": (DataProcessor, {}),
    }


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrates simple reverse-dispatching behavior."""
    print(f"\nBasic Usage: Reverse Dispatching\n{'-' * 72}")

    # Instantiate the presets
    csv_factory = CSVFactory()
    json_factory = JSONFactory()

    # Even though we called CSVFactory and JSONFactory, the returned instances are of DataFactory
    print(f"Type of csv_factory: {type(csv_factory).__name__}")
    print(f"Type of json_factory: {type(json_factory).__name__}")

    # Each instance is configured with different components
    print(f"CSV Factory source: {type(csv_factory.components['source']).__name__}")
    print(f"JSON Factory source: {type(json_factory.components['source']).__name__}")

    # Run the factories
    print(f"CSV run output: {csv_factory.run()}")
    print(f"JSON run output: {json_factory.run()}")

    # Simple verification
    assert type(csv_factory) is DataFactory
    assert isinstance(csv_factory.components["source"], CSVDataSource)
    assert type(json_factory) is DataFactory
    assert isinstance(json_factory.components["source"], JSONDataSource)


def advanced_usage_example() -> None:
    """Demonstrates runtime component overrides and custom get_component_information."""
    print(f"\nAdvanced Usage: Runtime Overrides\n{'-' * 72}")

    # We can override the preset's components during instantiation
    # Here we use JSONFactory but override the source with CSVDataSource
    custom_factory = JSONFactory(
        component_types={"source": (CSVDataSource, {})}
    )

    print(f"Custom Factory source: {type(custom_factory.components['source']).__name__}")
    print(f"Custom Factory output: {custom_factory.run()}")

    # We can also instantiate the head class directly
    direct_factory = DataFactory(
        component_types={
            "source": (DataSource, {}),
            "processor": (DataProcessor, {}),
        }
    )
    print(f"Direct Factory output: {direct_factory.run()}")

    # Verification
    assert type(custom_factory) is DataFactory
    assert isinstance(custom_factory.components["source"], CSVDataSource)
    assert isinstance(custom_factory.components["processor"], DataProcessor)


def dynamic_component_example() -> None:
    """Demonstrates overriding build_head_class for dynamic components."""
    print(f"\nDynamic Usage: Overriding build_head_class\n{'-' * 72}")

    class DynamicFactory(DataFactory):
        """A factory that chooses its source based on an argument."""
        class_registration: ClassVar[bool] = True

        @classmethod
        def build_head_class(
            cls,
            head_class: type[CompositeFactoryClass],
            *args: Any,
            source_type: str = "csv",
            **kwargs: Any
        ) -> CompositeFactoryClass:
            """Builds the head class with dynamic component selection."""
            source: tuple[type[DataSource], dict[str, Any]]
            if source_type == "json":
                source = (JSONDataSource, {})
            else:
                source = (CSVDataSource, {})

            component_types = kwargs.pop("component_types", {})
            component_types.setdefault("source", source)
            component_types.setdefault("processor", (DataProcessor, {}))

            return super().build_head_class(head_class, *args, component_types=component_types, **kwargs)

    # Use the dynamic factory
    csv_dynamic = DynamicFactory(source_type="csv")
    json_dynamic = DynamicFactory(source_type="json")

    print(f"CSV Dynamic output: {csv_dynamic.run()}")
    print(f"JSON Dynamic output: {json_dynamic.run()}")

    assert isinstance(csv_dynamic.components["source"], CSVDataSource)
    assert isinstance(json_dynamic.components["source"], JSONDataSource)


def hierarchy_example() -> None:
    """Demonstrates how the head class is determined in a hierarchy."""
    print(f"\nHierarchy Usage: Head Class Determination\n{'-' * 72}")

    # DataFactory is the head class because it's the direct subclass of CompositeFactoryClass
    registry = DataFactory.class_registry
    assert registry is not None
    print(f"DataFactory is head class: {registry.head_class is DataFactory}")

    # CSVFactory is not a head class; it belongs to DataFactory's registry
    # NamespaceClassRegistry stores classes by namespace and name
    registered_class = registry.get_class(
        namespace=CSVFactory.__module__,
        name=CSVFactory.__name__,
    )
    print(f"CSVFactory found in DataFactory registry: {registered_class is CSVFactory}")

    # We can create a new factory hierarchy by subclassing CompositeFactoryClass again
    class AnotherFactory(CompositeFactoryClass):
        class_registration: ClassVar[bool] = True

    class AnotherPreset(AnotherFactory):
        default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
            "source": (DataSource, {}),
        }

    another_instance = AnotherPreset()
    print(f"Type of AnotherPreset instance: {type(another_instance).__name__}")
    assert type(another_instance) is AnotherFactory


def build_head_class_override_example() -> None:
    """Demonstrates extending build_head_class to override head class attributes."""
    print(f"\nOverride Usage: Extending build_head_class\n{'-' * 72}")

    class ExtendedDataFactory(DataFactory):
        """A head class that has an additional 'description' attribute."""
        class_registration: ClassVar[bool] = True
        class_registry: ClassVar[NamespaceClassRegistry | None] = None  # Reset registry to start a new hierarchy.

        def __init__(self, *args: Any, description: str = "Generic description", **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.description = description

    class DescribedCSVFactory(ExtendedDataFactory):
        """A preset that overrides the head class's 'description' attribute."""
        default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
            "source": (CSVDataSource, {}),
            "processor": (DataProcessor, {}),
        }

        @classmethod
        def build_head_class(
            cls,
            head_class: type[CompositeFactoryClass],
            *args: Any,
            **kwargs: Any,
        ) -> CompositeFactoryClass:
            """Builds the head class and overrides the description.

            Args:
                head_class: The head class of the hierarchy.
                *args: Positional arguments for initialization.
                **kwargs: Keyword arguments for initialization.

            Returns:
                CompositeFactoryClass: The built head class.
            """
            # We can provide a default description for this preset
            kwargs.setdefault("description", "This is a CSV factory preset.")

            # We then call the super method to finish building the head class
            return super().build_head_class(head_class, *args, **kwargs)

    # Use the preset
    csv_factory = DescribedCSVFactory()
    assert isinstance(csv_factory, ExtendedDataFactory)

    print(f"Factory type: {type(csv_factory).__name__}")
    print(f"Factory description: {csv_factory.description}")
    print(f"Factory output: {csv_factory.run()}")

    assert type(csv_factory) is ExtendedDataFactory
    assert csv_factory.description == "This is a CSV factory preset."

    # We can still override the description at runtime
    custom_factory = DescribedCSVFactory(description="A very special CSV factory.")
    assert isinstance(custom_factory, ExtendedDataFactory)
    print(f"Custom description: {custom_factory.description}")
    assert custom_factory.description == "A very special CSV factory."


def init_attributes_example() -> None:
    """Demonstrates the automatically gathered init attributes."""
    print(f"\nInit Attributes Usage: Introspection\n{'-' * 72}")

    class ParametricFactory(DataFactory):
        """A factory with specific init parameters."""
        def __init__(self, arg1: Any, kwarg1: str = "default", **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.arg1 = arg1
            self.kwarg1 = kwarg1

    print(f"Init Parameters: {list(ParametricFactory.init_parameters.keys())}")
    print(f"Init Args: {ParametricFactory.init_args}")
    print(f"Init Defaults: {ParametricFactory.init_defaults}")

    assert "arg1" in ParametricFactory.init_parameters
    assert "kwarg1" in ParametricFactory.init_parameters
    assert ParametricFactory.init_args == ("self", "arg1", "kwarg1")
    assert ParametricFactory.init_defaults == {"kwarg1": "default"}


# Main #
if __name__ == "__main__":  # pragma: no cover
    basic_usage_example()
    advanced_usage_example()
    dynamic_component_example()
    hierarchy_example()
    build_head_class_override_example()
    init_attributes_example()
