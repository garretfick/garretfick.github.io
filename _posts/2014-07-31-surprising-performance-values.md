---
layout: post
title: The Surprising Performance of Values
date: 2014-07-31
---

Sometimes you find yourself needing to iterate over all items in a [`Dictionary`](http://msdn.microsoft.com/en-us/library/xfhwa508%28v=vs.110%29.aspx). And in those cases, sometimes you don't care about the keys - you only care about the values.

There are two ways you can accomplish this:

1. Iterate over the key-value pairs
2. Iterate over just the values

Is there a difference in performance? And if so, which one do you think executes faster?

Intuitively, I though iterating over the key-value pairs should be faster because I expected the dictionary stores these, and so there might be less work to iterate over the key-value pairs.

A quick program I wrote showed me how wrong I was.

```
using System;
using System.Collections.Generic;
using System.Diagnostics;
namespace DictionaryValues
{
    class Program
    {
        private const long NumIterations = 10000;
        private const long NumValues = 10000;
        static void Main(string[] args)
        {
            RunTestWithBoxing();
            RunTestNoBoxing();
        }
        private static void RunTestWithBoxing()
        {
            // Insert some randomization to throw off the optimizer
            var random = new Random();
            int sumByPairs = 0;
            int sumByValues = 0;
            // Populate the dictionary
            Dictionary<int, int%gt; dictionary = new Dictionary<int, int>();
            for (int i = 0; i < NumValues; ++i)
            {
                int val = random.Next();
                dictionary.Add(i, val);
            }
            // Use the pairs
            Stopwatch sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var key in dictionary)
                {
                    sumByPairs += key.Value;
                }
            }
            long pairsTime = sw.ElapsedMilliseconds;
            // Use the values
            sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var value in dictionary.Values)
                {
                    sumByValues += value;
                }
            }
            long valuesTime = sw.ElapsedMilliseconds;
            Trace.WriteLine(string.Format("Sums: {0}, {1}", sumByPairs, sumByValues));
            Trace.WriteLine(string.Format("Boxing Pairs Time: {0}", pairsTime));
            Trace.WriteLine(string.Format("Boxing Values Time: {0}", valuesTime));
            Trace.WriteLine(string.Format("Boxing Pairs Time / Boxing Values Time: {0}", (double)pairsTime / valuesTime));
        }
        public class Test
        {
            public int Value { get; set; }
        }
        private static void RunTestNoBoxing()
        {
            // Insert some randomization to throw off the optimizer
            var random = new Random();
            // Populate the dictionary
            Dictionary<Test, Test> dictionary = new Dictionary<Test, Test>();
            for (int i = 0; i < NumValues; ++i)
            {
                int val = random.Next();
                dictionary.Add(new Test { Value = i }, new Test { Value = val });
            }
            RunTestNoBoxingConcrete(dictionary);
            RunTestNoBoxingInterface(dictionary);
        }
        public static void RunTestNoBoxingConcrete(Dictionary<Test, Test> dictionary)
        {
            int sumByPairs = 0;
            int sumByValues = 0;
            // Use the pairs
            Stopwatch sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var key in dictionary)
                {
                    sumByPairs += key.Value.Value;
                }
            }
            long pairsTime = sw.ElapsedMilliseconds;
            // Use the values
            sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var value in dictionary.Values)
                {
                    sumByValues += value.Value;
                }
            }
            long valuesTime = sw.ElapsedMilliseconds;
            Trace.WriteLine(string.Format("Concrete Sums: {0}, {1}", sumByPairs, sumByValues));
            Trace.WriteLine(string.Format("Noboxing Pairs Time: {0}", pairsTime));
            Trace.WriteLine(string.Format("Noboxing Values Time: {0}", valuesTime));
            Trace.WriteLine(string.Format("Noboxing Pairs Time / Noboxing Values Time: {0}", (double)pairsTime / valuesTime));
        }
        public static void RunTestNoBoxingInterface(IDictionary<Test, Test> dictionary)
        {
            int sumByPairs = 0;
            int sumByValues = 0;
            // Use the pairs
            Stopwatch sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var key in dictionary)
                {
                    sumByPairs += key.Value.Value;
                }
            }
            long pairsTime = sw.ElapsedMilliseconds;
            // Use the values
            sw = Stopwatch.StartNew();
            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (var value in dictionary.Values)
                {
                    sumByValues += value.Value;
                }
            }
            long valuesTime = sw.ElapsedMilliseconds;
            Trace.WriteLine(string.Format("Interface Sums: {0}, {1}", sumByPairs, sumByValues));
            Trace.WriteLine(string.Format("Noboxing Pairs Time: {0}", pairsTime));
            Trace.WriteLine(string.Format("Noboxing Values Time: {0}", valuesTime));
            Trace.WriteLine(string.Format("Noboxing Pairs Time / Noboxing Values Time: {0}", (double)pairsTime / valuesTime));
        }
    }
}
```

When you run this, you'll find that the key-value pair is about 2-2.5 times slower.

Since Microsoft releases [their source code](http://referencesource.microsoft.com/#mscorlib/system/collections/generic/dictionary.cs) it is easy to see why iterating over the values is faster. The dictionary doesn't store key-value pairs, so it must construct it for each item, whereas the values can just return the values.

Knowing how things and checking the performance again reaps benefits and I'll be using [Values](http://msdn.microsoft.com/en-us/library/ekcfxy3x%28v=vs.110%29.aspx) if I only care about the values.