---
layout: post
title: Perceptron Training Algorithm
date: 2018-12-23
---

A perceptron is a linear binary classifier. That is, it is an algorithm that takes a vector
of inputs and produces a single true or false value representing whether the input vector
is within the set.

```
   (x1) ─────> (w1) ────┐
                        │
                        └─>┌───┐      ┌────┐
   (x2) ─────> (w2) ──────>│ ∑ │─────>│>θ ?│─────> (y)
                        ┌─>└───┘      └────┘
                        │
   (x3) ─────> (w3) ────┘
```

which is this equivalent of writing

```
y = 1 if ∑(wi xi) ≥ 0
```

For mathematical simplicity, we can treat θ as an input

```
   (x0) ─────> (-θ) ─────────┐
                             │
                             │
   (x1) ─────> (w1) ────┐    │
                        │    v
                        └─>┌───┐      ┌────┐
   (x2) ─────> (w2) ──────>│ ∑ │─────>│>0 ?│─────> (y)
                        ┌─>└───┘      └────┘
                        │
   (x3) ─────> (w3) ────┘
```

-θ is then known as the bias.

In order to use a perceptron, we need weights. These can be discovered
by the perceptron learning algorithm. This can be expressed in Python as shown below.

```py
# Create a data set that we want to train on. For this example
# we want to train on an AND boolean function.
and_training_set = []
and_training_set.append([1, 1])
and_training_set.append([1, 0])
and_training_set.append([0, 1])
and_training_set.append([0, 0])
and_labels = [1, 0, 0, 0]

learning_rate = 0.1

def predict(inputs, weights):
    # This multiplies each input but its appropriate weight and sums
    # them up. The bias weight is special because it's "input" is
    # always 1, so it is directly added to the list.
    val = sum([a*b for a,b in zip(inputs, weights[1:])]) + weights[0]

    # Finally, return the activation value as a Boolean value
    return 1 if val >= 0 else 0

def train(input_data, labels):
    # There is a weight for value in the input vector
    # plus one for the bias. We initialize the weights
    # to 0 for each value.
    weights = [0] * (len(and_training_set[0]) + 1)

    # Then randomly select inputs, update the weights if the output
    # was incorrect. We continue this procedure until all values are
    # classified correctly. Since we want to select randomly, and
    # input data is already random, we can just iterate over our
    # inputs until correctly classified.

    converged = False
    while not converged:
        # Iterate over all the samples - if we find any that is
        # not correct, then we set converged to False so we will
        # try again
        converged = True

        # Create pairs of the inputs and the label for that input vector
        # and iterate over the entire set.
        for inputs, label in zip(input_data, labels):
            prediction = predict (inputs, weights)

            if prediction != label:
                # If the prediction wasn't correct, then we have not yet
                # converged and will need to iterate again
                converged = False

                error = learning_rate * (label - prediction)

                # As per the algorithm, we also update our weights based
                # on the inputs and our prediction. To make this easy in Python
                # make an array with the bias and inputs. The bias goes first
                # since we have defined our first weight to be for the bias
                bias_inputs = [1] + inputs
                # Combine that with the weights that we just used
                weights = [(weight + error * input_val) for (weight, input_val) in zip(weights, bias_inputs)]

    return weights

weights = train(and_training_set, and_labels)

# Finally, we can use the weights to make predictions
prediction = predict([1, 0], weights)
```

The algorithm works so long as the data is linearly separable. This means that it is
possible to draw a line (with constant slope) that separates the regions. If not, then
this algorithm will not converged.

The Boolean function XOR is not linearly separable, and many practical problems do not
satisfy this requirement. In general, it is not known in advance whether the data is
linearly separable, so this algorithm leaves something to be desired.
