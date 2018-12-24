---
layout: post
title: Spin Locks in C++
date: 2018-10-02
---

Spin locks a ubiquitous tool used to implement synchronization on multiprocessor systems.
Algorithms for Scalable Synchronization in Shared-Memory Multiprocessors gives a good overview
of various spin lock approaches, but it can also be helpful to think about how you would
implement such a lock in another language.

This post is an attempt at expressing spin locks in C++. It should be noted that there are
inherent problems in expressing spin locks in C++ and some of the considerations in spin locks
don't quite map to higher level code. Still, it can be helpful for understanding.

When looking at locks, we care about several attributes:

* latency - time to get a lock without contention
* contention - interconnection traffic caused by the lock
* fairness - which processor gets the lock when released

## Test and Set

Test and set is perhaps the simplest spin lock.

```
            (start)
               │
       ┌───────┴────────┐
       │ Attempt to set │──────┐
       └───────┬────────┘      │
               │               │
              ╱ ╲     no       │
           Succeeded?──────────┘
              ╲ ╱
               │
          yes  │
       ┌───────┴────────┐
       │Critical section│
       └───────┬────────┘
               │
       ┌───────┴────────┐
       │   Unset flag   │
       └───────┬────────┘
               │
             (end)
```

This is trivial to implement in C++ with simple atomics:

```cpp
void* acquireLock()
{
     while (!std::atomic_flag_test_and_set_explicit(&lock, std::memory_order_acquire)) {
          // Do nothing
     }

     return nullptr;
}

void releaseLock(void* lockData) {
     std::atomic_flag_clear_explicit(&lock, std::memory_order_release);
}
```

This algorithm results in high contention because the attempts to set the flag cause invalidations.

## Test and Test and Set

We can reduce invalidations by only attempting to set if there is a reasonable chance of success.

```
             (start)
                │
                │───────────────┐
                │               │
               ╱ ╲     yes      │
            Is locked?──────────┘
               ╲ ╱              │
            no  │               │
        ┌───────┴────────┐      │
        │ Attempt to set │      │
        └───────┬────────┘      │
                │               │
               ╱ ╲     no       │
            Succeeded?──────────┘
               ╲ ╱
                │
           yes  │
        ┌───────┴────────┐
        │Critical section│
        └───────┬────────┘
                │
        ┌───────┴────────┐
        │   Unset flag   │
        └───────┬────────┘
                │
              (end)
```

The difference from test and set is the algorithm only makes an attempt if there is
a possibility that it might succeed.

Again, this is straightforward to implement in C++.

```cpp
void* acquireLock()
{
     while (!*lock._My_flag || !std::atomic_flag_test_and_set_explicit(&lock, std::memory_order_acquire)) {
          // Do nothing
     }

     return nullptr;
}

void releaseLock(void* lockData) {
     std::atomic_flag_clear_explicit(&lock, std::memory_order_release);
}

```

However, when the lock is releases, there remains contention because all waiting processors
will see the flag as available and attempt to set it.

## Test and Set and Wait

To reduce contention, we can introduce a wait so that when a lock is released, not all
processors will attempt to get the lock.

```
             (start)
                │───────────────────┐
                │                ┌──┴───┐
                │                │ Wait │
               ╱ ╲     yes       └──┬───┘
            Is locked?──────────────│
               ╲ ╱                  │
            no  │                   │
        ┌───────┴────────┐          │
        │ Attempt to set │          │
        └───────┬────────┘          │
                │                   │
               ╱ ╲     no           │
            Succeeded?──────────────┘
               ╲ ╱
                │
           yes  │
        ┌───────┴────────┐
        │Critical section│
        └───────┬────────┘
                │
        ┌───────┴────────┐
        │   Unset flag   │
        └───────┬────────┘
                │
              (end)
```

Different wait strategies can be employed, but a simple one is an exponential back-off
is straightforward to implement.

```cpp
void* acquireLock()
{
     std::chrono::nanoseconds waitTime(1);
    while (!std::atomic_flag_test_and_set_explicit(&lock, std::memory_order_acquire)) {
        // Wait a while before testing again.
        std::this_thread::sleep_for(std::chrono::nanoseconds(waitTime));\
        // This is the exponential back-off - other strategies can be
        // employed here.
        waitTime *= 2;
    }

    return nullptr;
}

void releaseLock(void* lockData) {
    std::atomic_flag_clear_explicit(&lock, std::memory_order_release);
}
```

## Array-Based Queue

A common problem with the spin lock based approaches is that each thread is waiting on the same address.
This causes a number of issues, especially consuming valuable bus bandwidth.

This could be avoided if each thread were to wait on a different address. The array-based queue approach
achieves this by having each thread wait on a separate address.

```cpp
const std::uint8_t HAS_LOCK = 0;
const std::uint8_t MUST_WAIT = 1;

struct queue_lock {
    std::uint8_t* slots;
    std::atomic_int16_t nextSlot;
    // This is not part of the standard definition
    // but we need this because we are using threads
    // to simulate processors.
    std::atomic_int16_t numProcessors;
};

queue_lock lock = {};

/// The array queue requires an array with as many slots as the number of processors.
void initializeLock(unsigned int numProcessors) {
    // In a real implementation, you would want each of these array items to be
    // in a separate cache line (or memory module) so each processors is testing
    // and independent memory location.
    lock.slots = (std::uint8_t*) malloc(sizeof(std::uint8_t) * numProcessors);
    memset(lock.slots, MUST_WAIT, numProcessors);

    lock.slots[0] = HAS_LOCK;
    lock.nextSlot = 0;
    lock.numProcessors = numProcessors;
}

void* acquireLock()
{
    std::atomic_uint16_t myPlace = std::atomic_fetch_add(&lock.nextSlot, 1);

    // If we have incremented past the end of the array, then set back to the beginning
    // Not that we are checking for mod == 0, so only one of our processors can experience
    // this condition at any given time.
    if (myPlace % lock.numProcessors == 0) {
        std::atomic_fetch_sub(&lock.nextSlot, lock.numProcessors);
    }

    // This is why we don't have a race condition above - because in all cases, we ensure that
    // we are within the bounds of the array.
    myPlace = myPlace % lock.numProcessors;

    while (lock.slots[myPlace] == MUST_WAIT) {
        // Do nothing
    }

    std::int16_t* myPlacePtr = (std::int16_t*) malloc(sizeof(std::int16_t));
    *myPlacePtr = 1;
    return myPlacePtr;
}

void releaseLock(void* lockData) {
    std::int16_t* myPlacePtr = (std::int16_t*) lockData;

    // Move the lock forward to the next place
    lock.slots[(*myPlacePtr + 1) % lock.numProcessors] = HAS_LOCK;

    free(myPlacePtr);
}
```

While this lock achieves part of the goal, it has an obvious drawback. The lock requires an array with as
many slots as there are cores. This is obviously wasteful.

## MCS Lock

The MCS lock algorithm satisfies many of the goals for efficient locks. Unfortunately, I cannot publish
the algorithm because it is also part of course work for a course I have taken previously. It is, however,
straightforward to implement and an interesting exercise.

## Final Words

I've given four algorithms for implementing the essence of spin locks in C++, but this is not the end. There
are further important considerations for real implementations.

* Architecture support for atomic operations varies.
* Performance is architecture specific testing on real hardware is important.
* Memory alignment was not considered.
* The best algorithm can depend on actual on lock contention.

Nevertheless, the algorithms here should be instructive for anyone interested in understanding how locks
are implemented by operating systems.
