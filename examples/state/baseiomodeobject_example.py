#!/usr/bin/env python
"""baseiomodeobject_example.py
An example of how to use BaseIOModeObject and its decorators.

This example demonstrates:
1. Creating a subclass of BaseIOModeObject.
2. Using staterestriction to restrict access to methods based on open state and mode.
3. Using asopen to ensure a method is called when the object is open.
4. Using asopenasync for asynchronous methods.
"""

# Imports #
# Standard Libraries #
import asyncio
from enum import StrEnum
from io import UnsupportedOperation
from typing import Any, Self

# Source Packages #
from baseobjects.state import BaseIOModeObject, asopen, asopenasync, staterestriction


# Classes #
class ExampleModes(StrEnum):
    """The modes for the example object."""

    READ = "r"
    WRITE = "w"
    APPEND = "a"


class ExampleIOObject(BaseIOModeObject):
    """An example object that has an I/O mode.

    Attributes:
        _valid_modes: The valid modes for this object.
        data: The data of the object.
    """

    # Attributes #
    _valid_modes: type[StrEnum] = ExampleModes
    data: str = ""

    # Magic Methods #
    # Construction/Destruction #
    def __init__(self, mode: ExampleModes | str = ExampleModes.READ, *args: Any, **kwargs: Any) -> None:
        """Initializes the example object.

        Args:
            mode: The I/O mode of the object.
            *args: Positional arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        super().__init__(*args, **kwargs)
        self._mode = ExampleModes(mode)

    # Instance Methods #
    # State Management #
    def open(self, *args: Any, **kwargs: Any) -> Self:
        """Opens the object.

        Args:
            *args: Positional arguments for opening.
            **kwargs: Keyword arguments for opening.

        Returns:
            This object.
        """
        print(f"Opening in mode: {self._mode}")
        return super().open(*args, **kwargs)

    async def open_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously opens the object.

        Args:
            *args: Positional arguments for opening.
            **kwargs: Keyword arguments for opening.

        Returns:
            This object.
        """
        print(f"Asynchronously opening in mode: {self._mode}")
        self._is_open = True
        return self

    def close(self) -> None:
        """Closes the object."""
        print("Closing the object.")
        super().close()

    async def close_async(self) -> None:
        """Asynchronously closes the object."""
        print("Asynchronously closing the object.")
        self._is_open = False

    # Data Operations #
    @staterestriction(open_state=True, valid_modes=ExampleModes.READ)  # type: ignore[arg-type]
    def read(self) -> str:
        """Reads the data.

        Returns:
            The data.
        """
        return self.data

    @staterestriction(open_state=True, valid_modes={"w", "a"})  # type: ignore[arg-type]
    def write(self, value: str) -> None:
        """Writes the data.

        Args:
            value: The data to write.
        """
        if self._mode == ExampleModes.WRITE:
            self.data = value
        else:
            self.data += value

    @staterestriction(open_state=True, valid_modes=True)  # type: ignore[arg-type]
    def general_info(self) -> str:
        """Returns general info about the object, allowed in any mode.

        Returns:
            General info string.
        """
        return f"Object in mode {self._mode} with data length {len(self.data)}"

    @asopen()  # type: ignore[arg-type]
    def process_data(self) -> None:
        """Processes the data within an as_open context.

        This method will automatically open the object if it is closed, and close it after completion if it opened it.
        """
        print(f"Processing data: {self.data}")

    @asopenasync()  # type: ignore[arg-type]
    async def process_data_async(self) -> None:
        """Asynchronously processes the data within an as_open_async context.

        This method will automatically open the object if it is closed, and close it after completion if it opened it.
        """
        print(f"Asynchronously processing data: {self.data}")


# Example Sections #
def staterestriction_example() -> None:
    """Demonstrates how to use staterestriction."""
    print("\n--- staterestriction Example ---")
    obj = ExampleIOObject(mode=ExampleModes.READ)

    print("Attempting to read from a closed object:")
    try:
        obj.read()
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("\nOpening the object and reading:")
    with obj:
        print(f"Data: {obj.read()!r}")

    print("\nAttempting to write when in READ mode:")
    with obj:
        try:
            obj.write("new data")
        except UnsupportedOperation as e:
            print(f"Caught expected error: {e}")

    obj.mode = ExampleModes.WRITE
    print(f"\nChanged mode to: {obj.mode}")
    with obj:
        obj.write("Hello, World!")
        print(f"Data after write (via attribute): {obj.data!r}")
        try:
            obj.read()
        except UnsupportedOperation as e:
            print(f"Caught expected error when reading in WRITE mode: {e}")

    print("\nDemonstrating valid_modes=True (allowed in any mode):")
    obj.mode = ExampleModes.READ
    with obj:
        print(f"READ mode: {obj.general_info()}")

    obj.mode = ExampleModes.WRITE
    with obj:
        print(f"WRITE mode: {obj.general_info()}")


def asopen_example() -> None:
    """Demonstrates how to use asopen."""
    print("\n--- asopen Example ---")
    obj = ExampleIOObject(mode=ExampleModes.WRITE)
    obj.data = "Initial Data"

    print("Calling process_data (it will auto-open and auto-close):")
    obj.process_data()
    print(f"Is object open? {obj.is_open}")

    print("\nCalling process_data when already open:")
    with obj:
        obj.process_data()
        print(f"Is object open? {obj.is_open}")
    print(f"Is object open after context? {obj.is_open}")


async def asopenasync_example() -> None:
    """Demonstrates how to use asopenasync."""
    print("\n--- asopenasync Example ---")
    obj = ExampleIOObject(mode=ExampleModes.WRITE)
    obj.data = "Async Data"

    print("Calling process_data_async (it will auto-open and auto-close):")
    await obj.process_data_async()  # type: ignore[operator]
    print(f"Is object open? {obj.is_open}")

    print("\nCalling process_data_async when already open:")
    async with obj:
        await obj.process_data_async()  # type: ignore[operator]
        print(f"Is object open? {obj.is_open}")
    print(f"Is object open after context? {obj.is_open}")


async def main_async() -> None:
    """Runs asynchronous examples."""
    await asopenasync_example()


def main() -> None:
    """Runs all examples."""
    staterestriction_example()
    asopen_example()
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
