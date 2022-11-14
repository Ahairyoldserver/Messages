import collections
from os.path import isdir
from os.path import isfile

import ResourceBundle
import yaml
from yaml.loader import BaseLoader


class InconsistentKeysError(Exception):
    def __init__(self, plugin: str, base_lang: str, current_lang: str) -> None:
        super().__init__(f'Found inconsistent keys in plugin \'{plugin}\'. '
                         f'Comparing \'{base_lang}\' and \'{current_lang}\'!')


class InconsistentPlaceholderCountError(Exception):
    def __init__(self, plugin: str, base_lang: str, current_lang: str, key: str) -> None:
        super().__init__(f'Found inconsistent placeholder count in plugin \'{plugin}\'. '
                         f'Comparing \'{base_lang}\' and \'{current_lang}\'! '
                         f'The key \'{key}\' seems to have different amount of placeholders.')


class MissingLanguageFileError(Exception):
    def __init__(self, plugin: str, lang: str) -> None:
        super().__init__(f'Found no \'{lang}\'-language file for plugin \'{plugin}\'.')


class MissingPluginFolderError(Exception):
    def __init__(self, plugin: str) -> None:
        super().__init__(f'Found no folder for plugin \'{plugin}\'.')


class MissingEncapsulationSignError(Exception):
    def __init__(self, plugin: str, language: str, key: str, missing: str) -> None:
        super().__init__(
            f'Found an odd amount of encapsulation signs in plugin \'{plugin}\' and language \'{language}\', '
            f'for key \'{key}\' one or more \'{missing}\' signs seem to be missing.')


class InvalidPrefixError(Exception):
    def __init__(self, plugin: str, language: str, key: str, found: str) -> None:
        super().__init__(f'Found an invalid prefix placeholder in plugin \'{plugin}\' and language \'{language}\', '
                         f'for key \'{key}\' the placeholder \'{found}\' was found. This prefix does not exists!')


def _validate_prefixes_and_encapsulation(prefixes: list[str], plugin: str, language: str,
                                         bundle: dict[str, str]) -> None:
    for key, value in bundle.items():
        # Validate encapsulation '${' and '}'
        count_start: int = value.count('${')
        count_end: int = value.count('}')

        if count_start > 0 and count_start > count_end:
            raise MissingEncapsulationSignError(plugin, language, key, '}')

        # Validate prefixes
        find: int = value.find('${prefix.')
        if find == -1:
            continue

        found: str = ''
        for i in range(find + 9, len(value)):
            if value[i] == '}':
                if found not in prefixes:
                    raise InvalidPrefixError(plugin, language, key, found)
                break
            else:
                found += value[i]


def _get_placeholders(value: str) -> list[str]:
    placeholders: list[str] = []
    current_placeholder: str = ''

    for c in value:
        if c == '$' and len(current_placeholder) == 0:
            current_placeholder += c
        elif c == '{' and len(current_placeholder) == 1 and current_placeholder[0] == '$':
            current_placeholder += c
        elif c == '}' and len(current_placeholder) > 2:
            current_placeholder += c
            placeholders.append(current_placeholder)
            current_placeholder = ''
        elif len(current_placeholder) > 1 and current_placeholder[0] == '$' and current_placeholder[1] == '{':
            current_placeholder += c
    return placeholders


def _validate_placeholder_count(plugin: str, base_lang: str, bundle_en: dict[str, str],
                                current_lang: str, bundle_current: dict[str, str]) -> None:
    for key, value in bundle_en.items():
        placeholders_en: list[str] = _get_placeholders(value)
        placeholders_current: list[str] = _get_placeholders(bundle_current.get(key))

        if collections.Counter(placeholders_en) != collections.Counter(placeholders_current):
            raise InconsistentPlaceholderCountError(plugin, base_lang, current_lang, key)


def main() -> None:
    with open('settings.yml', 'r') as f:
        # Load configurations
        config: dict = dict(list(yaml.load_all(f, Loader=BaseLoader))[0])
        plugins: list[str] = config.get('plugins')
        languages: list[str] = config.get('languages')
        prefixes: list[str] = list(dict(ResourceBundle.get_bundle('prefixes')).keys())

        # Iterate through all plugins
        for plugin in plugins:
            # Validate that all plugins folder are existing
            if not isdir(f'{plugin}'):
                raise MissingPluginFolderError(plugin)

            # Load english resource bundle
            # Based on this the other resource bundles will be compared and validated
            base_lang: str = languages[0]
            bundle_en: dict[str, str] = dict(ResourceBundle.get_bundle('messages', base_lang, path=plugin))
            _validate_prefixes_and_encapsulation(prefixes, plugin, base_lang, bundle_en)

            # Iterate through all languages
            for i in range(1, len(languages)):
                current_lang: str = languages[i]

                # Validate that the language file is existing
                if not isfile(f'{plugin}/messages_{current_lang}.properties'):
                    raise MissingLanguageFileError(plugin, current_lang)

                # Load current resource bundle
                bundle_current: dict[str, str] = dict(ResourceBundle.get_bundle('messages', current_lang, path=plugin))
                _validate_prefixes_and_encapsulation(prefixes, plugin, current_lang, bundle_current)

                # Validate that this resource bundle has exactly the same keys as the english one
                if collections.Counter(bundle_en.keys()) != collections.Counter(bundle_current.keys()):
                    raise InconsistentKeysError(plugin, base_lang, current_lang)

                # Validate the amount of placeholder for each entry
                _validate_placeholder_count(plugin, base_lang, bundle_en, current_lang, bundle_current)
    print('Message bundle validation succeeded!')


# Workflow information can be found here:
# https://github.com/jannekem/run-python-script-action
if __name__ == '__main__':
    main()
