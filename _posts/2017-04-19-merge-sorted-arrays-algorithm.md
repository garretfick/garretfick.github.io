---
layout: post
title: Merge Sorted Arrays Algorithm
date: 2017-04-19
---

The following is a simple algorithm to merge two sorted arrays. Merging two sorted arrays is essentially the same as a single round in merge sort.

If you were implementing this in a real project, you would probably was to use templates so this
could work with any type. I've restricted this to only unsigned ints to focus on the algorithm.

```c++
#include <iostream>
#include <cstdint>
#include <vector>

/// Merge two sorted arrays
/// @param array1 The first sorted array to merge
/// @param array2 The second sorted array to merge
/// @return A new array containing the merged result
std::vector<std::uint16_t> merge(std::vector<std::uint16_t>& array1, std::vector<std::uint16_t>& array2)
{
    std::uintptr_t index1 = 0;
    std::uintptr_t index2 = 0;

    auto merged = std::vector<std::uint16_t>();
    merged.reserve(array1.size() + array2.size());

    // Traverse the arrays while there are still items in both
    while (index1 < array1.size() && index2 < array2.size()) {
        if (array1[index1] < array2[index2]) {
            // Yes you can use post increment on the same line,
            // but I think it is easier to read it on two lines
            merged.push_back(array1[index1]);
            index1++;
        } else {
            merged.push_back(array2[index2]);
            index2++;
        }
    }

    // Now we have exhausted one of the arrays, so we need to empty
    // the remaining array. There must be a way to do this faster in c++?
    while (index1 < array1.size()) {
        merged.push_back(array1[index1]);
        index1++;
    }

    while (index2 < array2.size()) {
        merged.push_back(array2[index1]);
        index2++;
    }

    return merged;
}


int main()
{
    std::vector<std::uint16_t> one = { 1, 2, 5, 9, 19, 30 };
    std::vector<std::uint16_t> two = { 3, 4, 5, 8, 21 };

    auto merged = merge(one, two);
    for (auto it = merged.begin(); it != merged.end(); ++it) {
        std::cout << (*it) << std::endl;
    }
}

```