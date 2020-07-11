#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с XML
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os                          # Работа с файловой системой
import xml.parsers.expat as expat  # Анализ XML документа
import xmltodict                   # Преобразование XML документа в словарь
import json                        # Кодирование и декодирование данные в удобном формате

from datetime import datetime                # Работа со временем
from types import ModuleType                 # Тип модуля
import importlib.resources as pkg_resources  # Работа с ресурсами внутри пакетов

# Персональные
from liberty.modules.filem.json_ import Json  # Работа с JSON


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(Json):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса


# ######################################################################################################################
# Работа с XML
# ######################################################################################################################
class Xml(Messages):
    """Класс для работы с XML"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка XML файла
    def load_xml(self, file, out = True):
        """
        Загрузка XML файла

        (str [, bool]) -> dict or None

        Аргументы:
            file - Путь к файлу XML
            out  - Печатать процесс выполнения

        Возвращает словарь из XML файла или None
        """

        # Проверка аргументов
        if type(file) is not str or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.load_xml.__name__)

            return None

        # Поиск XML файла не удался
        if super().search_file(file, 'xml', False, out) is False:
            return None

        # Вывод сообщения
        if out is True:
            print(self._load_data.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        # Открытие файла
        with open(file, mode = 'r', encoding = 'utf-8') as xml_data_file:
            try:
                res = json.loads(json.dumps(xmltodict.parse(xml_data_file.read())))  # Парсинг XML документа
            except expat.ExpatError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self._red, datetime.now().strftime(self._format_time), self._end))

                return None

        # Файл пуст
        if len(res) == 0:
            # Печать
            if out is True:
                print(self._config_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return None

        return res  # Результат

    # Загрузка XML файла из ресурсов модуля
    def load_resources_xml(self, module, file, out = True):
        """
        Загрузка XML файла из ресурсов модуля

        (module, str [, bool]) -> dict or None

        Аргументы:
            module - Модуль
            file   - Файл XML
            out    - Печатать процесс выполнения

        Возвращает словарь из xml файла или None
        """

        # Проверка аргументов
        if isinstance(module, ModuleType) is False or type(file) is not str or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.load_resources_xml.__name__)

            return None

        # Вывод сообщения
        if out is True:
            print(self._load_data_resources.format(datetime.now().strftime(self._format_time), module.__name__))

        # Ресурс с XML файлом не найден
        if pkg_resources.is_resource(module, file) is False:
            # Вывод сообщения
            if out is True:
                print(self._load_data_resources_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return None

        # Открытие файла
        with pkg_resources.open_text(module, file, encoding='utf-8', errors='strict') as xml_data_file:
            try:
                res = json.loads(json.dumps(xmltodict.parse(xml_data_file.read())))  # Парсинг XML документа
            except expat.ExpatError:
                # Вывод сообщения
                if out is True:
                    print(self._invalid_file.format(self.red, datetime.now().strftime(self._format_time), self.end))

                return None

        # Файл пуст
        if len(res) == 0:
            # Печать
            if out is True:
                print(self._config_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return None

        return res  # Результат
