---
layout: post
title: Isomorphic Strings
date: 2017-05-06
---

The program below is a simple example of testing whether two strings are isomorphic. Isomorphic means there is a straight mapping between the two strings.

This example uses a simple "bitmap" to define and check the mapping between the two strings. It works when the input set is small because the map is small and can be allocated upfront.

As with other examples, the purpose of this example is to show a simple way to solve the problem. I have generally excluded boundary condition testing, use of templates, and other things you might do to make this generally more useful.

```
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>

const std::uintptr_t SIZE = 256;

bool is_isomorphic(const std::string& first, const std::string& second)
{
    if (first.size() != second.size()) {
        return false;
    }

    // Declare a char map - the index is the character from first
    // and the value is the character from second.
    // We could of course use another data structure, but this is
    // efficient so long as we don't have many characters to lookup
    char map[SIZE];
    std::fill(std::begin(map), std::end(map), 0);

    for (std::string::size_type i = 0; i < first.size(); ++i) {
        char char1 = first[i];
        char char2 = second[i];

        if (map[char1]) {
            // If we have te first one, then we check that the second is equal
            if (map[char1] != char2) {
                return false;
            }
        }
        else {
            // Otherwise, set the value since this is the first time we have seen
            // this character
            map[char1] = char2;
        }
    }

    // If we didn't find any characters that don't map correctly, then we succeeded
    return true;
}

int main()
{
    std::string foo = "foo";
    std::string baa = "baa";
    std::string bar = "bar";

    std::cout << foo << " and " << baa << " are " << is_isomorphic(foo, baa);
    std::cout << foo << " and " << bar << " are " << is_isomorphic(foo, bar);

    return 0;
}
```