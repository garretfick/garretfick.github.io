---
layout: post
title: Fun with Octagons
date: 2012-11-19
---

I've been looking at the [IPC-2581A specification](http://www.ipc-2581.com/) for representing PCB data. The XML format defines quite a few shapes, including octagons, but I was intrigued to find that octagons in IPC-2581A are defined quite differently from most resources. IPC-2581A defines an octagon in terms of the circumscribed diameter, whereas most geometry resources define octagons in terms of a side length.

![](/static/img/blog/fun-with-octagons/ipc2581_octagon.png)

For programming (and drawing), I need to know the location of each vertex. It turns out defining the octagon in terms of a circumscribed diameter makes calculating the location of each vertex trivial.

The centre of the octagon is located at C, and it is characterized by the circumscribed diameter L. The points located at the top, bottom, left, and right are easy to calculate because they are offset by L/2. The other points are a little less obvious.

We can figure out the location of these points by drawing the blue triangle from the center of the circle to one vertex. We know the length of the sides to the vertices is L/2. We know the interior angle, θ, of the triangle is 45° (360° / 8 triangles).

Now, let's draw a right triangle where the hypotenuse is from the centre to vertex. We can then use trigonometry to calculate x and y. x and y are the same since it is a isosceles triangle.

![](/static/img/blog/fun-with-octagons/vertex_location.png)

From the diagram, we can see that x = y = (L/2) sin(45) = 0.3535 L