#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с JSON
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os    # Работа с файловой системой
import json  # Кодирование и декодирование данные в удобном формате

from datetime import datetime                # Работа со временем
from types import ModuleType                 # Тип модуля
import importlib.resources as pkg_resources  # Работа с ресурсами внутри пакетов

# Персональные
from liberty.modules.filem.file_manager import FileManager  # Работа с файлами


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(FileManager):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._load_data = ' ' * 4 + self._('[{}] Загрузка данных из файла "{}" ...')
        self._invalid_file = ' ' * 4 + self._('[{}{}{}] Данные не загружены ...')
        self._load_data_resources = self._('[{}] Загрузка данных из ресурсов "{}" ...')
        self._load_data_resources_not_found = ' ' * 4 + self._('[{}{}{}] Ресурс не найден ...')
        self._config_empty = ' ' * 4 + self._('[{}{}{}] Файл пуст ...')


# ######################################################################################################################
# Работа с JSON
# ######################################################################################################################
class Json(Messages):
    """Класс для работы с JSON"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка JSON файла
    def load(self, file, create = False, out = True):
        """
        Загрузка JSON файла

        (str [, bool, bool]) -> dict or None

        Аргументы:
            file   - Путь к файлу JSON
            create - Создание файла JSON в случае его отсутствия
            out    - Печатать процесс выполнения

        Возвращает словарь из json файла или None
        """

        # Проверка аргументов
        if type(file) is not str or type(create) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.load.__name__)

            return None

        # Поиск JSON файла не удался
        if self.search_file(file, 'json', create, out) is False:
            return None

        # Вывод сообщения
        if out is True:
            print(self._load_data.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        # Открытие файла
        with open(file, mode = 'r', encoding = 'utf-8') as json_data_file:
            try:
                config = json.load(json_data_file)
            except json.JSONDecodeError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self._red, datetime.now().strftime(self._format_time), self._end))

                return None

        # Файл пуст
        if len(config) == 0:
            # Печать
            if out is True:
                print(self._config_empty.format(self._red, datetime.now().strftime(self._format_time), self._end))

            return None

        return config  # Результат

    # Загрузка JSON файла из ресурсов модуля
    def load_resources(self, module, file, out = True):
        """
        Загрузка JSON файла из ресурсов модуля

        (module, str [, bool]) -> dict or None

        Аргументы:
            module - Модуль
            file   - Файл JSON
            out    - Печатать процесс выполнения

        Возвращает словарь из json файла или None
        """

        # Проверка аргументов
        if isinstance(module, ModuleType) is False or type(file) is not str or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.load_resources.__name__)

            return None

        # Вывод сообщения
        if out is True:
            print(self._load_data_resources.format(datetime.now().strftime(self._format_time), module.__name__))

        # Ресурс с JSON файлом не найден
        if pkg_resources.is_resource(module, file) is False:
            # Вывод сообщения
            if out is True:
                print(self._load_data_resources_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return None

        # Открытие файла
        with pkg_resources.open_text(module, file, encoding='utf-8', errors='strict') as json_data_file:
            try:
                config = json.load(json_data_file)
            except json.JSONDecodeError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self.red, datetime.now().strftime(self._format_time), self.end))

                return None

        # Файл пуст
        if len(config) == 0:
            # Печать
            if out is True:
                print(self._config_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return None

        return config  # Результат
