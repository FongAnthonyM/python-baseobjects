#!/usr/bin/env python
"""baseregisteredclass_example.py
An example of how to create and use BaseRegisteredClass.

This example demonstrates:
1. Creating a concrete implementation of BaseRegisteredClass
2. Implementing the required abstract methods
3. Automatic registration of subclasses
4. Retrieving registered subclasses
5. Using the class registry for dispatching
"""


# Imports #
# Standard Libraries #
from typing import Any, ClassVar, Optional, Type

# Source Packages #
from baseobjects.classregistration import BaseClassRegistry, BaseRegisteredClass


# Definitions #
# Classes #
class SimpleClassRegistry(BaseClassRegistry):
    """A simple implementation of BaseClassRegistry.

    This registry uses class names as keys to store and retrieve classes.
    """

    def register_class(self, cls: type, name: str = None, **kwargs: Any) -> None:
        """Registers a class with the given name.

        Args:
            cls: The class to register.
            name: The name to register the class under. If None, uses the class name.
            **kwargs: Additional keyword arguments (not used in this implementation).
        """
        if name is None:
            name = cls.__name__

        self[name] = cls

    def get_class(self, name: str, default: Any = None) -> Type:
        """Gets a class from the registry by name.

        Args:
            name: The name of the class to retrieve.
            default: The default value to return if the class is not found.

        Returns:
            The requested class, or the default value if not found.
        """
        return self.get(name, default)


class Shape(BaseRegisteredClass):
    """Base class for shapes.

    This class demonstrates how to implement BaseRegisteredClass. Subclasses will be automatically registered in the
    class registry.
    """

    # Class Attributes #
    class_registry_type: ClassVar[Type[BaseClassRegistry]] = SimpleClassRegistry
    class_registration: ClassVar[bool] = True

    # Class Methods #
    @classmethod
    def register_class(cls, name: str = None) -> None:
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
    def get_registered_class(cls, name: str) -> Optional[Type["Shape"]]:
        """Get a registered class by name.

        Args:
            name: The name of the class to retrieve.

        Returns:
            The requested class, or None if not found.
        """
        if cls.class_registry is None:
            return None

        return cls.class_registry.get_class(name)

    # Instance Attributes #
    name: str

    # Magic Methods #
    def __init__(self, name: str) -> None:
        """Initialize a shape with a name.

        Args:
            name: The name of the shape.
        """
        self.name = name

    # Instance Methods #
    def area(self) -> float:
        """Calculate the area of the shape.

        Returns:
            The area of the shape.
        """
        return 0.0

    def perimeter(self) -> float:
        """Calculate the perimeter of the shape.

        Returns:
            The perimeter of the shape.
        """
        return 0.0

    def describe(self) -> str:
        """Return a description of the shape.

        Returns:
            A string describing the shape.
        """
        return f"{self.name} is a generic shape."


class Circle(Shape):
    """A circle shape."""

    def __init__(self, name: str, radius: float) -> None:
        """Initialize a circle with a name and radius.

        Args:
            name: The name of the circle.
            radius: The radius of the circle.
        """
        super().__init__(name)
        self.radius = radius

    def area(self) -> float:
        """Calculate the area of the circle.

        Returns:
            The area of the circle.
        """
        # Standard Libraries #
        import math

        return math.pi * self.radius**2

    def perimeter(self) -> float:
        """Calculate the perimeter (circumference) of the circle.

        Returns:
            The perimeter of the circle.
        """
        # Standard Libraries #
        import math

        return 2 * math.pi * self.radius

    def describe(self) -> str:
        """Return a description of the circle.

        Returns:
            A string describing the circle.
        """
        return f"{self.name} is a circle with radius {self.radius}."


class Rectangle(Shape):
    """A rectangle shape."""

    def __init__(self, name: str, width: float, height: float) -> None:
        """Initialize a rectangle with a name, width, and height.

        Args:
            name: The name of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        super().__init__(name)
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate the area of the rectangle.

        Returns:
            The area of the rectangle.
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle.

        Returns:
            The perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)

    def describe(self) -> str:
        """Return a description of the rectangle.

        Returns:
            A string describing the rectangle.
        """
        return f"{self.name} is a rectangle with width {self.width} and height {self.height}."


class Square(Rectangle):
    """A square shape (special case of rectangle)."""

    def __init__(self, name: str, side: float) -> None:
        """Initialize a square with a name and side length.

        Args:
            name: The name of the square.
            side: The side length of the square.
        """
        super().__init__(name, side, side)
        self.side = side

    def describe(self) -> str:
        """Return a description of the square.

        Returns:
            A string describing the square.
        """
        return f"{self.name} is a square with side length {self.side}."


class Triangle(Shape):
    """A triangle shape."""

    def __init__(self, name: str, a: float, b: float, c: float) -> None:
        """Initialize a triangle with a name and three sides.

        Args:
            name: The name of the triangle.
            a: The length of the first side.
            b: The length of the second side.
            c: The length of the third side.
        """
        super().__init__(name)
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        """Calculate the area of the triangle using Heron's formula.

        Returns:
            The area of the triangle.
        """
        # Standard Libraries #
        import math

        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        """Calculate the perimeter of the triangle.

        Returns:
            The perimeter of the triangle.
        """
        return self.a + self.b + self.c

    def describe(self) -> str:
        """Return a description of the triangle.

        Returns:
            A string describing the triangle.
        """
        return f"{self.name} is a triangle with sides {self.a}, {self.b}, and {self.c}."


# Functions #
# Example Sections #
def automatic_class_registration():
    """Demonstrates automatic registration of subclasses."""
    print("Automatic Class Registration:\n")

    # Check if subclasses were automatically registered
    print("Checking if subclasses were automatically registered...")

    # The class_registry should have been created automatically
    print(f"Class registry exists: {Shape.class_registry is not None}")

    # Print the registered classes
    print("\nRegistered classes:")
    if Shape.class_registry is not None:
        for name, cls in Shape.class_registry.items():
            print(f"  - {name}: {cls.__name__}")

    # Verify that all expected classes are registered
    print("\nVerifying registered classes...")
    assert Shape.get_registered_class("Circle") == Circle
    assert Shape.get_registered_class("Rectangle") == Rectangle
    assert Shape.get_registered_class("Square") == Square
    assert Shape.get_registered_class("Triangle") == Triangle
    print("All classes are correctly registered.")
    print()


def creating_instances_from_registry():
    """Demonstrates creating instances from registered classes."""
    print("Creating Instances from Registry:\n")

    # Get classes from the registry
    print("Getting classes from the registry...")
    circle_class = Shape.get_registered_class("Circle")
    rectangle_class = Shape.get_registered_class("Rectangle")
    square_class = Shape.get_registered_class("Square")
    triangle_class = Shape.get_registered_class("Triangle")

    # Create instances
    print("Creating instances...")
    circle = circle_class("My Circle", 5.0)
    rectangle = rectangle_class("My Rectangle", 4.0, 6.0)
    square = square_class("My Square", 3.0)
    triangle = triangle_class("My Triangle", 3.0, 4.0, 5.0)

    # Use the instances
    print("\nShape descriptions:")
    print(f"  - {circle.describe()}")
    print(f"  - {rectangle.describe()}")
    print(f"  - {square.describe()}")
    print(f"  - {triangle.describe()}")

    print("\nShape areas:")
    print(f"  - Circle area: {circle.area():.2f}")
    print(f"  - Rectangle area: {rectangle.area():.2f}")
    print(f"  - Square area: {square.area():.2f}")
    print(f"  - Triangle area: {triangle.area():.2f}")

    print("\nShape perimeters:")
    print(f"  - Circle perimeter: {circle.perimeter():.2f}")
    print(f"  - Rectangle perimeter: {rectangle.perimeter():.2f}")
    print(f"  - Square perimeter: {square.perimeter():.2f}")
    print(f"  - Triangle perimeter: {triangle.perimeter():.2f}")
    print()


def manual_class_registration():
    """Demonstrates manual registration of classes."""
    print("Manual Class Registration:\n")

    # Define a new shape class that won't be automatically registered
    class Hexagon(Shape):
        """A hexagon shape."""

        class_registration = False  # Disable automatic registration

        def __init__(self, name: str, side: float) -> None:
            """Initialize a hexagon with a name and side length.

            Args:
                name: The name of the hexagon.
                side: The side length of the hexagon.
            """
            super().__init__(name)
            self.side = side

        def area(self) -> float:
            """Calculate the area of the hexagon.

            Returns:
                The area of the hexagon.
            """
            # Standard Libraries #
            import math

            return 3 * math.sqrt(3) * self.side**2 / 2

        def perimeter(self) -> float:
            """Calculate the perimeter of the hexagon.

            Returns:
                The perimeter of the hexagon.
            """
            return 6 * self.side

        def describe(self) -> str:
            """Return a description of the hexagon.

            Returns:
                A string describing the hexagon.
            """
            return f"{self.name} is a hexagon with side length {self.side}."

    # Check if Hexagon was automatically registered (it shouldn't be)
    print("Checking if Hexagon was automatically registered...")
    hexagon_class = Shape.get_registered_class("Hexagon")
    print(f"Hexagon in registry: {hexagon_class is not None} == False")

    # Manually register the Hexagon class
    print("\nManually registering the Hexagon class...")
    Hexagon.register_class()

    # Check if Hexagon is now registered
    print("Checking if Hexagon is now registered...")
    hexagon_class = Shape.get_registered_class("Hexagon")
    print(f"Hexagon in registry: {hexagon_class is not None} == True")

    # Create and use a Hexagon instance
    print("\nCreating and using a Hexagon instance...")
    hexagon = hexagon_class("My Hexagon", 4.0)
    print(f"Description: {hexagon.describe()}")
    print(f"Area: {hexagon.area():.2f}")
    print(f"Perimeter: {hexagon.perimeter():.2f}")
    print()


def shape_factory():
    """Demonstrates using the class registry as a factory for shapes."""
    print("Shape Factory:\n")

    # Create a factory function
    def create_shape(shape_type: str, name: str, **kwargs: Any) -> Shape:
        """Factory function to create shapes.

        Args:
            shape_type: The type of shape to create.
            name: The name of the shape.
            **kwargs: Additional parameters for the shape constructor.

        Returns:
            An instance of the requested shape type.

        Raises:
            ValueError: If the shape type is not found in the registry.
        """
        shape_class = Shape.get_registered_class(shape_type)
        if shape_class is None:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return shape_class(name, **kwargs)

    # Use the factory to create shapes
    print("Using the factory to create shapes...")

    shapes = [
        ("Circle", "Factory Circle", {"radius": 7.0}),
        ("Rectangle", "Factory Rectangle", {"width": 5.0, "height": 8.0}),
        ("Square", "Factory Square", {"side": 4.0}),
        ("Triangle", "Factory Triangle", {"a": 5.0, "b": 7.0, "c": 9.0}),
        ("Hexagon", "Factory Hexagon", {"side": 3.0}),
    ]

    for shape_type, name, params in shapes:
        try:
            shape = create_shape(shape_type, name, **params)
            print(f"\nCreated {shape_type}:")
            print(f"  - Description: {shape.describe()}")
            print(f"  - Area: {shape.area():.2f}")
            print(f"  - Perimeter: {shape.perimeter():.2f}")
        except ValueError as e:
            print(f"\nError creating {shape_type}: {e}")

    # Try to create an unknown shape type
    print("\nTrying to create an unknown shape type...")
    try:
        shape = create_shape("Octagon", "Factory Octagon", side=2.0)
        print(f"Created Octagon: {shape.describe()}")
    except ValueError as e:
        print(f"Error: {e} == 'Unknown shape type: Octagon'")
    print()


# Main #
if __name__ == "__main__":
    # Demonstrate automatic class registration
    automatic_class_registration()

    # Demonstrate creating instances from the registry
    creating_instances_from_registry()

    # Demonstrate manual class registration
    manual_class_registration()

    # Demonstrate using the class registry as a factory
    shape_factory()
