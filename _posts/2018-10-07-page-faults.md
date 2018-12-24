---
layout: post
title: Page Faults
date: 2018-10-07
---

What happens when there is a page fault?

```

```
             (start)
                │                ┌───────────┐                ┌───────────┐
                │ VPN            │   ┌───────┴────────┐       │   ┌───────┴────────┐
                │                │   │  Find on disk  │       │   │   TLB update   │
        ┌───────┴────────┐       │   └───────┬────────┘       │   └───────┬────────┘
        │   TLB Lookup   │       │           │                |           │
        └───────┬────────┘       │           │                |           │
                │                │           │                |           │
                │                │   ┌───────┴────────┐       │   ┌───────┴────────┐
                │                │   │ Read page frame│       │   │     Resume     │
        ┌───────┴────────┐       │   └───────┬────────┘       │   └───────┬────────┘
        │   PT Lookup    │       │           │                |           |
        └───────┬────────┘       │           │                |           |
                │                │           │                |         (end)
                │                │   ┌───────┴────────┐       │
                │                │   │    PT update   │       │
                └────────────────┘   └───────┬────────┘       │
                                             └────────────────┘

         Thread local                   System global              Processor local
```

If each process has at most one thread, then there is no risk of serialization since
each process has it's own page table. But, if the process has multiple threads, then
we need a strategy to avoid ensuring that page fault service doesn't have serialization.
