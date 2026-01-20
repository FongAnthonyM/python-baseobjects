#!/usr/bin/env python
"""deepchainmap_performance.py
Performance tests for the DeepChainMap class in the baseobjects.collections package.
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
import timeit
from collections import ChainMap
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.collections import DeepChainMap
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestDeepChainMapPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the DeepChainMap class.

    This test suite measures the performance of various operations on DeepChainMap objects and compares them with
    standard Python ChainMap implementations.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_map(self) -> DeepChainMap:
        """Create a test DeepChainMap for use in tests.

        Returns:
            DeepChainMap: An instance of DeepChainMap with an empty mapping.
        """
        return DeepChainMap({})

    @pytest.fixture
    def populated_test_map(self) -> DeepChainMap:
        """Create a populated test DeepChainMap for use in tests.

        Returns:
            DeepChainMap: A populated instance of DeepChainMap with two mappings.
        """
        map1 = {f"key{i}": f"value{i}" for i in range(50)}
        map2 = {f"key{i + 50}": f"value{i + 50}" for i in range(50)}
        return DeepChainMap(map1, map2)

    @pytest.fixture
    def nested_test_map(self) -> DeepChainMap:
        """Create a nested test DeepChainMap for use in tests.

        Returns:
            DeepChainMap: A nested instance of DeepChainMap with keys in multiple maps.
        """
        map1 = {f"key{i}": f"value{i}" for i in range(30)}
        map2 = {f"key{i}": f"value{i}_map2" for i in range(20, 50)}
        map3 = {f"key{i}": f"value{i}_map3" for i in range(40, 70)}
        return DeepChainMap(map1, map2, map3)

    @pytest.fixture
    def normal_map(self) -> ChainMap[Any, Any]:
        """Create a normal ChainMap for comparison.

        Returns:
            ChainMap: A standard Python ChainMap with an empty mapping.
        """
        return ChainMap({})

    @pytest.fixture
    def populated_normal_map(self) -> ChainMap[Any, Any]:
        """Create a populated normal ChainMap for comparison.

        Returns:
            ChainMap: A populated standard Python ChainMap with two mappings.
        """
        map1 = {f"key{i}": f"value{i}" for i in range(50)}
        map2 = {f"key{i + 50}": f"value{i + 50}" for i in range(50)}
        return ChainMap(map1, map2)

    @pytest.fixture
    def nested_normal_map(self) -> ChainMap[Any, Any]:
        """Create a nested normal ChainMap for comparison.

        Returns:
            ChainMap: A nested standard Python ChainMap with keys in multiple maps.
        """
        map1 = {f"key{i}": f"value{i}" for i in range(30)}
        map2 = {f"key{i}": f"value{i}_map2" for i in range(20, 50)}
        map3 = {f"key{i}": f"value{i}_map3" for i in range(40, 70)}
        return ChainMap(map1, map2, map3)

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating DeepChainMap instances.

        This test compares the speed of creating an empty DeepChainMap with a normal ChainMap.
        """

        def create_deep() -> None:
            DeepChainMap({})

        def create_normal() -> None:
            ChainMap({})

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(create_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap creation: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap creation: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap creation time)",
        )
        assert percent < self.speed_tolerance

    def test_creation_speed_populated_performance(self) -> None:
        """Test the performance of creating a populated DeepChainMap.

        This test compares the speed of creating a populated DeepChainMap with a normal ChainMap.
        """
        map1 = {f"key{i}": f"value{i}" for i in range(50)}
        map2 = {f"key{i + 50}": f"value{i + 50}" for i in range(50)}

        def create_deep() -> None:
            DeepChainMap(map1, map2)

        def create_normal() -> None:
            ChainMap(map1, map2)

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(create_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap populated creation: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap populated creation: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap populated creation time)",
        )
        assert percent < self.speed_tolerance

    def test_get_item_speed_performance(
        self,
        populated_test_map: DeepChainMap,
        populated_normal_map: ChainMap[Any, Any],
    ) -> None:
        """Test the performance of getting an item from a DeepChainMap.

        This test compares the speed of getting an item from a DeepChainMap with a normal ChainMap.

        Args:
            populated_test_map: A fixture providing a populated DeepChainMap instance.
            populated_normal_map: A fixture providing a populated normal ChainMap.
        """
        key = "key25"  # Key in the first map

        def get_deep() -> None:
            populated_test_map[key]

        def get_normal() -> None:
            populated_normal_map[key]

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(get_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(get_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap get item: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap get item: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap get item time)",
        )
        assert percent < self.speed_tolerance

    def test_set_item_speed_new_performance(
        self,
        test_map: DeepChainMap,
        normal_map: ChainMap[Any, Any],
    ) -> None:
        """Test the performance of setting a new item in a DeepChainMap.

        This test compares the speed of setting a new item in a DeepChainMap with a normal ChainMap.

        Args:
            test_map: A fixture providing a DeepChainMap instance.
            normal_map: A fixture providing a normal ChainMap.
        """
        key = "new_key"
        value = "new_value"

        def set_deep() -> None:
            test_map[key] = value

        def set_normal() -> None:
            normal_map[key] = value

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(set_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(set_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap set new item: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap set new item: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap set new item time)",
        )
        assert percent < self.speed_tolerance

    def test_set_item_speed_existing_performance(
        self,
        nested_test_map: DeepChainMap,
        nested_normal_map: ChainMap[Any, Any],
    ) -> None:
        """Test the performance of updating an existing item in a DeepChainMap.

        This test compares the speed of updating an existing item in a DeepChainMap with a normal ChainMap. The key
        exists in a nested map, not the first map.

        Args:
            nested_test_map: A fixture providing a nested DeepChainMap instance.
            nested_normal_map: A fixture providing a nested normal ChainMap.
        """
        key = "key25"  # Key in the second map
        value = "updated_value"

        def set_deep() -> None:
            nested_test_map[key] = value

        def set_normal() -> None:
            # Standard ChainMap always updates the first map, so we need to simulate deep behavior
            for mapping in nested_normal_map.maps:
                if key in mapping:
                    mapping[key] = value
                    break

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(set_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(set_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap set existing item: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap set existing item: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap set existing item time)",
        )
        assert percent < self.speed_tolerance

    def test_del_item_speed_performance(
        self,
        nested_test_map: DeepChainMap,
        nested_normal_map: ChainMap[Any, Any],
    ) -> None:
        """Test the performance of deleting an item from a DeepChainMap.

        This test compares the speed of deleting an item from a DeepChainMap with a normal ChainMap.
        The key exists in a nested map, not the first map.

        Args:
            nested_test_map: A fixture providing a nested DeepChainMap instance.
            nested_normal_map: A fixture providing a nested normal ChainMap.
        """
        # We'll use different keys for each run to avoid KeyError after deletion
        keys_deep = [f"key{i}" for i in range(25, 30)]
        keys_normal = [f"key{i}" for i in range(25, 30)]
        key_index = 0

        def del_deep() -> None:
            nonlocal key_index
            key = keys_deep[key_index % len(keys_deep)]
            key_index += 1
            try:
                del nested_test_map[key]
            except KeyError:
                pass

        def del_normal() -> None:
            nonlocal key_index
            key = keys_normal[key_index % len(keys_normal)]
            key_index += 1
            # Standard ChainMap doesn't support deleting from nested maps, so we need to simulate deep behavior
            try:
                for mapping in nested_normal_map.maps:
                    if key in mapping:
                        del mapping[key]
                        break
            except KeyError:
                pass

        # Calculate the mean time in microseconds for the DeepChainMap implementation
        deep_time = timeit.timeit(del_deep, number=self.timeit_runs)
        mean_deep = deep_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the ChainMap implementation
        normal_time = timeit.timeit(del_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_deep / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nStandard ChainMap delete item: {mean_normal:.3f} μs ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        print(
            f"DeepChainMap delete item: {mean_deep:.3f} μs "
            f"({percent:.3f}% of standard ChainMap delete item time)",
        )
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
