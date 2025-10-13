#!/usr/bin/env python
"""circulardoublylinkedcontainer_performance.py
Performance tests for the CircularDoublyLinkedContainer and LinkedNode classes in the baseobjects.collections package.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import copy
import pickle
import timeit
from typing import Any, ClassVar, Dict, List

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.collections import CircularDoublyLinkedContainer, LinkedNode
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestLinkedNodePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the LinkedNode class.

    This test suite measures the performance of various operations on LinkedNode objects
    and compares them with standard Python implementations.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_node(self) -> LinkedNode:
        """Create a test LinkedNode for use in tests.

        Returns:
            LinkedNode: An instance of LinkedNode with test data.
        """
        return LinkedNode("test_data")

    @pytest.fixture
    def linked_nodes(self) -> List[LinkedNode]:
        """Create a list of linked nodes for use in tests.

        Returns:
            List[LinkedNode]: A list of linked nodes.
        """
        nodes = [LinkedNode(f"data{i}") for i in range(5)]
        # Link the nodes
        for i in range(len(nodes)):
            nodes[i].next = nodes[(i + 1) % len(nodes)]
            nodes[i].previous = nodes[(i - 1) % len(nodes)]
        return nodes

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating LinkedNode instances.

        This test measures the speed of creating a LinkedNode.
        """

        def create_node() -> None:
            LinkedNode("test_data")

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(create_node, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nLinkedNode creation: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        # No comparison here, just measuring the absolute time

    def test_access_speed_performance(self, linked_nodes: List[LinkedNode]) -> None:
        """Test the performance of accessing next and previous nodes.

        This test measures the speed of accessing next and previous nodes.

        Args:
            linked_nodes: A fixture providing a list of linked nodes.
        """
        node = linked_nodes[0]

        def access_next() -> None:
            _ = node.next

        def access_previous() -> None:
            _ = node.previous

        # Calculate the mean time in microseconds for next access
        next_time = timeit.timeit(access_next, number=self.timeit_runs)
        mean_next = next_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for previous access
        prev_time = timeit.timeit(access_previous, number=self.timeit_runs)
        mean_prev = prev_time / self.timeit_runs * 1000000

        # Print the performance measurements
        print(f"\nAccess next: {mean_next:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"Access previous: {mean_prev:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time


class TestCircularDoublyLinkedContainerPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the CircularDoublyLinkedContainer class.

    This test suite measures the performance of various operations on CircularDoublyLinkedContainer objects
    and compares them with standard Python list implementations.
    """

    # Attributes #
    timeit_runs: int = 10000  # Reduced for more complex operations
    speed_tolerance: float = 200.0  # Higher tolerance for linked structures

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_container(self) -> CircularDoublyLinkedContainer:
        """Create a test CircularDoublyLinkedContainer for use in tests.

        Returns:
            CircularDoublyLinkedContainer: An instance of the test class.
        """
        return CircularDoublyLinkedContainer()

    @pytest.fixture
    def populated_test_container(self) -> CircularDoublyLinkedContainer:
        """Create a populated test CircularDoublyLinkedContainer for use in tests.

        Returns:
            CircularDoublyLinkedContainer: A populated instance of the test class.
        """
        container = CircularDoublyLinkedContainer()
        for i in range(100):
            container.append(f"value{i}")
        return container

    @pytest.fixture
    def normal_list(self) -> list:
        """Create a normal list for comparison.

        Returns:
            list: A standard Python list.
        """
        return []

    @pytest.fixture
    def populated_normal_list(self) -> list:
        """Create a populated normal list for comparison.

        Returns:
            list: A populated standard Python list.
        """
        return [f"value{i}" for i in range(100)]

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating CircularDoublyLinkedContainer instances.

        This test compares the speed of creating an empty CircularDoublyLinkedContainer with a normal list.
        """

        def create_container() -> None:
            CircularDoublyLinkedContainer()

        def create_list() -> None:
            list()

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(create_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(create_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list creation: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"CircularDoublyLinkedContainer creation: {mean_container:.3f} μs ({percent:.3f}% of standard list creation time)"
        )
        assert percent < self.speed_tolerance

    def test_append_speed_performance(self, test_container: CircularDoublyLinkedContainer, normal_list: list) -> None:
        """Test the performance of appending an item to a CircularDoublyLinkedContainer.

        This test compares the speed of appending an item to a CircularDoublyLinkedContainer with a normal list.

        Args:
            test_container: A fixture providing a CircularDoublyLinkedContainer instance.
            normal_list: A fixture providing a normal list.
        """
        value = "test_value"

        def append_container() -> None:
            test_container.append(value)

        def append_list() -> None:
            normal_list.append(value)

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(append_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(append_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list append: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"CircularDoublyLinkedContainer append: {mean_container:.3f} μs ({percent:.3f}% of standard list append time)"
        )
        assert percent < self.speed_tolerance

    def test_get_item_speed_performance(
        self, populated_test_container: CircularDoublyLinkedContainer, populated_normal_list: list
    ) -> None:
        """Test the performance of getting an item from a CircularDoublyLinkedContainer.

        This test compares the speed of getting an item from a CircularDoublyLinkedContainer with a normal list.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        index = 50

        def get_container() -> None:
            populated_test_container[index]

        def get_list() -> None:
            populated_normal_list[index]

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(get_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(get_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list get item: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"CircularDoublyLinkedContainer get item: {mean_container:.3f} μs ({percent:.3f}% of standard list get item time)"
        )
        assert percent < self.speed_tolerance

    def test_insert_speed_performance(self, test_container: CircularDoublyLinkedContainer, normal_list: list) -> None:
        """Test the performance of inserting an item into a CircularDoublyLinkedContainer.

        This test compares the speed of inserting an item into a CircularDoublyLinkedContainer with a normal list.

        Args:
            test_container: A fixture providing a CircularDoublyLinkedContainer instance.
            normal_list: A fixture providing a normal list.
        """
        # We'll insert at the beginning to make it fair for both implementations
        index = 0
        value = "insert_value"

        def insert_container() -> None:
            test_container.insert(value, index)

        def insert_list() -> None:
            normal_list.insert(index, value)

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(insert_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(insert_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list insert: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"CircularDoublyLinkedContainer insert: {mean_container:.3f} μs ({percent:.3f}% of standard list insert time)"
        )
        assert percent < self.speed_tolerance

    def test_pop_speed_performance(
        self, populated_test_container: CircularDoublyLinkedContainer, populated_normal_list: list
    ) -> None:
        """Test the performance of popping an item from a CircularDoublyLinkedContainer.

        This test compares the speed of popping an item from a CircularDoublyLinkedContainer with a normal list.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
            populated_normal_list: A fixture providing a populated normal list.
        """

        # We need to repopulate after each pop to avoid emptying the containers
        def pop_and_repopulate_container() -> None:
            try:
                populated_test_container.pop()
            except (IndexError, KeyError):
                # Repopulate if empty
                for i in range(100):
                    populated_test_container.append(f"value{i}")

        def pop_and_repopulate_list() -> None:
            try:
                populated_normal_list.pop()
            except IndexError:
                # Repopulate if empty
                populated_normal_list.extend([f"value{i}" for i in range(100)])

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(pop_and_repopulate_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(pop_and_repopulate_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(f"\nStandard list pop: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"CircularDoublyLinkedContainer pop: {mean_container:.3f} μs ({percent:.3f}% of standard list pop time)")
        assert percent < self.speed_tolerance

    def test_iteration_speed_performance(
        self, populated_test_container: CircularDoublyLinkedContainer, populated_normal_list: list
    ) -> None:
        """Test the performance of iterating over a CircularDoublyLinkedContainer.

        This test compares the speed of iterating over a CircularDoublyLinkedContainer with a normal list.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
            populated_normal_list: A fixture providing a populated normal list.
        """

        def iterate_container() -> None:
            for node in populated_test_container:
                pass

        def iterate_list() -> None:
            for item in populated_normal_list:
                pass

        # Calculate the mean time in microseconds for the container implementation
        container_time = timeit.timeit(iterate_container, number=self.timeit_runs)
        mean_container = container_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(iterate_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_container / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list iteration: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"CircularDoublyLinkedContainer iteration: {mean_container:.3f} μs ({percent:.3f}% of standard list iteration time)"
        )
        assert percent < self.speed_tolerance

    def test_shift_left_speed_performance(self, populated_test_container: CircularDoublyLinkedContainer) -> None:
        """Test the performance of shifting a CircularDoublyLinkedContainer to the left.

        This test measures the speed of shifting a CircularDoublyLinkedContainer to the left.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
        """

        def shift_left() -> None:
            populated_test_container.shift_left(1)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(shift_left, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nShift left: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_shift_right_speed_performance(self, populated_test_container: CircularDoublyLinkedContainer) -> None:
        """Test the performance of shifting a CircularDoublyLinkedContainer to the right.

        This test measures the speed of shifting a CircularDoublyLinkedContainer to the right.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
        """

        def shift_right() -> None:
            populated_test_container.shift_right(1)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(shift_right, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nShift right: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_move_node_start_speed_performance(self, populated_test_container: CircularDoublyLinkedContainer) -> None:
        """Test the performance of moving a node to the start of a CircularDoublyLinkedContainer.

        This test measures the speed of moving a node to the start of a CircularDoublyLinkedContainer.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
        """
        # Get a node from the middle
        node = populated_test_container[50]

        def move_node_start() -> None:
            populated_test_container.move_node_start(node)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(move_node_start, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nMove node start: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_move_node_end_speed_performance(self, populated_test_container: CircularDoublyLinkedContainer) -> None:
        """Test the performance of moving a node to the end of a CircularDoublyLinkedContainer.

        This test measures the speed of moving a node to the end of a CircularDoublyLinkedContainer.

        Args:
            populated_test_container: A fixture providing a populated CircularDoublyLinkedContainer instance.
        """
        # Get a node from the middle
        node = populated_test_container[50]

        def move_node_end() -> None:
            populated_test_container.move_node_end(node)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(move_node_end, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nMove node end: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
