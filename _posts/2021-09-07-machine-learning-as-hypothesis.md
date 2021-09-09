---
layout: post
title: Machine Learning Models as Hypothesis
date: 2021-09-07
---

It is common when describing neural networks (a subset of machine learning) to
use the character $$h$$ as the output from a perceptron, as in:

$$
h = g(a)
$$

*h* here stands for hypothesis. Literature explains the output of a perceptron
as a classification or likelihood in the output given the input.

I like to see analogs in other domains and it occurred that machine learning
models are very much hypotheses, such as those from physics. Newton's second
law tells us that the acceleration of an object depends on the
mass of the object and the amount of force applied, namely

$$
F = ma
$$

This is very much a hypothesis. It is a mathematical model that enables us to
make predictions. Given an observed mass and acceleration, we can predict the
applied force. Einsten's Theory of Special Relativity is another such
hypothesis.

How then does this relate to machine learning models and $$h$$? The machine
learned model is nothing more than a hypothesis. It purports to enable us to
make predictions about the world. Sometimes the predictions are correct other
times the model lacks fidelity and makes incorrect predictions. In all cases
though, the output is the result of a hypothesis.
