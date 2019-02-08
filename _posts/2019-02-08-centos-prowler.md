---
layout: post
title: prowler on Centos7
date: 2019-02-08
---

I've been experimenting with tools for benchmarking AWS deployments. One tool I experimented with is
(prowler)[https://github.com/toniblyx/prowler]. However, it doesn't seem to run nicely under Windows
unless you have cygwin.

After a few failures, I decided to just install CentOS 7 into Hyper-V (mostly because I hadn't tried to
run CentOS in Hyper-V and was curious what I would find). Well, it was more complex than I thought. For
reference, the particular version I had was:

```
$ cat /etc/centos-release
CentOS Linux release 7.6.1810 (Core)
```

After installing CentOS into Hyper-V, you need to setup networking. There is a good (Stackoverflow
post)[https://unix.stackexchange.com/questions/17436/centos-on-hyperv-eth0-not-in-ifconfig] on how to do this.

1. Search and download *Linux Integration Disk*. I downloaded the ISO.
1. Connect the ISO with Hyper-V.
1. Mount the ISO:
   `sudo mount /dev/cdrom /media`
1. Run the install script
   `sudo /media/install.sh`
1. Edit `/etc/sysconfig/network-scripts/ifcfg-eth0` so that it contains at least the following:
   ```
   DEVICE=eth0
   BOOTPROTO=dhcp
   ONBOOT=yes
   ```
1. Edit `/etc/sysconfig/network` so that it contains at least the following:
   ```
   NETWORKING=yes
   HOSTNAME=your.choise.lan
   ```
1. Reboot with `reboot`

Next, install `pip`, `git`, and the `aws cli`

1. Update yum
   `yum -y update`
1. Enable EPEL by installing the yum package
   `yum -y install epel-release`
1. Install `pip` from yum
   `yum -y install python-pip git`
1. Install the AWS CLI
   `pip install awscli`

Configure AWS CLI in the usual way with

```
aws configure
```

Next install prowler

```
git clone https://github.com/Alfresco/prowler
cd prowler
```

And finally run prowler

```
./prowler
```
