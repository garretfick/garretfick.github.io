---
layout: post
title: Testing Asynchronous Behaviour in Java with Countdown Latch
date: 2018-09-09
---

The popularity of reactive programming in Java (such as [`CompletableFuture`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html))
mean that multi-threaded programming is increasingly common. This can cause problems
for unit testing because developers sometimes rely on timeouts which can cause random test
failures if timeouts are too small or long tests if timeouts are too long. Fortunately,
there is a simple pattern with `CountDownLatch` that makes is possible to write tests that
are resilient to random failure and execute fast.

Enter [`CountDownLatch`](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/CountDownLatch.html).

`CountDownLatch` is a synchronization aid that blocks a thread until it's value reaches 0.
How can you use this in testing of reactive programming? Put the asserts in in callback
clause and at the end, countdown the latch.

```java
package com.ficksworkshop.junitcountdownlatch;

import org.junit.Test;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;

import static org.junit.Assert.assertEquals;

public class TestAsync {
    /**
     * A function that does some work and returns a future with the result.
     * Normally this function would be the code that you want to test.
     * @return The completed future.
     */
    public CompletableFuture<String> doWork() {
        return CompletableFuture.supplyAsync(() -> "Hello");
    }

    /**
     * A unit test that calls a function depending on a completable future.
     * @throws Exception If the latch expires before calling countdown.
     */
    @Test
    public void testCompletableFutureWithCountdownLatch() throws Exception {
        // Initialize the latch starting at 1. This means that the latch
        // must countdown once to release the thread.
        CountDownLatch latch = new CountDownLatch(1);

        doWork().thenAccept(value -> {
            assertEquals("Hello", value);
            // Since we have finished the asserts, countdown the latch
            // to unblock the test.
            latch.countDown();
        });

        // Wait for the work to finish. Normally this will quickly unblock
        // Only if the test fails will the timeout expire.
        latch.await();

        assertEquals("Hello", value);
        // Since we have finished the asserts, countdown the latch
        // to unblock the test.
    }
}
```

What are the risks? Best practices for tests are to NOT put asserts within conditions
or loops, which this approach clearly violates. However, I think the risk in this case
is tolerable because the only way that you don't hit the asserts is if you failed to
correctly initialize the latch.
