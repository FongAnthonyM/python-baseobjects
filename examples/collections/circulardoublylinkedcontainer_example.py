#!/usr/bin/env python
"""circulardoublylinkedcontainer_example.py
An example of how to use CircularDoublyLinkedContainer class.

This example demonstrates:
1. Creating and using a CircularDoublyLinkedContainer
2. Adding, inserting, and removing nodes
3. Traversing the container in both directions
4. Manipulating node positions
5. Using the container's iterators and cycles
"""


# Imports #
# Source Packages #
from baseobjects.collections import CircularDoublyLinkedContainer
from baseobjects.collections.circulardoublylinkedcontainer import LinkedNode


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of CircularDoublyLinkedContainer."""
    print("\nBasic CircularDoublyLinkedContainer Usage:")

    # Create an empty container
    container = CircularDoublyLinkedContainer()
    print(f"Created empty container: is_empty={container.is_empty} == True")

    # Add nodes to the container
    print("\nAdding nodes to the container:")
    node1 = container.append("First Node")
    print(f"Added node with data: {node1.data} == 'First Node'")

    node2 = container.append("Second Node")
    print(f"Added node with data: {node2.data} == 'Second Node'")

    node3 = container.append("Third Node")
    print(f"Added node with data: {node3.data} == 'Third Node'")

    # Check container properties
    print(f"\nContainer is empty: {container.is_empty} == False")
    print(f"Container length: {len(container)} == 3")

    # Access nodes
    print("\nAccessing nodes:")
    first_node = container.first_node
    assert first_node is not None
    print(f"First node data: {first_node.data} == 'First Node'")

    last_node = container.last_node
    assert last_node is not None
    print(f"Last node data: {last_node.data} == 'Third Node'")

    # Access by index
    print("\nAccessing nodes by index:")
    node_at_0 = container[0]
    print(f"Node at index 0: {node_at_0.data} == 'First Node'")

    node_at_1 = container[1]
    print(f"Node at index 1: {node_at_1.data} == 'Second Node'")

    node_at_2 = container[2]
    print(f"Node at index 2: {node_at_2.data} == 'Third Node'")

    # Negative indexing
    node_at_minus_1 = container[-1]
    print(f"Node at index -1: {node_at_minus_1.data} == 'Third Node'")

    node_at_minus_2 = container[-2]
    print(f"Node at index -2: {node_at_minus_2.data} == 'Second Node'")


def node_manipulation_example() -> None:
    """Demonstrate node manipulation in CircularDoublyLinkedContainer."""
    print("\nNode Manipulation Example:")

    # Create a container with some nodes
    container = CircularDoublyLinkedContainer()
    container.append("Node A")
    container.append("Node B")
    container.append("Node C")

    print("Initial container contents:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Insert a node at a specific position
    print("\nInserting a node at index 1:")
    inserted_node = container.insert("Node X", 1)
    print(f"Inserted node with data: {inserted_node.data} == 'Node X'")

    print("Container contents after insertion:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Remove a node
    print("\nRemoving node at index 2:")
    removed_node = container.pop(2)
    print(f"Removed node with data: {removed_node.data} == 'Node B'")

    print("Container contents after removal:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Move a node to the start
    print("\nMoving 'Node C' to the start:")
    node_to_move = container[2]  # This should be 'Node C'
    container.move_node_start(node_to_move)

    print("Container contents after moving node to start:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Move a node to the end
    print("\nMoving 'Node C' to the end:")
    node_to_move = container[0]  # This should be 'Node C'
    container.move_node_end(node_to_move)

    print("Container contents after moving node to end:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Move a node to a specific position
    print("\nMoving 'Node C' to index 1:")
    node_to_move = container[2]  # This should be 'Node C'
    container.move_node(node_to_move, 1)

    print("Container contents after moving node to index 1:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")


def iteration_example() -> None:
    """Demonstrate iteration through CircularDoublyLinkedContainer."""
    print("\nIteration Example:")

    # Create a container with some nodes
    container = CircularDoublyLinkedContainer()
    container.append("Node 1")
    container.append("Node 2")
    container.append("Node 3")
    container.append("Node 4")

    print("Container contents:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Forward iteration (default)
    print("\nForward iteration:")
    for node in container.forward_iter():
        print(f"  {node.data}")

    # Reverse iteration
    print("\nReverse iteration:")
    for node in container.reverse_iter():
        print(f"  {node.data}")

    # Demonstrate cycle (limited to 8 iterations for example)
    print("\nForward cycle (first 8 iterations):")
    cycle = container.forward_cycle()
    for i in range(8):
        node = next(cycle)
        print(f"  Iteration {i}: {node.data}")

    # Reverse cycle (limited to 8 iterations for example)
    print("\nReverse cycle (first 8 iterations):")
    cycle = container.reverse_cycle()
    for i in range(8):
        node = next(cycle)
        print(f"  Iteration {i}: {node.data}")


def shift_example() -> None:
    """Demonstrate shifting the start position in CircularDoublyLinkedContainer."""
    print("\nShift Example:")

    # Create a container with some nodes
    container = CircularDoublyLinkedContainer()
    container.append("Node A")
    container.append("Node B")
    container.append("Node C")
    container.append("Node D")

    print("Initial container contents:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Shift left by 1
    print("\nShifting left by 1:")
    container.shift_left(1)
    # or use the operator: container << 1

    print("Container contents after shift left:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Shift right by 2
    print("\nShifting right by 2:")
    container.shift_right(2)
    # or use the operator: container >> 2

    print("Container contents after shift right:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")


def custom_node_example() -> None:
    """Demonstrate using custom LinkedNode objects."""
    print("\nCustom Node Example:")

    # Create custom nodes
    node_a = LinkedNode("Custom Node A")
    node_b = LinkedNode("Custom Node B")
    node_c = LinkedNode("Custom Node C")

    # Create a container and add the custom nodes
    container = CircularDoublyLinkedContainer()
    container.append(node_a)
    container.append(node_b)
    container.append(node_c)

    print("Container with custom nodes:")
    for i, node in enumerate(container):
        print(f"  Node {i}: {node.data}")

    # Demonstrate that the nodes are properly linked
    print("\nNavigating through nodes directly:")
    current = container.first_node
    assert current is not None
    assert current.next is not None
    assert current.next.next is not None
    assert current.next.next.next is not None

    print(f"First node: {current.data}")
    print(f"Next node: {current.next.data}")
    print(f"Next node's next: {current.next.next.data}")
    print(f"Next node's next's next (circular): {current.next.next.next.data}")

    print("\nNavigating backwards:")
    assert current.previous is not None
    assert current.previous.previous is not None

    print(f"First node's previous (circular): {current.previous.data}")
    print(f"Previous node's previous: {current.previous.previous.data}")


def practical_example() -> None:
    """Demonstrate a practical use case for CircularDoublyLinkedContainer."""
    print("\nPractical Example - Circular Buffer:")

    # Create a circular buffer with a maximum size of 3
    class CircularBuffer:
        def __init__(self, max_size: int) -> None:
            self.container = CircularDoublyLinkedContainer()
            self.max_size = max_size

        def add(self, item: object) -> None:
            if len(self.container) >= self.max_size:
                # Remove the oldest item (first node)
                self.container.pop(0)
            self.container.append(item)

        def get_items(self) -> list[object]:
            return [node.data for node in self.container]

    # Create a buffer and add items
    buffer = CircularBuffer(max_size=3)

    print("Adding 'Item 1' to buffer:")
    buffer.add("Item 1")
    print(f"Buffer contents: {buffer.get_items()} == ['Item 1']")

    print("\nAdding 'Item 2' to buffer:")
    buffer.add("Item 2")
    print(f"Buffer contents: {buffer.get_items()} == ['Item 1', 'Item 2']")

    print("\nAdding 'Item 3' to buffer:")
    buffer.add("Item 3")
    print(f"Buffer contents: {buffer.get_items()} == ['Item 1', 'Item 2', 'Item 3']")

    print("\nAdding 'Item 4' to buffer (exceeds max size, will remove oldest):")
    buffer.add("Item 4")
    print(f"Buffer contents: {buffer.get_items()} == ['Item 2', 'Item 3', 'Item 4']")

    print("\nAdding 'Item 5' to buffer:")
    buffer.add("Item 5")
    print(f"Buffer contents: {buffer.get_items()} == ['Item 3', 'Item 4', 'Item 5']")


def deep_copy_example() -> None:
    """Demonstrate deep copying of CircularDoublyLinkedContainer."""
    print("\nDeep Copy Example:")

    # Standard Libraries #
    import copy

    # Create a container with some nodes
    original = CircularDoublyLinkedContainer()
    original.append("Node 1")
    original.append("Node 2")
    original.append("Node 3")

    print("Original container contents:")
    for i, node in enumerate(original):
        print(f"  Node {i}: {node.data}")

    # Create a deep copy
    copied = copy.deepcopy(original)

    print("\nCopied container contents:")
    for i, node in enumerate(copied):
        print(f"  Node {i}: {node.data}")

    # Modify the original
    print("\nModifying original container:")
    original.append("Node 4")
    original[0].data = "Modified Node 1"

    print("Original container after modification:")
    for i, node in enumerate(original):
        print(f"  Node {i}: {node.data}")

    print("\nCopied container (should be unchanged):")
    for i, node in enumerate(copied):
        print(f"  Node {i}: {node.data}")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    node_manipulation_example()
    iteration_example()
    shift_example()
    custom_node_example()
    practical_example()
    deep_copy_example()
