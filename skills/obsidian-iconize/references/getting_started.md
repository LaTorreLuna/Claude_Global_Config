# Obsidian-Iconize - Getting Started

**Pages:** 6

---

## Syncing ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/guide/syncing.html

**Contents:**
- Syncing ​
- Lucide Icons ​
- Background Checker ​

Normally, syncing should work across all devices with established cloud providers. However, if you want to sync your data across devices with Obsidian Sync and possibly have thousands of icons, you need to try the following configuration (detailed discussions can be found here) for a successful syncing process:

Try setting the Iconize icon packs folder path to .obsidian/icons. Setting the icon packs path to this specific path does not sync the icon packs and you have to sync them manually. This won't clog up the synchronization process of Obsidian Sync.

You also need to enable the background checker. Your settings should look like this:

Obsidian supports Lucide icons by default. This native integration brings several advantages, such as there is no additional download required and sync seamlessly across all your devices. That's why I highly advise, if you are experiencing syncing issues, exclusively use the Lucide icons for now, which are installed by default, and remove all other icon packs from your Obsidian vault.

When the the native Lucide icon pack is disabled, it will look something like this:

The background checker is not only useful for syncing. It is also useful for when you want to download icons that are set in your vault but are not yet available in the icon packs.

Next to setting the icon packs path to .obsidian/icons, you should also enable the background checker. This will check if icons are missing and will download them in the background and extract them to the correct icon pack folder. In addition, it will also remove unused icon files from the icon packs folder (the icons will still be available).

---

## Icon Packs ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/guide/icon-packs.html

**Contents:**
- Icon Packs ​
- Predefined Icon Packs ​
- Custom Icon Packs ​
- Using Emojis ​

Iconize comes with some predefined icon packs. However, you can also add your own icon packs. This section of the documentation will show you how to do that, but also how to use the predefined icon packs and emojis.

To use a predefined icon pack, you can go to the settings of the plugin and select Browse icon packs and then select the icon pack you want to use. So that the following modal will open:

After you have selected the icon pack you want to use, it will download the icon pack and then you can use it in your vault.

Currently, Iconize supports the following predefined icon packs:

If you want to add a predefined icon pack or you would like to update an existing one, feel free to open a pull request on GitHub.

This feature is currently not 100% available and stable. If you want to use it, you can do that, but it might be that some things are not working as expected. Furthermore, there might be some breaking changes in the future.

If you want to add your own icon pack, you can do that by using the option Add icon pack in the plugin settings of Iconize. You just need to enter the name of the icon pack. After that, you can add the icons you want to use in your vault by using the plus icon (+) next to the custom icon pack.

After you have added the icon pack, you need to zip your custom icon pack by going to the plugins folder of Obsidian. You can find the plugins folder by going to the settings of Obsidian and then clicking on Open plugins folder. After that, you need to go to the folder obsidian-iconize and then to the folder icons. In this folder, you can zip your custom icon pack. The zip file needs to have the same name as the icon pack you have entered in the settings of Iconize.

The creation of a zip file needs to be currently done manually. In the future, this will be automatically done by Iconize. See this issue for more information.

If you want to use emojis in your vault, you can do that by using the built-in functionality of Iconize. You can directly use emojis in the icon picker by searching for them. You can search for emojis by using the name of the emoji or by using the emoji itself.

Furthermore, you can also adapt the style of the emoji by choosing the emoji style in the settings of Iconize. You can choose between Native and Twemoji.

---

## Settings ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/guide/settings.html

**Contents:**
- Settings ​

Documentation Coming Soon

---

## Getting Started ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/api/getting-started.html

**Contents:**
- Getting Started ​
- What is possible? ​
- Installation ​

---

## Icon Packs ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/guide/icon-packs

**Contents:**
- Icon Packs ​
- Predefined Icon Packs ​
- Custom Icon Packs ​
- Using Emojis ​

Iconize comes with some predefined icon packs. However, you can also add your own icon packs. This section of the documentation will show you how to do that, but also how to use the predefined icon packs and emojis.

To use a predefined icon pack, you can go to the settings of the plugin and select Browse icon packs and then select the icon pack you want to use. So that the following modal will open:

After you have selected the icon pack you want to use, it will download the icon pack and then you can use it in your vault.

Currently, Iconize supports the following predefined icon packs:

If you want to add a predefined icon pack or you would like to update an existing one, feel free to open a pull request on GitHub.

This feature is currently not 100% available and stable. If you want to use it, you can do that, but it might be that some things are not working as expected. Furthermore, there might be some breaking changes in the future.

If you want to add your own icon pack, you can do that by using the option Add icon pack in the plugin settings of Iconize. You just need to enter the name of the icon pack. After that, you can add the icons you want to use in your vault by using the plus icon (+) next to the custom icon pack.

After you have added the icon pack, you need to zip your custom icon pack by going to the plugins folder of Obsidian. You can find the plugins folder by going to the settings of Obsidian and then clicking on Open plugins folder. After that, you need to go to the folder obsidian-iconize and then to the folder icons. In this folder, you can zip your custom icon pack. The zip file needs to have the same name as the icon pack you have entered in the settings of Iconize.

The creation of a zip file needs to be currently done manually. In the future, this will be automatically done by Iconize. See this issue for more information.

If you want to use emojis in your vault, you can do that by using the built-in functionality of Iconize. You can directly use emojis in the icon picker by searching for them. You can search for emojis by using the name of the emoji or by using the emoji itself.

Furthermore, you can also adapt the style of the emoji by choosing the emoji style in the settings of Iconize. You can choose between Native and Twemoji.

---

## Getting Started ​

**URL:** https://florianwoelki.github.io/obsidian-iconize/guide/getting-started.html

**Contents:**
- Getting Started ​
- Installation ​
- Usage ​
- Support the Project ​

This obsidian plugin allows you to add any custom icon (of type .svg) or from an icon pack to anything you want in your Vault. This can be a file, a folder, in a title, or even in a paragraph of your notes.

For installing the plugin, you can either install it from the community plugins or download the latest release from the GitHub releases.

This was all you need to do to install the plugin. Now you can start using it.

Using the plugin is really straightforward. Obviously, Iconize has a lot of other features, but the most important one is to add icons to your files or folders.

First of all, you need an icon pack. You can either use one of the predefined icon packs or add your own. For adding your own, please read the documentation about custom icon packs.

For adding a predefined icon pack, you can go to the settings of the plugin and select Browse icon packs and then select the icon pack you want to use.

After installing the icon pack, you just need to right-click on a file or folder and then select the option Change Icon. This will open a modal where you can select the icon you want to use.

Our vision is to let you add Icons to your Obsidian Vault whereever you want. We want to make it as easy as possible to add Icons to your notes, files, or folders.

This project is open source and free to use. If you like it, please consider supporting us

---
