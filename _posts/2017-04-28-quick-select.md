---
layout: post
title: Quick Select
date: 2017-04-28
---

Quick select is an efficient algorithm for finding the k-th item in a list. The following is a simple implementation to find the k-th smallest item from a list of integers.

I've kept the example simple and concrete (instead of with templates) to focus on the algorithm.

```c++
#include <iostream>
#include <cmath>
#include <utility>

/// Sorts the list about the value of the pivot index.
/// After this function completes, the items to the left of the pivotIndex
/// are all less than the value at the pivotIndex and the items to the right
/// of the pivotIndex are all greater than the value at the pivotIndex
///
/// @param items The items that we want to sort in place
/// @param left The index of the leftmost value in items to partition
/// @param right The index of the rightmost value in items to partition
/// @param pivotIndex The index to parition about
///
/// @return The final index of the pivot value
int partition(int* items, int left, int right, int pivotIndex)
{
    // Take the item at our pivot index (our randomly selected midpoint)
    // and move it to the end of the items
    int pivotValue = items[pivotIndex];
    std::swap(items[pivotIndex], items[right]);
    int storeIndex = left;

    // Now sort the items in the middle so that all of the values
    // less that the pivot values will be to the left and all
    // of the values larger than the pivot value will be to the
    // right of the pivot
    for (int i = left; i < right - 1; ++i) {
        if (items[i] < pivotValue) {
            std::swap(items[storeIndex], items[i]);
            storeIndex++;
        }
    }

    // Finally move the pivot to the correct position
    std::swap(items[right], items[storeIndex]);

    for (int i = left;  i < right; ++i) {
        std::cout << items[i] << ' ';
    }
    std::cout << std::endl;
    std::cout << pivotValue << std::endl;

    return storeIndex;
}

/// Select the k-th smallest value from items. This will sort the items in place
/// without allocating any new memory
///
/// @param items The items to select from
/// @param left The index of the leftmost value in items to partition
/// @param right The index of the rightmost value in items to partition
/// @param k The index of the item to find, starting from 0
///
/// @return the k-th smallest value
int select(int* items, int left, int right, int k)
{
    // If we have no more items to search from, then this is the value
    if (left == right) {
        return items[left];
    }

    // Pick a random index (value) to partition the items
    int pivotIndex = left + std::floor(rand() % (right - left + 1));

    // Now for the partition index, we will get the value at that index
    // and then reposition the items in the array so that all the items
    // smaller than the value at pivotIndex are less than the value and
    // all the items greater than the value at pivotIndex are greater
    // than the value. The returns the final position of the pivotIndex
    pivotIndex = partition(items, left, right, pivotIndex);

    // We know that the value at pivotIndex is in the correct position, so
    // if it's position is k, then this is the value we want
    if (k == pivotIndex) {
        return items[k];
    }

    // Similarly, since we know that the value at pivotIndex is in the correct
    // position, if the position is greater that what we want to find, then
    // we know k-th value is to the left so we can focus only on that part
    // of the array
    if (k < pivotIndex) {
        return select(items, left, pivotIndex - 1, k);
    }

    // Lastly, since we know that the vlaue at pivotIndex is in the correct
    // position, then the k-th value must be to the right (since k > pivotIndex)
    return select(items, pivotIndex + 1, right, k);
}


int main()
{
    int items[] = { 6, 5, 1, 0, 4, 75, 98, 14, 25, 22, 29, 41 };

    std::cout << select(items, 0, sizeof(items) / sizeof(items[0]) - 1, 4);

    return 0;
}
```
