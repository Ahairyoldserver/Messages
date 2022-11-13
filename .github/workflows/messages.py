import ResourceBundle
import collections
import yaml

from os.path import isfile
from os.path import isdir
from yaml.loader import BaseLoader


class InconsistentKeysError(Exception):
    def __init__(self, plugin: str, base_lang: str, current_lang: str) -> None:
        super().__init__(f'Found inconsistent keys in plugin \'{plugin}\'. '
                         f'Comparing \'{base_lang}\' and \'{current_lang}\'!')


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


def validate_prefixes_and_encapsulation(prefixes: list[str], plugin: str, language: str, bundle: dict[str, str]):
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


def main() -> None:
    with open('../../settings.yml', 'r') as f:
        config: dict = dict(list(yaml.load_all(f, Loader=BaseLoader))[0])
        plugins: list = config.get('plugins')
        languages: list = config.get('languages')
        prefixes: list[str] = list(dict(ResourceBundle.get_bundle('prefixes')).keys())

        for plugin in plugins:
            if not isdir(f'{plugin}'):
                raise MissingPluginFolderError(plugin)

            base_lang: str = languages[0]
            bundle_en: dict[str, str] = dict(ResourceBundle.get_bundle('messages', base_lang, path=plugin))
            validate_prefixes_and_encapsulation(prefixes, plugin, base_lang, bundle_en)

            for i in range(1, len(languages)):
                current_lang: str = languages[i]
                if not isfile(f'{plugin}/messages_{current_lang}.properties'):
                    raise MissingLanguageFileError(plugin, current_lang)

                bundle_current: dict[str, str] = dict(ResourceBundle.get_bundle('messages', current_lang, path=plugin))
                validate_prefixes_and_encapsulation(prefixes, plugin, current_lang, bundle_current)
                if collections.Counter(bundle_en.keys()) != collections.Counter(bundle_current.keys()):
                    raise InconsistentKeysError(plugin, base_lang, current_lang)
    print('Message bundle validation succeeded!')


if __name__ == '__main__':
    main()
