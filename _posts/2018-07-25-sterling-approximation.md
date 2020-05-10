---
layout: post
title: Sterlings Approximation for Factorial
date: 2018-07-25
---

Sterling's approximation for the factorial function, even for small values of x.
Out of my own interest, I wanted to know how accurate it is.

$$
x! \simeq x^{x} e^{-x} \sqrt{2 \pi x}
$$

We can evaluate the accuracy for a few values of x. With the following script:

```java
// The factorial way
var factorial = 1;
var curValue = input;
while (curValue > 0) {
    factorial *= curValue;
    curValue -= 1;
}

// The Sterling way
var approx = Math.pow(input, input) * Math.pow(Math.E, -input) * Math.sqrt(2 * Math.PI * input);
```

<script>

function serlingApproximation(value) {
    var input = parseInt(document.getElementById("sterlingInput").value);

    // The factorial way
    var factorial = 1;
    var curValue = input;
    while (curValue > 0) {
        factorial *= curValue;
        curValue -= 1;
    }

    // The Sterling way
    var approx = Math.pow(input, input) * Math.pow(Math.E, -input) * Math.sqrt(2 * Math.PI * input);

    document.getElementById("sterlingFactorial").innerHTML = factorial;
    document.getElementById("sterlingApproximation").innerHTML = approx;
}



</script>

<input id="sterlingInput" type="number" value="1" onchange="serlingApproximation()"/>

<div>Factorial: <span id="sterlingFactorial"></span></div>
<div>Approximation: <span id="sterlingApproximation"></span></div>
