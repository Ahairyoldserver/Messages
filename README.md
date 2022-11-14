# Messages [![Validate Messages](https://github.com/Ahairyoldserver/Messages/actions/workflows/resource_bundle_validation.yml/badge.svg)](https://github.com/Ahairyoldserver/Messages/actions/workflows/resource_bundle_validation.yml)
This repository holds all messages for the **ahairyoldserver.net** network!

## Files and Structure
This repository holds all messages in all supported languages for our network. For each plugin, a folder is created 
with its name, where the name is the exact plugin name. Each plugin needs to have a properties file for every supported
languages. This will be validated by the workflow. In addition, there are some more files for configuration which will
be described in the following subsections.

### Language Files
All language-files are properties files. This means, all entries are structured like a dictionary. To ensure that the 
automation and the reading from our MessageAPI works fine, please follow the constraints below:
1. Naming convention of all language-files: `messages_languageCode_countryCode.properties`
2. For each language specified in the [settings.yml](https://github.com/Ahairyoldserver/Messages/blob/develop/settings.yml), a language file needs to be created for each plugin.
3. All language files are located in the corresponding plugin folder.
4. All language files are encoded in UTF-8.
5. Every message key is included in every correlated language files.
6. Every message key is unique.
7. All entries following this format: `message_key=your message here`

If you want to make use of placeholders, please follow these conventions:
1. All placeholders start with `${` and ends with `}`.
2. You can specify your placeholder name inside those encapsulations.
3. If you want to change your placeholder to a prefix placeholder use the syntax `${prefix.key}`, where `key` is an existing key in the [prefixes](https://github.com/Ahairyoldserver/Messages/blob/develop/prefixes.properties) file!
4. If you are using a placeholder make sure, that the **exact same placeholder** is also included in the corresponding language files of this plugin.
5. You can use unlimited placeholders in each message, as soon as you follow these conventions!

Furthermore, you can use all spigot color codes. Please make sure, that you are using a **§** sign instead of a **&** sign. <br>
If you want to have a preview of your message, you can use this [tool](https://minecraft.tools/en/motd.php). <br>
[![Spigot ChatColors](https://user-images.githubusercontent.com/60903023/199811974-a41ce1de-04a1-400b-9f55-d90321dc7d6b.png)](https://www.spigotmc.org/resources/chatcolor-farbcodes-im-chat.64589/)

### Settings File
This file specify which plugins are included in this repository and which languages are supported. 
If you add a new plugin or language, **add it also** to this file. This is important for the automated validation of 
the syntax of all files.

### Prefixes File
This file contains all pre-defined prefixes for the messages. Feel free to add new prefixes or adapt the current ones. 
Please make sure, that you are **not** changing the existing keys! Otherwise, the existing messages that are using this 
prefix will not be replaced correctly. Since they are losing the reference to the prefix.

## Work Sequence
Please follow this sequence when you are going to change messages. This is a script between the developers and 
contents/translators:
1. The _Developer_ will raise an issue, which includes information about the **plugin, key, description, and placeholders** for all required messages in tabular format. 
2. The _Content_ will implement those messages following the conventions above.
3. The _Content_ will keep the order of the placeholders for the english message.
4. The _Content_ will ensure that the workflow is passing. 
5. The _Content_ will assign the developer who raised this issue as a reviewer, as soon as he is done.
6. The _Developer_ will review all new messages and will add feedback or a request for changing anything if required.
7. The _Content_ maybe has to adjust some messages.
8. The _Content_ can merge the changes when the developer has approved it.

| Step | Developer                                                                                                                                                             | Content                                                                                             |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| 1    | The _Developer_ will raise an issue, which includes information about the **plugin, key, description, and placeholders** for all required messages in tabular format. |                                                                                                     |
| 2    |                                                                                                                                                                       | The _Content_ will implement those messages following the conventions above.                        |
| 3    |                                                                                                                                                                       | The _Content_ will keep the order of the placeholders for the english message.                      |
| 4    |                                                                                                                                                                       | The _Content_ will ensure that the workflow is passing.                                             |
| 5    |                                                                                                                                                                       | The _Content_ will add the plugin to the settings file, if it was not included before.              |
| 6    |                                                                                                                                                                       | The _Content_ will assign the developer who raised this issue as a reviewer, as soon as he is done. |
| 7    | The _Developer_ will review all changes and will add feedback or a request for changing anything if required.                                                         |                                                                                                     |
| 8    |                                                                                                                                                                       | The _Content_ maybe has to adjust some messages.                                                    |
| 9    | The _Developer_ will approve the merge request.                                                                                                                       |                                                                                                     |
| 10   |                                                                                                                                                                       | The _Content_ will merge the changes.                                                               |

## ResourceBundle Workflow
A workflow is integrated which validates the complete repository. That means, based on the defined plugins and languages 
in the settings file, it will iterate through all folders and files and validate the content of it. This workflow will 
fail if one of the above mention points are not fulfilled. If that is the case, go to `Actions` and open the failed 
workflow. When opening the log, you will see an error message with information where the validation failed. When all 
problems are solved you are able to merge your changes.