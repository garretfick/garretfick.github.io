---
layout: post
title: Josephus Problem
date: 2017-05-20
---

[Josephus Problem](https://en.wikipedia.org/wiki/Josephus_problem) describes a counting-out game where you progressively remove (kill) people by their position, until only one person remains. For example, take a group of 10 people, then kill each second person until only one person remains. Josephus Problem tells us who is the survivor.

There is an analytical solution for the special case of skipping one person (k=2). Within that, there is an interesting sub-problem - you need to calculate the value of n with only the highest bit set. For that, there are both naive and efficient solutions.

The following shows how solve Josephus Problem for the special case of k=2, using both naive and efficient solutions to get highest bit set.

```c++
#include <bitset>
#include <iostream>

#if _MSC_VER && !__INTEL_COMPILER
// If we are on a MSVC compiler, we can use the MSVC intrinsic to get the highest one bit
// There are equivalent functions for GCC and LLVM (__builtin_clz)
#include <intrin.h>
#pragma intrinsic(_BitScanReverse)
#endif

/// Get the value of the integer with only the highest bit set
/// For example, 8 (100) is 8 (100). 9 (101) is 8 (100).
int highest_one_bit(int i) {
    std::cout << "Highest one bit value " << std::bitset<32>(i) << std::endl;
#if _MSC_VER && !__INTEL_COMPILER
    // Most compilers have an intrinsic function for these bit set functions.
    // On MSVC, this is _BitScanReverse. This compiles to the assembly
    // bsr eax,dword ptr [i]
    unsigned long pos = 0;
    _BitScanReverse(&pos, (unsigned long)i);

    int value = 1 << pos;
    std::cout << "Intrinsic highest bit set " << std::bitset<32>(value) << std::endl;

    return value;
#else
    // The approach here is to shift the highest bit progressively
    // to the right. Then use bitwise OR to set that bit to 1.
    // After all of these shifts, all of the bits starting from
    // the greatest bit and to the right are 1.

    i |= (i >> 1);
    i |= (i >> 2);
    i |= (i >> 4);
    i |= (i >> 8);
    i |= (i >> 16);

    // Our value is now of the form with all 1's set. For example,
    // if the original value was 00001010, the value is now 00001111.
    // To get only the highest bit set, shift one to the right, and
    // then subtract from the original value.
    int value = i - (((unsigned)i) >> 1);
    std::cout << "Naive highest bit set " << std::bitset<32>(value) << std::endl;

    return value;
#endif
}

/// Calculates the safe position for the Josephus problem for the special
/// case of k=2 (where we kill each second person)
int josephus_problem_2(int n) {
    // f(N) = 2L + 1 where N =2^M + L and 0 <= L < 2^M
    // find value of L for the equation
    int l_val = n - highest_one_bit(n);
    return 2 * l_val + 1;
}

int main()
{
    std::cout << "Answer " << josephus_problem_2(10) << std::endl;
    return 0;
}
```