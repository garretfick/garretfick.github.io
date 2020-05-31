---
layout: post
title: Mapping SYS COLORS to Element
date: 2011-11-27
---

Whenever you create a custom control in Windows, it is important that the control look right, even when Windows has been themed. This means when drawing, you need to pick the right ID to use with `GetSysColor()`. The problem is that many of the [IDs for  `GetSysColor`](http://msdn.microsoft.com/en-us/library/windows/desktop/ms724371(v=vs.85).aspx) map to the same colour on many Windows themes, making it difficult to determine which colour to use. How do you know which color is used for which element?

The trick is to tell Windows substitute a different colour from the theme. One way to do this is through the registry, and thankfully, the names are similar to the IDs, so doing it this way gives you confidence in what you changed. Follow these steps to change a Windows theme colour:

1. Open the Registry Editor. Browse to `KEY_CURRENT_USER\Control Panel\Colors`
2. Record the value for the item you want to change (so you can get it back later)
3. Modify the value of interest
4. Reboot

Here, I've modified ButtonFace and ButtonText to red and green, respectively. As you can see, ButtonFace is also used as the background color for dialogs and ButtonText is used for ListView column headers. It's not intuitive, but with some trial and error, you can figure out how each color ID is used.

images/blog/2011/11/registrycolourmodified.png

Lastly, in case you didn't follow the instructions, and failed to write down the default value, the defaults are also stored in the registry in the key `HKEY_USERS\.DEFAULT\Control Panel\Colors`.