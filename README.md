# Extract Text to Laravel Blade View

[![Build Status](https://travis-ci.org/MohannadNaj/sublime-extract-to-blade.svg?branch=master)](https://travis-ci.org/MohannadNaj/sublime-extract-to-blade) [![Build status](https://ci.appveyor.com/api/projects/status/txtal1v37kjs31xl?svg=true)](https://ci.appveyor.com/project/MohannadNaj/sublime-extract-to-blade)


This plugin for Sublime Text 3 allows you to extract the selected text into a new or existing [laravel blade views](https://laravel.com/docs/master/blade) with the `@include` sentence and the appropriate path.

![screenshot](https://i.imgur.com/53e2Kgd.gif)

## 💾 Installation

### Package Control

It is highly recommended to install `Extract Text to Laravel Blade View` with [Package Control](https://packagecontrol.io).

1. [Install Package Control](https://packagecontrol.io/installation) if you haven't yet.
2. Open the command palette (<kbd>Ctrl+Shift+P</kbd> for Windows/Linux, <kbd>Cmd+Shift+P</kbd> for Mac OS)
3. Search for _Package Control: Install Package_ and hit <kbd>Enter</kbd>.
4. Type `Extract Text to Laravel Blade View` and press <kbd>Enter</kbd> to install it.


### Manual Installation

You can clone this repository into your _Sublime Text 3/Packages_

```shell
git clone https://github.com/MohannadNaj/sublime-extract-to-blade
```

##### Mac OS

```shell
cd ~/Library/Application Support/Sublime Text 3/Packages/
git clone git://github.com/MohannadNaj/sublime-extract-to-blade.git
```


##### Linux

```shell
cd ~/.config/sublime-text-3/Packages
git clone git://github.com/MohannadNaj/sublime-extract-to-blade.git
```


##### Windows

```shell
cd "%APPDATA%\Sublime Text 3\Packages"
git clone git://github.com/MohannadNaj/sublime-extract-to-blade.git
```

👉 The `git` command must be available on the command line.

👉 You may need to add the directory containing `git.exe` to your `PATH` environment variable.


## Usage

- While on a Laravel Blade View, Select some text
- open the Command Palette (<kbd>Ctrl+Shift+P</kbd> for Windows/Linux, <kbd>Cmd+Shift+P</kbd> for Mac OS), and look for "Extract: Move selection to blade view ..".
> Alternatively, you can set a key map for this step. see [Keymap](#keymap)

- Enter the blade path for the new blade view (e.g: `welcome.services`)
> you can use relative blade paths also if it's enabled. see [Options](#options)

The plugin will create or append the extracted text to the newly created blade view, and insert `@include` statement in the text source file. The plugin will look for the `resources/views/` directory to resolve the entered path.

## Options
Set your options by navigating to _Preferences > Settings_.

### extract_to_blade_save_last_path
_default: true_
``` js
{
    "extract_to_blade_save_last_path": true
}
```
By enabling this option, the plugin will remember how you located the directory of the blade file the last time you extracted text, and will set the next input to the same directory.

If you extracted a portion of the text to `welcome.about`, the next time the input will be ready for you by default: `welcome.`.

### extract_to_blade_relative_path
_default: false_
``` js
{
    "extract_to_blade_relative_path": false
}
```
By enabling this option, the plugin will build the blade paths relatively to the text source file path.

If you extracted text from `resources/views/layouts/app.blade.php` and typed: `header`, it will create the file on `resources/views/layouts/`, so the blade path for it will be: `@include('layouts.header')`.

Disable this if you used to write the full blade path at your `include` statements.


### extract_to_blade_include_sentence
_default: @include('%s')_
``` js
{
    "extract_to_blade_include_sentence": "@include('%s')"
}
```
The sentence will be used for entering the resolved blade path.

Change this if you prefer the double quotes over the apostrophe for example.
``` js
{
    // double quotes + 4 lines after!!
    "extract_to_blade_include_sentence": "@include(\"%s\")\n\n\n\n"    
}
```

## Keymap

You can set the keymap for extracting the selected text to a Laravel blade view from _Preferences > Key Bindings_. Assuming you want <kbd>Ctrl+Alt+E</kbd> as the command shortcut:
``` js
[
    // windows
    { "keys": ["ctrl+alt+e"], "command": "extract_to_blade"},

    // Linux and Mac OS
    { "keys": ["super+alt+e"], "command": "extract_to_blade"},
]
```

## Credits

- The forked [Extract Text to File](https://github.com/dreki/sublime-extract-to-file) plugin
- The [Installation](#installation) part on this README was modified from [GitGutter's README file](https://github.com/jisaacks/GitGutter/blob/master/README.md)
