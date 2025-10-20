#!/usr/bin/env python
"""basedict_performance.py
Performance tests for the BaseDict class in the baseobjects.bases.collections package.
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
import timeit
from collections import UserDict
from typing import Any, Dict, List

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases.collections import BaseDict
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestBaseDictPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseDict class.

    This test suite measures the performance of various operations on BaseDict objects
    and compares them with standard Python dictionaries and UserDict.
    """

    # Class Definitions #
    class TestDict(BaseDict):
        """A concrete subclass of BaseDict for testing purposes."""

    # Attributes #
    timeit_runs: int = 100000
    dict_size: int = 100  # Size of dictionaries for performance tests

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dict(self) -> "TestBaseDictPerformance.TestDict":
        """Create a test dictionary instance for use in tests.

        Returns:
            TestDict: An instance of the test class with some initial data.
        """
        return self.TestDict({f"key_{i}": f"value_{i}" for i in range(self.dict_size)})

    @pytest.fixture
    def test_user_dict(self) -> UserDict:
        """Create a UserDict instance for comparison.

        Returns:
            UserDict: A UserDict instance with the same initial data as test_dict.
        """
        return UserDict({f"key_{i}": f"value_{i}" for i in range(self.dict_size)})

    @pytest.fixture
    def test_std_dict(self) -> dict[str, str]:
        """Create a standard dictionary for comparison.

        Returns:
            Dict[str, str]: A standard dictionary with the same initial data as test_dict.
        """
        return {f"key_{i}": f"value_{i}" for i in range(self.dict_size)}

    # Tests
    def test_creation_performance(self) -> None:
        """Test the performance of creating BaseDict instances.

        This test compares the speed of creating BaseDict instances with creating
        standard Python dictionaries and UserDict instances.
        """
        init_data = {f"key_{i}": f"value_{i}" for i in range(self.dict_size)}

        def create_base_dict() -> None:
            self.TestDict(init_data)

        def create_user_dict() -> None:
            UserDict(init_data)

        def create_std_dict() -> None:
            dict(init_data)

        # Calculate the mean time in microseconds for BaseDict creation
        base_time = timeit.timeit(create_base_dict, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserDict creation
        user_time = timeit.timeit(create_user_dict, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict creation
        std_time = timeit.timeit(create_std_dict, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict creation: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict creation: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict creation: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict creation time, {percent_std:.3f}% of standard dict creation time)",
        )
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard dict

    def test_get_item_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of getting items from dictionaries.

        This test compares the speed of getting items from BaseDict with getting items from
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """
        # Use a key that exists in all dictionaries
        key = "key_50"

        def get_base_dict_item() -> None:
            _ = test_dict[key]

        def get_user_dict_item() -> None:
            _ = test_user_dict[key]

        def get_std_dict_item() -> None:
            _ = test_std_dict[key]

        # Calculate the mean time in microseconds for BaseDict item access
        base_time = timeit.timeit(get_base_dict_item, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserDict item access
        user_time = timeit.timeit(get_user_dict_item, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict item access
        std_time = timeit.timeit(get_std_dict_item, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict item access: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict item access: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict item access: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict item access time, {percent_std:.3f}% of standard dict item access time)",
        )
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard dict

    def test_set_item_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of setting items in dictionaries.

        This test compares the speed of setting items in BaseDict with setting items in
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """
        # Use a key that will be set in all dictionaries
        key = "new_key"
        value = "new_value"

        def set_base_dict_item() -> None:
            test_dict[key] = value

        def set_user_dict_item() -> None:
            test_user_dict[key] = value

        def set_std_dict_item() -> None:
            test_std_dict[key] = value

        # Calculate the mean time in microseconds for BaseDict item setting
        base_time = timeit.timeit(set_base_dict_item, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserDict item setting
        user_time = timeit.timeit(set_user_dict_item, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict item setting
        std_time = timeit.timeit(set_std_dict_item, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict item setting: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict item setting: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict item setting: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict item setting time, {percent_std:.3f}% of standard dict item setting time)",
        )
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard dict

    def test_delete_item_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of deleting items from dictionaries.

        This test compares the speed of deleting items from BaseDict with deleting items from
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """
        # Use a key that exists in all dictionaries and will be deleted
        keys = [f"key_{i}" for i in range(self.dict_size)]

        def delete_base_dict_item() -> None:
            key = keys.pop(0)
            del test_dict[key]
            keys.append(key)  # Put the key back at the end for reuse

        def delete_user_dict_item() -> None:
            key = keys.pop(0)
            del test_user_dict[key]
            keys.append(key)  # Put the key back at the end for reuse

        def delete_std_dict_item() -> None:
            key = keys.pop(0)
            del test_std_dict[key]
            keys.append(key)  # Put the key back at the end for reuse

        # Calculate the mean time in microseconds for BaseDict item deletion
        base_time = timeit.timeit(delete_base_dict_item, number=min(self.timeit_runs, self.dict_size))
        mean_base = base_time / min(self.timeit_runs, self.dict_size) * 1000000

        # Reset the keys list
        keys = [f"key_{i}" for i in range(self.dict_size)]

        # Calculate the mean time in microseconds for UserDict item deletion
        user_time = timeit.timeit(delete_user_dict_item, number=min(self.timeit_runs, self.dict_size))
        mean_user = user_time / min(self.timeit_runs, self.dict_size) * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Reset the keys list
        keys = [f"key_{i}" for i in range(self.dict_size)]

        # Calculate the mean time in microseconds for standard dict item deletion
        std_time = timeit.timeit(delete_std_dict_item, number=min(self.timeit_runs, self.dict_size))
        mean_std = std_time / min(self.timeit_runs, self.dict_size) * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict item deletion: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict item deletion: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict item deletion: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict item deletion time, {percent_std:.3f}% of standard dict item deletion time)",
        )
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard dict

    def test_iteration_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of iterating over dictionaries.

        This test compares the speed of iterating over BaseDict with iterating over
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """

        def iterate_base_dict() -> None:
            for _ in test_dict:
                pass

        def iterate_user_dict() -> None:
            for _ in test_user_dict:
                pass

        def iterate_std_dict() -> None:
            for _ in test_std_dict:
                pass

        # Calculate the mean time in microseconds for BaseDict iteration
        base_time = timeit.timeit(iterate_base_dict, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserDict iteration
        user_time = timeit.timeit(iterate_user_dict, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict iteration
        std_time = timeit.timeit(iterate_std_dict, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict iteration: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict iteration: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict iteration: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict iteration time, {percent_std:.3f}% of standard dict iteration time)",
        )
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard dict

    def test_copy_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of copying dictionaries.

        This test compares the speed of copying BaseDict with copying
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """

        def copy_base_dict() -> None:
            test_dict.copy()

        def copy_user_dict() -> None:
            copy.copy(test_user_dict)

        def copy_std_dict() -> None:
            test_std_dict.copy()

        # Calculate the mean time in microseconds for BaseDict copy
        base_time = timeit.timeit(copy_base_dict, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserDict copy
        user_time = timeit.timeit(copy_user_dict, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict copy
        std_time = timeit.timeit(copy_std_dict, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard dict copy: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserDict copy: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict copy: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict copy time, {percent_std:.3f}% of standard dict copy time)",
        )
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard dict

    def test_deepcopy_performance(
        self,
        test_dict: "TestBaseDictPerformance.TestDict",
        test_user_dict: UserDict,
        test_std_dict: dict[str, str],
    ) -> None:
        """Test the performance of deep copying dictionaries.

        This test compares the speed of deep copying BaseDict with deep copying
        standard Python dictionaries and UserDict instances.

        Args:
            test_dict: A fixture providing a TestDict instance.
            test_user_dict: A fixture providing a UserDict instance.
            test_std_dict: A fixture providing a standard dictionary.
        """

        def deepcopy_base_dict() -> None:
            test_dict.deepcopy()

        def deepcopy_user_dict() -> None:
            copy.deepcopy(test_user_dict)

        def deepcopy_std_dict() -> None:
            copy.deepcopy(test_std_dict)

        # Calculate the mean time in microseconds for BaseDict deepcopy
        base_time = timeit.timeit(deepcopy_base_dict, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for UserDict deepcopy
        user_time = timeit.timeit(deepcopy_user_dict, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_user = user_time / (self.timeit_runs // 10) * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard dict deepcopy
        std_time = timeit.timeit(deepcopy_std_dict, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_std = std_time / (self.timeit_runs // 10) * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict deepcopy: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"UserDict deepcopy: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard dict)")
        print(
            f"BaseDict deepcopy: {mean_base:.3f} μs ({percent_user:.3f}% of UserDict deepcopy time, {percent_std:.3f}% of standard dict deepcopy time)",
        )
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserDict
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard dict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
