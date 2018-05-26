---
layout: post
title: Docker (Training) on Windows
date: 2018-05-23
---

I'm been working my way through a number of [Docker training](https://training.docker.com) (tutorials). In the past, I had always used Docker on Mac, and it was pretty easy to follow the tutorials. This time, however, I'm on my Windows machine, and this post describes the changes I have made to my development environment.

First, I wanted to be able to install Docker in my Windows environment (so I don't have to startup a VM just to run a Docker command). Unfortunately, this come with some significant differences:

1. Docker on Windows requires Hyper-V which is incompatible with VirtualBox.
1. Hyper-V has limited desktop UI-integration.

For myself, the above doesn't seem like a big trade-off. I almost exclusively use VirtualBox through Vagrant, so I don't need the desktop-UI integration (in any case, it always seemed a little flakey).

However, there is a big hidden trade-off here. Vagrant boxes are specific to a particular [provider](https://www.vagrantup.com/docs/providers/) and in general, a Vagrant box built for VirtualBox/VMWare will not work with Hyper-V.

    It is possible to create Vagrant boxes that target multiple providers, but in my experience, most Vagrant boxes target only one provider.

    I have no experience with the VMWare provider, so the above is only based on my reading and not on first-hand experience.

Second, I wanted to be able to follow the tutorial without translating every instruction from what to do on Linux into what to do on Windows. Of course it is possible to take that approach (and it was my initial strategy), but I quickly found I was spending my time doing the translation rather than the training. It was still instructive, but not my focus.

My strategy therefore was to setup Hyper-V, then use an Ubuntu Vagrant box to run the extra scripts. With a synced folder, I can make all of the changes directly change the files on my destkop matchine.

You can follow the steps below to create the same setup that I used.

1. Follow the directions on the [Vagrant Hyper-V page](https://www.vagrantup.com/docs/hyperv/) to setup Hyper-V.
