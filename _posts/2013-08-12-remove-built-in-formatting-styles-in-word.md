---
layout: post
title: Remove Built-in Formatting Styles in Word
date: 2013-08-12
---

When I write documents in Microsoft Word, I make extensive use of styles because they are the easiest way to ensure that your document has a consistent formatting and that helps make your document more formal. It is also an enormous time saver if you want to change a style in your document because you only have to change it in one place and your entire document will be updated.

Word has many built-in styles but they compete with using a consistent formatting you define. I've always wanted to remove some styles from certain documents. Although you can't remove them entirely, you can prevent them from being used and in fact force your doucment only use styles that you've defined.

1. Press `Alt+Ctrl+Shift+S` to show the `Styles` pane.

    ![](/static/img/blog/remove_builtin_word_styles/styles_pane.png)

2. In the `Styles` pane, at the bottom click `Manage Styles` (the third button). The `Manage Styles` window shows. Select the `Restrict` tab.

    ![](/static/img/blog/remove_builtin_word_styles/manage_styles.png)
 
3. For each style(s) you don't want to use
    1. Select the style name.
    2. Click `Restrict`.

4. Check `Limit formatting to permitted styles`.
5. Click `OK`.
6. In the `Start Enforcing Protection` window, click `OK` without setting a password.

    ![](/static/img/blog/remove_builtin_word_styles/start_enforcing_protection.png)

After doing this, you will find that formatting options are disabled.

![](/static/img/blog/remove_builtin_word_styles/disabled_formatting.png)

This is what you want, but it also makes annotating your document with to do items more difficult. To combat that, I usually define some special "annotation" character styles to highlight to do items. I'll assume anyone wanting to restrict styles is sufficiently advanced that I don't need to explain how to create styles.