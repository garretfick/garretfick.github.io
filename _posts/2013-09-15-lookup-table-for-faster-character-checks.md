---
layout: post
title: Lookup Table For Faster Character Checks
date: 2013-09-15
---

Some time ago I wrote some code to check if a character was a valid VHDL identifier. The rules for a valid identifier are somewhat complex and so checking with an if statement is also complex. For one part of the identifier, the if statement would be

```
if ((charToCheck >= '0' && charToCheck <= '0')
   || (charToCheck >= 'A' && charToCheck <= 'Z')
   || (charToCheck >= 'a' && charToCheck <= 'z')
   || (charToCheck >= 192 && charToCheck <= 214)
   || (charToCheck >= 216 && charToCheck <= 246)
   || (charToCheck >= 248))
{
   //Character is valid
}
```

Instead, I decided to implement a lookup table, where I pre-calculated correct characters

```
// Valid characters encoded as a table
bool kValidCharTable[256] =
{
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//0   - 15
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//16  - 31
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//32  - 47
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,//48  - 63 (0-9)
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,//64  - 79 (A
   ...
};
if (kValidCharTable[charToCheck])
{
   //Character is valid
}
```

This of course uses more space, but I think it is more readable and it should perform faster. As I was reading Programming Pearls, it occurred to me that I could have encoded things as a bit vector to save space. Just for my interest, tried these out to see how they perform. The results were a little surprising. First I'll give the code, then summarize the results.

```
#include <stdio.h>
#include <cstring>
#include <ctime>
#include <iostream>
#include <cstdint>>
// The functions here have been carefully written so that the compiler doesn't
// optimize too much. For example, I actually calculate and return a value from
// the functions so that the compiler doesn't completely omit the code.
const long kNumInterations = 10000000L;
// Check for valid characters by the if approach
bool CheckByIf(char* charsToCheck, int numChars)
{
    bool isValid = true;

    for (int charIndex = 0; charIndex < numChars && isValid; ++charIndex)
    {
        char charToCheck = charsToCheck[charIndex];
        if (!((charToCheck >= '0' && charToCheck <= '0')
            || (charToCheck >= 'A' && charToCheck <= 'Z')
            || (charToCheck >= 'a' && charToCheck <= 'z')
            || (charToCheck >= 192 && charToCheck <= 214)
            || (charToCheck >= 216 && charToCheck <= 246)
            || (charToCheck >= 248)))
        {
            isValid = false;
        }
    }
    return isValid;
}
// Valid characters encoded as a table
bool kValidCharTable[256] =
{
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//0   - 15
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//16  - 31
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//32  - 47
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,//48  - 63 (0-9)
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,//64  - 79 (A
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,//80  - 95 -Z,_)
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,//96  - 111 (a
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,//112 - 127 -z)
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//128 - 143
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//144 - 159
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//160 - 175
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,//176 - 191
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,//192 - 207
    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,//208 - 223
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,//224 - 239
    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,//240 - 255
};
// Check for valid characters by the table approach
bool CheckByCharTable(char* charsToCheck, int numChars)
{
    bool isValid = true;
    for (int charIndex = 0; charIndex < numChars && isValid; ++charIndex)
    {
        isValid = kValidCharTable[charsToCheck[charIndex]];
    }
    return isValid;
}
// Valid characters, encoded as a bit array
std::uint64_t kValidCharBitArray[4] = {
    0x03FF000000000000,
    0x07FFFFFE87FFFFFE,
    0x0000000000000000,
    0xFF7FFFFFFF7FFFFF};
// Check for valid characters by a bit array approach
bool CheckByBitArray(char* charsToCheck, int numChars)
{
    bool isValid = true;
    for (int charIndex = 0; charIndex < numChars && isValid; ++charIndex)
    {
        char charToCheck = charsToCheck[charIndex];
        isValid = (kValidCharBitArray[charToCheck / 64] >> (charToCheck % 64)) & 1;
    }
    return isValid;
}
int main(int argc, char* argv[])
{
    int len = (argc > 1) ? strlen(argv[1]) : 0;
    bool isValidTable, isValidIf, isValidBit;
    if (len > 0)
    {
        // Run the lookup algorithm
        clock_t ifTime = clock();
        for (long iteration = 0; iteration < kNumInterations; ++iteration)
        {
            isValidIf = CheckByIf(argv[1], len);
        }
        ifTime = clock() - ifTime;
        // Run the table algorithm
        clock_t tableTime = clock();
        for (long iteration = 0; iteration < kNumInterations; ++iteration)
        {
            isValidTable = CheckByCharTable(argv[1], len);
        }
        tableTime = clock() - tableTime;
        // Run the bit algorithm
        clock_t bitTime = clock();
        for (long iteration = 0; iteration < kNumInterations; ++iteration)
        {
            isValidBit = CheckByBitArray(argv[1], len);
        }
        bitTime = clock() - bitTime;

        std::cout << "If: " << ifTime << " Valid: " << isValidIf << std::endl;
        std::cout << "Table: " << tableTime << " Valid: " << isValidTable << std::endl;
        std::cout << "Bit: " << bitTime << " Valid: " << isValidTable << std::endl;
    }
    return 0;
}
```

Intuitively, which one do you think is fastest? I ran things 3 times with the input `TheStringThatIAmCheckingForComparison`. The table below lists the result.

Function        | Time
----------------|----------
`CheckByIf`       | 1240, 1202, 1303
`CheckByTable`    | 369, 333, 332
`CheckByBitArray` | 1422, 1165, 1185

Intuitively, I expected the lookup table would be fastest, and it is. What really surprised me is how slow the bit array is. I'm glad I implemented the table instead of optimizing too much.
