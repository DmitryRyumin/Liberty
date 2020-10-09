#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с файлами
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os                 # Работа с файловой системой
import shutil             # Набор функций высокого уровня для обработки файлов, групп файлов, и папок
from pathlib import Path  # Работа с путями в файловой системе

from datetime import datetime  # Работа со временем

# Персональные
from liberty.modules.core import core  # Ядро


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(core.Core):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._file_load = self._('[{}] Поиск "{}" файла ...')
        self._file_name = self._('[{}{}{}] Необходимо указать название файла с расширением "{}" ...')
        self._dir_found = self._('[{}{}{}] Вместо файла передана директория ...')
        self._file_not_found = ' ' * 4 + self._('[{}{}{}] Файл "{}" не найден ...')
        self._file_not_found_create = ' ' * 4 + self._('[{}] Файл "{}" не найден, но был создан ...')
        self._wrong_extension = ' ' * 4 + self._('[{}{}{}] Расширение файла должно быть "{}" ...')

        self._files_load = self._('[{}] Поиск файлов с расширениями "{}" в директории "{}" ...')
        self._dir_name = self._('[{}{}{}] Необходимо указать название директории ...')
        self._files_not_found = ' ' * 4 + self._('[{}{}{}] В указанной директории необходимые файлы не найдены ...')

        self._clear_folder = self._('[{}] Очистка директории "{}" ...')
        self._clear_folder_not_found = ' ' * 4 + self._('[{}{}{}] Директория "{}" не найдена ...')


# ######################################################################################################################
# Работа с файлами
# ######################################################################################################################
class FileManager(Messages):
    """Класс для работы с файлами"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Поиск файла
    def search_file(self, file, extension, create = False, out = True):
        """
        Поиск файла

        (str, str [, bool, bool]) -> bool

        Аргументы:
            file      - Путь к файлу
            extension - Расширение файла
            create    - Создание файла в случае его отсутствия
            out       - Печатать процесс выполнения

        Возвращает: True если файл найден, в обратном случае False
        """

        # Проверка аргументов
        if type(file) is not str or type(extension) is not str or type(create) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.search_file.__name__)

            return False

        # Файл не передан
        if not file:
            # Вывод сообщения
            if out is True:
                print(self._file_name.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, extension.upper()
                ))

            return False

        # Передана директория
        if os.path.isdir(file) is True:
            # Вывод сообщения
            if out is True:
                print(self._dir_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return False

        # Вывод сообщения
        if out is True:
            print(self._file_load.format(datetime.now().strftime(self._format_time), os.path.basename(file)))

        _, ext = os.path.splitext(file)  # Расширение файла

        if ext.replace('.', '') != extension:
            # Вывод сообщения
            if out is True:
                print(self._wrong_extension.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, extension
                ))

            return False

        # Файл не найден
        if os.path.isfile(file) is False:
            # Создание файла
            if create is True:
                # Создание JSON файла
                open(file, 'a', encoding = 'utf-8').close()

                # Вывод сообщения
                if out is True:
                    print(self._file_not_found_create.format(
                        datetime.now().strftime(self._format_time), os.path.basename(file)
                    ))

                return False

            # Вывод сообщения
            if out is True:
                print(self._file_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, os.path.basename(file)
                ))

            return False

        return True  # Результат

    # Поиск файлов в указанной директории
    def search_files(self, folder, extension, sort = True, out = True):
        """
        Поиск файлов в указанной директории

        (str, tuple [, bool, bool]) -> tuple or None

        Аргументы:
            file      - Путь к файлам
            extension - Расширение файлов
            sort      - Сортировать файлы
            out       - Печатать процесс выполнения

        Возвращает кортеж c файлами, в обратном случае None
        """

        # Проверка аргументов
        if type(folder) is not str or type(extension) is not tuple or len(extension) == 0 \
                or type(sort) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.search_files.__name__)

            return None

        # Директория не передана
        if os.path.isdir(folder) is False:
            # Вывод сообщения
            if out is True:
                print(self._dir_name.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return None

        # Вывод сообщения
        if out is True:
            print(self._files_load.format(
                datetime.now().strftime(self._format_time), ', '.join(x for x in extension), self._args['file']
            ))

        # Список из файлов с необходимым расширением
        files = [
            str(p.resolve()) for p in Path(self._args['file']).glob('*') if p.suffix.replace('.', '') in extension
        ]

        # В указанной директории не найдены необходимые файлы
        if len(files) is 0:
            # Вывод сообщения
            if out is True:
                print(self._files_not_found.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return None

        # Сортировка файлов
        if sort is True:
            return sorted(files)

        return files

    # Очистка директории
    def clear_folder(self, path, out = True):
        """
        Очистка директории

        (str, [, bool]) -> bool

        Аргументы:
            path - Путь к директории
            out  - Печатать процесс выполнения

        Возвращает: True если директория очищена, в обратном случае False
        """

        # Проверка аргументов
        if type(path) is not str or not path or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.clear_folder.__name__)

            return False

        # Вывод сообщения
        if out is True:
            print(self._clear_folder.format(datetime.now().strftime(self._format_time), path))

        # Каталог с файлами найден
        if os.path.exists(path):
            # Очистка
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                try:
                    shutil.rmtree(filepath)
                except OSError:
                    os.remove(filepath)
        else:
            # Вывод сообщения
            if out is True:
                print(self._clear_folder_not_found.format(
                    self.red, datetime.now().strftime(self._format_time), self.end, path
                ))

            return False

        return True  # Результат
