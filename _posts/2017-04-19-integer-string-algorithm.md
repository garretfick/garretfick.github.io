---
layout: post
title: Integer to String Algorithm
date: 2017-04-19
---

The following is a simple example for now to convert an integer to a string (doesn't include error checking, sign detection, non-base 10).

```c++
#include <cstdint>
#include <iostream>
#include <string>

/// Reverses the characters in the string
/// @param str The string to reverse (the original string is modified)
/// @return The reversed string
std::string reverse(std::string& str)
{
    std::string::size_type half = str.size() / 2;
    std::string::size_type end = str.size() - 1;

    for (std::string::size_type i = 0; i < half; ++i) {
        char tmp = str[i];
        str[i] = str[end - i];
        str[end - i] = tmp;
    }

    return str;
}

/// Convert the number to a string
/// @param num The number to convert (assumed to be positive)
/// @return The converted number
std::string int_to_string(int num)
{
    auto result = std::string();

    // We want to process from reverse, that's much easier
    while (num != 0) {
        // Process each digit one at a time
        int rem = num % 10;

        // In C/C++, this addition just gives
        // us the right char value for the character
        result.push_back('0' + rem);

        num /= 10;
    }

    return reverse(result);
}

int main()
{
    auto result = int_to_string(3017);
    std::cout << result;
    return 0;
}
```