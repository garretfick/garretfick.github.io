---
layout: post
title: Building Wonders Without Blueprints - How AI Learned to “Understand” Language
date: 2025-05-08
---

*Note: This blog post was adapted from a Toastmasters speech I gave, with the help of AI to format and refine the text.*

Have you ever marveled at the ancient wonders of the world and realized they were built long before we had modern science—even before formal mathematics or physics existed? Throughout history, humanity has a long and impressive track record of building things before we fully understood the principles that made them work.

You might think that our modern, science-driven era is different. But surprisingly, we are still building powerful technologies that we don’t completely understand. One of the most fascinating examples today is Artificial Intelligence—especially generative AI like ChatGPT.

If you haven’t used it before, ChatGPT is a tool where you can make a request like, “I’m going to Croatia for two weeks. I enjoy outdoor activities and prefer traveling by bus. Can you create an itinerary for me?”

The AI might suggest a route that includes the city of Dubrovnik. You could then reply, “That sounds great, but can you create an itinerary that avoids Dubrovnik? It's a bit too touristy for me.” The AI can take that new information and instantly update the plan.

This seamless interaction begs a fascinating question: Does the AI actually understand the words you're using? And if so, how? Let's explore the magic behind the machine.

## At Its Heart, AI is a Prediction Engine

So, how does it all work? At its core, a large language model is a highly advanced word prediction machine. We give the AI a sequence of words and simply ask it to predict the most likely next word. We then add that predicted word to the sequence and ask it again, "What comes next?" We repeat this process, one word at a time, until it has generated a complete and satisfying response, like your Croatian travel itinerary.

From the outside, we see coherent sentences and ideas. But inside the computer, the currency isn't words; it's numbers. To make this work, we need a way to translate between the world of human language and the world of computer mathematics. This translation process is called creating an embedding. (That's the only truly technical term we'll need).

Think of an embedding as a unique recipe for each word, made up of numerical ingredients. For the word "queen," the recipe might include a pinch of ‘royalty,’ a dash of ‘femininity,’ and a spoonful of ‘power.’ It’s these complex numerical recipes that allow the AI to compare words and make sophisticated predictions.

## From Simple Numbers to Complex Meanings

Let's start with a very basic embedding. Imagine a tiny language with just five words: king, queen, man, woman, is. We could create a simple translation:

* king = 1
* queen = 2
* man = 3
* woman = 4
* is = 5

Using this system, the sentence "Queen is woman" would become the numerical sequence `2 5 4`. An AI could work with this, but it’s far too simple to capture the rich complexity of language. Words can be synonyms, have different forms (like conjugated verbs or plurals), and share abstract relationships (like 'cup' and 'coffee'). Our simple embedding doesn’t understand any of that.

To do better, we need to assign more than one number to each word. Imagine every word has a "fingerprint"—not a single number, but a long list of numbers that describes what words it typically associates with. By analyzing vast amounts of text from Wikipedia, books, and the internet, we can calculate the frequency with which words appear together. For example, 'coffee' is often seen near 'cup,' 'mug,' or 'morning.'

Even this method has flaws. The word 'queen' might never appear with 'aardvark,' yet this non-relationship would still be recorded. Much of the data is not very useful.

This is where researchers developed even smarter methods. A groundbreaking technique called Word2Vec starts by giving each word a random list of numbers. Then, it reads through billions of sentences and constantly "nudges" the numbers. When words that often appear together (like ‘queen’ and ‘royal’) are seen, their number lists are nudged to become more similar. After millions of these adjustments, words with similar meanings naturally end up with similar numerical fingerprints.

## The Magic of Word Math

In the end, each word is represented by a complex set of numbers. What do these individual numbers mean? We honestly don't know. They might represent concepts like royalty, gender, plurality, or abstract ideas we don't even have names for.

But we know they mean something, because they allow for a kind of linguistic algebra. In a now-famous example, if you take the numbers for ‘king,’ subtract the numbers for ‘man,’ and add the numbers for ‘woman,’ the resulting set of numbers is incredibly close to the numbers for ‘queen.’

```
king − man + woman ≈ queen
```

Right there, in that simple mathematical puzzle, lies the wonder of human progress. Just like the ancient builders who raised monuments before they fully understood physics, we have built something extraordinary with AI before we fully understand how it works. It took creativity, curiosity, and courage to build this modern wonder.

And perhaps that’s how true progress always begins: not with the certainty of a blueprint, but with the power of imagination.