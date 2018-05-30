---
layout: post
title: Visitor Versus "is" Cast in C#
date: 2013-09-03
---

Obviously C# is not C++, and so it is important to not simply assume that things true in C++ are also true in C#. A good question is the cost of the [is operator](http://msdn.microsoft.com/en-us/library/scekt9xw%28v=vs.110%29.aspx) compared to a [virtual (or abstract) function](http://msdn.microsoft.com/en-us/library/9fkccyh4.aspx). Is a visitor better than casting? This is pretty easy to test, but I couldn't find any good post about this, so I wrote it myself.

A few things should affect the result. Most importantly, the speed of the cast approach depends on the number of `if` tests you have to do, or equivalently, the number of failed tests. The more classes you have to test, the slower things should be. The result might also depend on class hierarchy depth. To test this out, I designed the following class hierarchy.

![](/static/img/blog/visitor-versus-cast-s-in-c/c-sharp-visitor.png)

I then wrote to code to either cast via `is` or call a visitor function. Everything except the `Circle` class can be entirely removed from the code by conditional compiles. This way, I can test the effects of adding more classes or increating the class hierarchy depth and this is detailed in the table below.

<table>
<thead>
<tr><th>Classes</th><th>Visitor Time (ms)</th><th>Visitor Average</th><th>Cast Time (ms)</th><th>Cast Average</th><th>Fastest</th></tr>
</thead>
<tbody>
<tr>
<td>Circle</td>
<td>
<p>1218<br />1233<br />1176</p>
</td>
<td>
<p>0.12</p>
</td>
<td>
<p>798<br />802<br />807</p>
</td>
<td>
<p>0.08</p>
</td>
<td>
<p>Cast</p>
</td>
</tr>
<tr>
<td>Circle<br />Square</td>
<td>
<p>2259<br />2242<br />2520</p>
</td>
<td>
<p>0.12</p>
</td>
<td>
<p>1890<br />1898<br />1903</p>
</td>
<td>
<p>0.09</p>
</td>
<td>
<p>Cast</p>
</td>
</tr>
<tr>
<td>
<p>Circle<br />Square<br />RoundedSquare</p>
</td>
<td>
<p>3339<br />3337<br />3305</p>
</td>
<td>
<p>0.11</p>
</td>
<td>
<p>3769<br />3780<br />3766</p>
</td>
<td>
<p>0.13</p>
</td>
<td>
<p>Visitor</p>
</td>
</tr>
<tr>
<td>
<p>Circle<br />Square<br />Hexagon</p>
</td>
<td>
<p>3286<br />3581<br />3301</p>
</td>
<td>
<p>0.11</p>
</td>
<td>
<p>3693<br />3718<br />3681</p>
</td>
<td>
<p>0.12</p>
</td>
<td>
<p>Visitor</p>
</td>
</tr>
<tr>
<td>
<p>Circle<br />Square<br />RoundedSquare<br />Hexagon</p>
</td>
<td>
<p>4501<br />4592<br />4649</p>
</td>
<td>
<p>0.11</p>
</td>
<td>
<p>5703<br />5672<br />5662</p>
</td>
<td>
<p>0.14</p>
</td>
<td>
<p>Visitor</p>
</td>
</tr>
<tr>
<td>
<p>Circle<br />Square<br />RoundedSquare<br />Hexagon<br />Octagon</p>
</td>
<td>
<p>5541<br />5649<br />5534</p>
</td>
<td>
<p>0.11</p>
</td>
<td>
<p>7920<br />7950<br />7958</p>
</td>
<td>
<p>0.16</p>
</td>
<td>
<p>Visitor</p>
</td>
</tr>
</tbody>
</table>

Times increase with each addition because the total number of objects increases, so the important number is the average. The loop is also run 10000 times so that the times are much larger than the timer resolution of 1 ms.

Overall, the results are not that unexpected. As you add more types, the number of failed if's increases, and the performance degredates. The visitor stays the same. Interestingly, at the lowest end, the cast is faster than the visitor, and so for simple checks, the better choice might be the cast.

You can see the full source below.

```
// Comment the conditional compile lines below to 
// remove particular types from the object hierarchy
#define SQUARE
#define ROUNDEDSQUARE
#define HEXAGON
#define OCTAGON
 
using System;
using System.Collections.Generic;
using System.Diagnostics;
 
namespace VisitorVsCast
{
    /// <summary>
    /// The visitor interface
    /// </summary>
    public interface IVisitor
    {
        void VisitCircle(Circle circle);
#if SQUARE
        void VisitSquare(Square square);
#endif
#if ROUNDEDSQUARE
        void VisitRoundedSquare(RoundedSquare square);
#endif
#if HEXAGON
        void VisitHexagon(Hexagon hexagon);
#endif
#if OCTAGON
        void VisitOctagon(Octagon octagon);
#endif
    }
 
    /// <summary>
    /// Base class for all shapes
    /// </summary>
    public abstract class Shape
    {
        public abstract void AcceptVisitor(IVisitor visitor);
    }

    /// <summary>
    /// A circle
    /// </summary>
    public class Circle : Shape
    {
        public override void AcceptVisitor(IVisitor visitor)
        {
            visitor.VisitCircle(this);
        }
    }

#if SQUARE
    /// <summary>
    /// A square shape
    /// </summary>
    public class Square : Shape
    {
        public override void AcceptVisitor(IVisitor visitor)
        {
            visitor.VisitSquare(this);
        }
    }
#endif
 
#if ROUNDEDSQUARE
    /// <summary>
    /// A rounded square (a square with round corners)
    /// </summary>
    public class RoundedSquare : Square
    {
        public override void AcceptVisitor(IVisitor visitor)
        {
            visitor.VisitRoundedSquare(this);
        }
    }
#endif

#if HEXAGON
    public class Hexagon : Shape
    {
        public override void AcceptVisitor(IVisitor visitor)
        {
            visitor.VisitHexagon(this);
        }
    }
#endif

#if OCTAGON
    public class Octagon : Shape
    {
        public override void AcceptVisitor(IVisitor visitor)
        {
            visitor.VisitOctagon(this);
        }
    }
#endif

    /// <summary>
    /// Counting visitor
    /// </summary>
    public class CountingVisitor : IVisitor
    {

        public void VisitCircle(Circle circle)
        {
        }

#if SQUARE
        public void VisitSquare(Square square)
        {
        }
#endif

#if ROUNDEDSQUARE
        public void VisitRoundedSquare(RoundedSquare square)
        {
        }
#endif

#if HEXAGON
        public void VisitHexagon(Hexagon hexagon)
        {
        }
#endif

#if OCTAGON
        public void VisitOctagon(Octagon octagon)
        {
        }
#endif
    }

    class Program
    {
        static int NumObjectsPerCategory = 10000;
        static int NumIterations = 10000;

        static void Main(string[] args)
        {
            long visitorTime = 0;
            long castTime = 0;

            // Create a list with lots of shapes. It doesn't matter the order
            // of the shapes, but that we have a bunch
            List<Shape> shapes = new List<Shape>();
            shapes.Capacity += 5 * NumObjectsPerCategory;
            for (int i = 0; i < NumObjectsPerCategory; ++i)
            {
                shapes.Add(new Circle());
            }
#if SQUARE
            for (int i = 0; i < NumObjectsPerCategory; ++i)
            {
                shapes.Add(new Square());
            }
#endif
#if ROUNDEDSQUARE
            for (int i = 0; i < NumObjectsPerCategory; ++i)
            {
                shapes.Add(new RoundedSquare());
            }
#endif
#if HEXAGON
            for (int i = 0; i < NumObjectsPerCategory; ++i)
            {
                shapes.Add(new Hexagon());
            }
#endif
#if OCTAGON
            for (int i = 0; i < 10000; ++i)
            {
                shapes.Add(new Octagon());
            }
#endif

            visitorTime = CountByVisitor(shapes);
            castTime = CountByCast(shapes);

            Console.WriteLine("Visitor: {0}", visitorTime);
            Console.WriteLine("Cast: {0}", castTime);
        }

        /// <summary>
        /// Iterate them by the visitor
        /// </summary>
        /// <param name="shapes"></param>
        /// <returns></returns>
        static long CountByVisitor(List<Shape> shapes)
        {
            CountingVisitor visitor = new CountingVisitor();

            Stopwatch sw = Stopwatch.StartNew();

            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (Shape shape in shapes)
                {
                    shape.AcceptVisitor(visitor);
                }
            }

            return sw.ElapsedMilliseconds;
        }

        /// <summary>
        /// Iterate them by cast
        /// </summary>
        /// <param name="shapes"></param>
        /// <returns></returns>
        static long CountByCast(List<Shape> shapes)
        {
            Stopwatch sw = Stopwatch.StartNew();

            for (int i = 0; i < NumIterations; ++i)
            {
                foreach (Shape shape in shapes)
                {
                    if (shape is Circle)
                    {
                    }
#if ROUNDEDSQUARE
                    else if (shape is RoundedSquare)
                    {
                    }
#endif
#if SQUARE
                    else if (shape is Square)
                    {
                    }
#endif
#if HEXAGON
                    else if (shape is Hexagon)
                    {
                    }
#endif
#if OCTAGON
                else if (shape is Octagon)
                {
                }
#endif
                }
            }

            return sw.ElapsedMilliseconds;
        }

    }
}
```