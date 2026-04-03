#!/usr/bin/env python
"""namespaceregisteredclass_example.py
An example of how to create and use NamespaceRegisteredClass.

This example demonstrates:
1. Creating a concrete implementation of NamespaceRegisteredClass
2. Automatic registration of subclasses with namespaces
3. Retrieving registered subclasses by namespace and name
4. Customizing namespace and name for registration
5. Using the class registry for dispatching
"""

# Imports #
# Standard Libraries #
from typing import Any, ClassVar

# Source Packages #
from baseobjects.classregistration import NamespaceRegisteredClass


# Definitions #
# Classes #
class Vehicle(NamespaceRegisteredClass):
    """Base class for vehicles.

    This class demonstrates how to implement NamespaceRegisteredClass.
    Subclasses will be automatically registered in the class registry with namespaces.
    """

    # Class Attributes #
    class_registration: ClassVar[bool] = True

    # Instance Attributes #
    name: str

    def __init__(self, name: str) -> None:
        """Initializes a vehicle with a name.

        Args:
            name: The name of the vehicle.
        """
        self.name = name

    def start(self) -> str:
        """Starts the vehicle.

        Returns:
            A message indicating the vehicle has started.
        """
        return f"{self.name} is starting..."

    def stop(self) -> str:
        """Stops the vehicle.

        Returns:
            A message indicating the vehicle has stopped.
        """
        return f"{self.name} is stopping..."

    def describe(self) -> str:
        """Returns a description of the vehicle.

        Returns:
            A string describing the vehicle.
        """
        return f"{self.name} is a generic vehicle."


class Car(Vehicle):
    """A car vehicle."""

    # Class Attributes #
    class_registry_namespace: ClassVar[str] = "land"

    def __init__(self, name: str, doors: int = 4) -> None:
        """Initializes a car with a name and number of doors.

        Args:
            name: The name of the car.
            doors: The number of doors.
        """
        super().__init__(name)
        self.doors = doors

    def start(self) -> str:
        """Starts the car.

        Returns:
            A message indicating the car has started.
        """
        return f"{self.name} car engine is starting... Vroom!"

    def describe(self) -> str:
        """Returns a description of the car.

        Returns:
            A string describing the car.
        """
        return f"{self.name} is a car with {self.doors} doors."


class Motorcycle(Vehicle):
    """A motorcycle vehicle."""

    # Class Attributes #
    class_registry_namespace: ClassVar[str] = "land"
    class_registry_name: ClassVar[str] = "Bike"  # Custom name for registry

    def __init__(self, name: str, has_sidecar: bool = False) -> None:
        """Initializes a motorcycle with a name and sidecar information.

        Args:
            name: The name of the motorcycle.
            has_sidecar: Whether the motorcycle has a sidecar.
        """
        super().__init__(name)
        self.has_sidecar = has_sidecar

    def start(self) -> str:
        """Starts the motorcycle.

        Returns:
            A message indicating the motorcycle has started.
        """
        return f"{self.name} motorcycle engine is starting... Vroom vroom!"

    def describe(self) -> str:
        """Returns a description of the motorcycle.

        Returns:
            A string describing the motorcycle.
        """
        sidecar_info = "with a sidecar" if self.has_sidecar else "without a sidecar"
        return f"{self.name} is a motorcycle {sidecar_info}."


class Boat(Vehicle):
    """A boat vehicle."""

    # Class Attributes #
    class_registry_namespace: ClassVar[str] = "water"

    def __init__(self, name: str, length: float) -> None:
        """Initializes a boat with a name and length.

        Args:
            name: The name of the boat.
            length: The length of the boat in meters.
        """
        super().__init__(name)
        self.length = length

    def start(self) -> str:
        """Starts the boat.

        Returns:
            A message indicating the boat has started.
        """
        return f"{self.name} boat engine is starting... Rumble!"

    def describe(self) -> str:
        """Returns a description of the boat.

        Returns:
            A string describing the boat.
        """
        return f"{self.name} is a boat with length {self.length} meters."


class Airplane(Vehicle):
    """An airplane vehicle."""

    # Class Attributes #
    class_registry_namespace: ClassVar[str] = "air"

    def __init__(self, name: str, engines: int) -> None:
        """Initializes an airplane with a name and number of engines.

        Args:
            name: The name of the airplane.
            engines: The number of engines.
        """
        super().__init__(name)
        self.engines = engines

    def start(self) -> str:
        """Starts the airplane.

        Returns:
            A message indicating the airplane has started.
        """
        return f"{self.name} airplane engines are starting... Whoosh!"

    def describe(self) -> str:
        """Returns a description of the airplane.

        Returns:
            A string describing the airplane.
        """
        return f"{self.name} is an airplane with {self.engines} engines."


class Helicopter(Vehicle):
    """A helicopter vehicle."""

    # Class Attributes #
    _module_ = "air"  # Using _module_ instead of class_registry_namespace

    def __init__(self, name: str, rotors: int = 1) -> None:
        """Initializes a helicopter with a name and number of rotors.

        Args:
            name: The name of the helicopter.
            rotors: The number of main rotors.
        """
        super().__init__(name)
        self.rotors = rotors

    def start(self) -> str:
        """Starts the helicopter.

        Returns:
            A message indicating the helicopter has started.
        """
        return f"{self.name} helicopter rotors are starting... Whop whop whop!"

    def describe(self) -> str:
        """Returns a description of the helicopter.

        Returns:
            A string describing the helicopter.
        """
        return f"{self.name} is a helicopter with {self.rotors} main rotor(s)."


# Functions #
# Example Sections #
def automatic_namespace_registration() -> None:
    """Demonstrates automatic registration of subclasses with namespaces."""
    print("Automatic Namespace Registration:\n")

    # Checks if subclasses were automatically registered
    print("Checking if subclasses were automatically registered...")

    # The class_registry should have been created automatically
    print(f"Class registry exists: {Vehicle.class_registry is not None}")

    # Prints the registered classes by namespace
    print("\nRegistered classes by namespace:")
    if Vehicle.class_registry is not None:
        for namespace, classes in Vehicle.class_registry.items():
            print(f"Namespace: {namespace}")
            for name, (cls, _kwargs) in classes.items():
                print(f"  - {name}: {cls.__name__}")

    # Verifies that all expected classes are registered in their correct namespaces
    print("\nVerifying registered classes...")
    assert Vehicle.get_registered_class("land", "Car") == Car
    assert Vehicle.get_registered_class("land", "Bike") == Motorcycle  # Note the custom name
    assert Vehicle.get_registered_class("water", "Boat") == Boat
    assert Vehicle.get_registered_class("air", "Airplane") == Airplane
    assert Vehicle.get_registered_class("air", "Helicopter") == Helicopter
    print("All classes are correctly registered in their namespaces.")
    print()


def creating_instances_from_registry() -> None:
    """Demonstrates creating instances from registered classes."""
    print("Creating Instances from Registry:\n")

    # Gets classes from the registry
    print("Getting classes from the registry by namespace and name...")
    car_class: Any = Vehicle.get_registered_class("land", "Car")
    assert car_class is not None
    motorcycle_class: Any = Vehicle.get_registered_class("land", "Bike")
    assert motorcycle_class is not None
    boat_class: Any = Vehicle.get_registered_class("water", "Boat")
    assert boat_class is not None
    airplane_class: Any = Vehicle.get_registered_class("air", "Airplane")
    assert airplane_class is not None
    helicopter_class: Any = Vehicle.get_registered_class("air", "Helicopter")
    assert helicopter_class is not None

    # Creates instances
    print("Creating instances...")
    car = car_class("Sedan", doors=4)
    motorcycle = motorcycle_class("Cruiser", has_sidecar=True)
    boat = boat_class("Sailboat", length=12.5)
    airplane = airplane_class("Jumbo Jet", engines=4)
    helicopter = helicopter_class("Chopper", rotors=2)

    # Use the instances
    print("\nVehicle descriptions:")
    print(f"  - {car.describe()}")
    print(f"  - {motorcycle.describe()}")
    print(f"  - {boat.describe()}")
    print(f"  - {airplane.describe()}")
    print(f"  - {helicopter.describe()}")

    print("\nStarting vehicles:")
    print(f"  - {car.start()}")
    print(f"  - {motorcycle.start()}")
    print(f"  - {boat.start()}")
    print(f"  - {airplane.start()}")
    print(f"  - {helicopter.start()}")
    print()


def custom_namespace_and_name() -> None:
    """Demonstrates registering a class with a custom namespace and name."""
    print("Custom Namespace and Name:\n")

    # Defines a new vehicle class with custom namespace and name
    class Submarine(Vehicle):
        """A submarine vehicle."""

        def __init__(self, name: str, depth: float) -> None:
            """Initializes a submarine with a name and maximum depth.

            Args:
                name: The name of the submarine.
                depth: The maximum depth in meters.
            """
            super().__init__(name)
            self.depth = depth

        def start(self) -> str:
            """Starts the submarine.

            Returns:
                A message indicating the submarine has started.
            """
            return f"{self.name} submarine engines are starting... Bubble bubble!"

        def describe(self) -> str:
            """Returns a description of the submarine.

            Returns:
                A string describing the submarine.
            """
            return f"{self.name} is a submarine that can dive to {self.depth} meters."

    # Registers the submarine with a custom namespace and name
    print("Registering a submarine with custom namespace and name...")
    Submarine.register_class(namespace="underwater", name="Sub")

    # Verifies the submarine is registered
    print("\nVerifying submarine registration...")
    submarine_class: Any = Vehicle.get_registered_class("underwater", "Sub")
    assert submarine_class == Submarine
    print("Submarine is correctly registered as 'Sub' in the 'underwater' namespace.")

    # Creates and use a submarine instance
    print("\nCreating and using a submarine instance...")
    submarine = submarine_class("Deep Diver", depth=1000.0)
    print(f"Description: {submarine.describe()}")
    print(f"Starting: {submarine.start()}")
    print()


def module_based_namespace() -> None:
    """Demonstrates using the module name as the namespace."""
    print("Module-Based Namespace:\n")

    # Defines a new vehicle class that uses its module as the namespace
    class Spaceship(Vehicle):
        """A spaceship vehicle."""

        # No explicit namespace - will use module

        def __init__(self, name: str, warp_speed: float) -> None:
            """Initializes a spaceship with a name and warp speed.

            Args:
                name: The name of the spaceship.
                warp_speed: The maximum warp speed.
            """
            super().__init__(name)
            self.warp_speed = warp_speed

        def start(self) -> str:
            """Starts the spaceship.

            Returns:
                A message indicating the spaceship has started.
            """
            return f"{self.name} spaceship engines are starting... Whoosh!"

        def describe(self) -> str:
            """Returns a description of the spaceship.

            Returns:
                A string describing the spaceship.
            """
            return f"{self.name} is a spaceship capable of warp {self.warp_speed}."

    # The spaceship should be registered with the module name as the namespace
    print("Checking if spaceship is registered with module name as namespace...")

    # Prints all namespaces to find the spaceship
    print("\nAll namespaces in registry:")
    assert Vehicle.class_registry is not None
    for namespace, classes in Vehicle.class_registry.items():
        print(f"Namespace: {namespace}")
        for name, (cls, _kwargs) in classes.items():
            print(f"  - {name}: {cls.__name__}")

    # Finds the spaceship in the registry
    spaceship_found = False
    for namespace, classes in Vehicle.class_registry.items():
        if "Spaceship" in classes:
            spaceship_class = classes["Spaceship"][0]
            if spaceship_class == Spaceship:
                spaceship_found = True
                print(f"\nSpaceship found in namespace: {namespace}")
                break

    assert spaceship_found, "Spaceship should be registered with its module as namespace"

    # Creates and use a spaceship instance
    print("\nCreating and using a spaceship instance...")
    spaceship = Spaceship("Enterprise", warp_speed=9.0)
    print(f"Description: {spaceship.describe()}")
    print(f"Starting: {spaceship.start()}")
    print()


def vehicle_factory() -> None:
    """Demonstrates using the class registry as a factory for vehicles."""
    print("Vehicle Factory:\n")

    # Creates a factory function
    def create_vehicle(vehicle_type: str, namespace: str, name: str, **kwargs: Any) -> Vehicle:
        """Factory function to create vehicles.

        Args:
            vehicle_type: The type of vehicle to create (namespace).
            namespace: The namespace of the vehicle class.
            name: The name of the vehicle.
            **kwargs: Additional parameters for the vehicle constructor.

        Returns:
            An instance of the requested vehicle type.

        Raises:
            ValueError: If the vehicle type is not found in the registry.
        """
        try:
            vehicle_class: Any = Vehicle.get_registered_class(namespace, vehicle_type)
        except KeyError:
            vehicle_class = None

        if vehicle_class is None:
            msg = f"Unknown vehicle type: {vehicle_type} in namespace {namespace}"
            raise ValueError(msg)
        result = vehicle_class(name, **kwargs)
        assert isinstance(result, Vehicle)
        return result

    # Use the factory to create vehicles
    print("Using the factory to create vehicles...")

    vehicles: list[tuple[str, str, str, dict[str, Any]]] = [
        ("Car", "land", "Luxury Sedan", {"doors": 2}),
        ("Bike", "land", "Sport Bike", {"has_sidecar": False}),
        ("Boat", "water", "Yacht", {"length": 20.0}),
        ("Airplane", "air", "Passenger Jet", {"engines": 2}),
        ("Helicopter", "air", "Medical Chopper", {"rotors": 1}),
        ("Sub", "underwater", "Research Sub", {"depth": 500.0}),
    ]

    for vehicle_type, namespace, name, params in vehicles:
        try:
            vehicle = create_vehicle(vehicle_type, namespace, name, **params)
            print(f"\nCreated {vehicle_type}:")
            print(f"  - Description: {vehicle.describe()}")
            print(f"  - Starting: {vehicle.start()}")
        except ValueError as e:
            print(f"\nError creating {vehicle_type}: {e}")

    # Try to create an unknown vehicle type
    print("\nTrying to create an unknown vehicle type...")
    try:
        vehicle = create_vehicle("Rocket", "space", "Moon Rocket", thrust=1000000)
        print(f"Created Rocket: {vehicle.describe()}")
    except ValueError as e:
        print(f"Error: {e}")
    print()


# Main #
if __name__ == "__main__":
    # Demonstrates automatic namespace registration
    automatic_namespace_registration()

    # Demonstrates creating instances from the registry
    creating_instances_from_registry()

    # Demonstrates custom namespace and name
    custom_namespace_and_name()

    # Demonstrates module-based namespace
    module_based_namespace()

    # Demonstrates using the class registry as a factory
    vehicle_factory()
