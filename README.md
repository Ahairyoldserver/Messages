# Messages [![Validate Messages](https://github.com/Ahairyoldserver/Messages/actions/workflows/resource_bundle_validation.yml/badge.svg)](https://github.com/Ahairyoldserver/Messages/actions/workflows/resource_bundle_validation.yml)
This repository holds all messages for the **ahairyoldserver.net** network!

## Files and Structure
This repository contains all messages in all supported languages for our network. For each plugin, a folder is created 
with its name, where the name is the exact name of the plugin. Each plugin must have a properties file for each 
supported language. This is checked by the workflow. In addition, there are some other files for configuration, 
which are described in the following subsections.

### Language Files
All language files are property files. This means that all entries are structured like a dictionary. To ensure that 
automation and reading from our MessageAPI works smoothly, please note the following restrictions:
1. Naming convention of all language-files: `messages_languageCode_countryCode.properties`
2. For each language specified in the [settings.yml](https://github.com/Ahairyoldserver/Messages/blob/develop/settings.yml), a language file needs to be created for each plugin.
3. All language files are located in the corresponding plugin folder.
4. All language files are encoded in UTF-8.
5. Every message key is included in every correlated language files.
6. Every message key is unique.
7. All entries following this format: `message_key=your message here`

If you want to make use of placeholders, please follow these conventions:
1. All placeholders start with `${` and end with `}`.
2. You can specify your placeholder name inside those encapsulations.
3. If you want to change your placeholder to a prefix placeholder use the syntax `${prefix.key}`, where `key` is an existing key in the [prefixes](https://github.com/Ahairyoldserver/Messages/blob/develop/prefixes.properties) file!
4. If you are using a placeholder make sure, that the **exact same placeholder** is also included in the corresponding language files of this plugin.
5. You can use unlimited placeholders in each message, as soon as you follow these conventions!

Furthermore, you can use all spigot color codes. If you want to have a preview of your message, you can use this [tool](https://minecraft.tools/en/motd.php).

| Code    | Color                                                                        | &#124; | Code    | Color                                                                      |
|---------|------------------------------------------------------------------------------|--------|---------|----------------------------------------------------------------------------|
| §0      | ![#black](https://placehold.co/15x15/black/black.png) Black                  | &#124; | §1      | ![#darkblue](https://placehold.co/15x15/darkblue/darkblue.png) Dark Blue   |
| §2      | ![#darkgreen](https://placehold.co/15x15/darkgreen/darkgreen.png) Dark Green | &#124; | §3      | ![#darkaqua](https://placehold.co/15x15/009292/009292.png) Dark Aqua       |
| §4      | ![#darkred](https://placehold.co/15x15/darkred/darkred.png) Dark Red         | &#124; | §5      | ![#darkpurple](https://placehold.co/15x15/purple/purple.png) Dark Purple   |
| §6      | ![#gold](https://placehold.co/15x15/gold/gold.png) Gold                      | &#124; | §7      | ![#gray](https://placehold.co/15x15/gray/gray.png) Gray                    |
| §8      | ![#darkgray](https://placehold.co/15x15/darkgray/darkgray.png) Dark Gray     | &#124; | §9      | ![#blue](https://placehold.co/15x15/blue/blue.png) Blue                    |
| §a      | ![#green](https://placehold.co/15x15/43CA43/43CA43.png) Green                | &#124; | §b      | ![#aqua](https://placehold.co/15x15/aqua/aqua.png) Aqua                    |
| §c      | ![#red](https://placehold.co/15x15/red/red.png) Red                          | &#124; | §d      | ![#lightpurple](https://placehold.co/15x15/C341C3/C341C3.png) Light Purple |
| §e      | ![#yellow](https://placehold.co/15x15/yellow/yellow.png) Yellow              | &#124; | §f      | ![#white](https://placehold.co/15x15/white/white.png) White                |
| ------- | -----------------                                                            | &#124; | ------- | ----------------                                                           |
| §k      | Magic                                                                        | &#124; | §l      | **Bold**                                                                   |
| §m      | <s>Strikethrough</s>                                                         | &#124; | §n      | <ins>Underline</ins>                                                       |
| §o      | _Italic_                                                                     | &#124; | §r      | Reset                                                                      |

### Settings File
This file specifies which plugins are included in this repository and which languages are supported. When you add a 
new plugin or language, **add it to this file as well**. This is important for automatic validation of the syntax of all files.

### Prefixes File
This file contains all predefined prefixes for the messages. You are welcome to add new prefixes or modify the existing 
ones. Please make sure that you do **not** change the existing keys! Otherwise, the existing messages using this prefix 
will not be replaced correctly. This is because they will lose the reference to the prefix.

## Work Sequence
Please follow this order if you want to update messages. This is a script between developers and content/translators:

| Step | Developer                                                                                                                                                             | Content                                                                                             |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| 1    | The _Developer_ will raise an issue, which includes information about the **plugin, key, description, and placeholders** for all required messages in tabular format. | _Wait for their turn..._                                                                            |
| 2    | _Wait for their turn..._                                                                                                                                              | The _Content_ will implement those messages following the conventions above.                        |
| 3    | _Wait for their turn..._                                                                                                                                              | The _Content_ will keep the order of the placeholders for the english message.                      |
| 4    | _Wait for their turn..._                                                                                                                                              | The _Content_ will ensure that the workflow is passing.                                             |
| 5    | _Wait for their turn..._                                                                                                                                              | The _Content_ will add the plugin to the settings file, if it was not included before.              |
| 6    | _Wait for their turn..._                                                                                                                                              | The _Content_ will assign the developer who raised this issue as a reviewer, as soon as he is done. |
| 7    | The _Developer_ will review all changes and will add feedback or a request for changing anything if required.                                                         | _Wait for their turn..._                                                                            |
| 8    | _Wait for their turn..._                                                                                                                                              | The _Content_ maybe has to adjust some messages.                                                    |
| 9    | The _Developer_ will approve the merge request.                                                                                                                       | _Wait for their turn..._                                                                            |
| 10   | _Wait for their turn..._                                                                                                                                              | The _Content_ will merge the changes.                                                               |

## ResourceBundle Workflow
There is an integrated workflow that validates the entire repository. This means that based on the plugins and languages 
defined in the settings file, it goes through all the folders and files and validates their contents. This workflow will 
fail if any of the previously mentioned points are not met. If this is the case, go to `Actions` and open the failed 
workflow. When you open the log, you will see an error message with information about where the validation failed. 
When all issues are resolved, you can merge your changes.
