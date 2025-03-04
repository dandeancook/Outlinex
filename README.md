THE GOAL OF THIS FORK
=====================

Better looking outline
* With symbol on every outline line

Allow making and showing regions of code file in outline
* Prefix identifiers which are shown in outline with hyphens to make a region
* Those identifiers will be unused vars, empty functions, etc.

Outline Example:
![Screenshot](https://i.imgur.com/ZbxYWwU.png)


HOW TO INSTALL
==============

Steps
* Remove previous `Outline` package if any, to avoid functionality confusion.
* Find Sublime `Packages` dir
	* Sublime Main Menu >> Preferences >> Browse Packages
* Clone this repo: `git clone -b dev https://github.com/nova3h/outlinex`
	* Clone right inside the `Packages` dir
* OPTIONAL: Edit plugin source code
	* Edit files right inside the newly cloned dir.
	* Edit file `outline.sublime-settings` too if to change any settings
	* Use Sublime API Ref at https://www.sublimetext.com/docs/api_reference.html


HOW TO USE
==========

Create a Region
* At any code line
* Create a method, function, property, or variable
	* With prefix of 5 hyphens: _____
	* With affix of 5 hyphens too: _____
	* With prefix `OX_INDENT_` to specify method/func names to indent, eg. variable functions
	    * Use hyphen to separate func names and no `_` in func names
	* Exact value `_____BLANK_____` to create a blank line in outline

* If the language is JavaScript (ES6)
	* It's possible to add either `#` (private method), or `$` (JS specific char)
	  before the prefix above, in order to minifier to minify those region markers.


OLD README
==========

## Outline for Sublime Text 3

### Overview

Inspired by [FileBrowser](https://github.com/aziz/SublimeFileBrowser), this package shows the outline of your file, class/function name list of your code, or table of content/toc of your markdown/LaTeX document in a sidebar-style tab.

![Screenshot](screenshot.png?raw=true "Screenshot")

### Installation

#### Install via Package Control

This package is available on [Package Control](https://packagecontrol.io/). Search for `Outline`.

#### Manual installation

1. Clone or download this repository to your hard drive using the green `Clone or download` button
2. Rename the cloned or extracted folder to `Outline`. Make sure `outline.py` is at the root of the `Outline` folder.
3. Move the `Outline` folder to your Sublime Text's `Packages` folder. To find the `Packages` folder, click menu `Preferences` > `Browse Packages`.
4. Restart Sublime Text, and press `Ctrl + Shift + P` to select your preferred layout (`Browse Mode`)

### Default layout

The outline tab can be set as a sidebar on the left or right. Press `Ctrl + Shift + P` and select either `Browse Mode: Outline (Left)` or `Browse Mode: Outline (Right)` to set your preferred layout.

If you also use [FileBrowser](https://github.com/aziz/SublimeFileBrowser), you can use both in three different layouts:

* `FileBrowser` left, `Outline` right
* `FileBrowser` top left, `Outline` bottom left
* `FileBrowser` top right, `Outline` bottom right

To use `FileBrowser` and `Outline` together, please close the `FileBrowser` sidebar first and then use the correponding `Browse Mode` command to set the layout, otherwise the `Outline` view may not work as intended.

### Color theme

`Outline` can be configured to use the current editor color scheme. To do so, change the setting below:

```json
"outline_inherit_color_scheme": true
```

`Outline` has two built-in color themes: Bright (default theme) and Dark. To switch to the Dark theme, add the following to your user settings file. Open the user settings file by "Preferences > Package Settings > Outline > Settings" (Sublime Text version 3124 or later), or "Settings - User":

```json
"outline_inherit_color_scheme": false
"color_scheme": "Packages/Outlinex/outline-Dark.hidden-tmTheme"
```

Remove `-Dark` or remove the entire line to return to the bright theme. To customize your own color theme, see [this issue](https://github.com/warmdev/SublimeOutline/issues/1).

### Outline content and indentation

Outline is updated when you save a file or switch between files.

Content and indentation in the `Outline` tab is controlled by the `Symbol List.tmPreferences` file (file name may differ) corresponding to the syntax of your file.

### Known issue

* This package may not work if you use a multi-column/row layout.

### License

This plugin is licensed under the MIT license.
