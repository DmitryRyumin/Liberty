#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Распознавание жестов

python liberty/samples/amir_play.py [<command> --config путь_к_конфигурационному_файлу
    --frames_to_update 25 --automatic_update --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
from datetime import datetime  # Работа со временем

# Персональные
import liberty  # Воспроизведение фото/видео данных

from liberty import configs                                            # Конфигурационные файлы
from liberty.modules.amir.gesture_recognizer import GestureRecognizer  # Распознавание жестов

# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(GestureRecognizer):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
class Run(Messages):
    """Класс для распознавания жестов"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Проверка JSON файла настроек на валидность
    def _valid_json_config(self, config, out = True):
        """
        Проверка настроек JSON на валидность

        (dict [, bool]) -> bool

        Аргументы:
           config - Словарь из JSON файла
           out    - Печатать процесс выполнения

        Возвращает: True если файл валидный, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._valid_json_config(config, out) is False:
            return False

        curr_all_layer = all_layer = 1  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # Отображение ограничивающего прямоугольника ближайшего найденного скелета
            if key == 'skeleton_rectangle':
                # Проверка значения
                if type(val) is not bool:
                    continue

                # Общее количество разделов не изменялось
                if curr_all_layer == all_layer:
                    if config['skeleton_rectangle'] is True:
                        # Добавляем:
                        #     1. Цвет рамки ограничивающего прямоугольника найденного скелета
                        #     2. Толщина рамки ограничивающего прямоугольника найденного скелета
                        #     3. Цвет фона ограничивающего прямоугольника найденного скелета
                        #     4. Отступы для ограничивающего прямоугольника
                        all_layer += 4

                curr_valid_layer += 1

            # 1. Цвет рамки ограничивающего прямоугольника найденного скелета
            # 2. Цвет фона ограничивающего прямоугольника найденного скелета
            if key == 'skeleton_rectangle_outline_color' or key == 'skeleton_rectangle_background_color':
                # Отображение ограничивающего прямоугольника найденного скелета
                if 'skeleton_rectangle' in config and config['skeleton_rectangle'] is True:
                    all_layer_2 = 4  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 255:
                            continue

                        # 1. Красный
                        # 2. Зеленый
                        # 3. Синий
                        # 4. Прозрачность
                        if k == 'red' or k == 'green' or k == 'blue' or k == 'alpha':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # Толщина рамки ограничивающего прямоугольника найденного скелета
            if key == 'skeleton_rectangle_outline_size':
                # Отображение ограничивающего прямоугольника найденного скелета
                if 'skeleton_rectangle' in config and config['skeleton_rectangle'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 10:
                        continue

                    curr_valid_layer += 1

            # Отступы для ограничивающего прямоугольника
            if key == 'padding_rectangle':
                # Отображение ограничивающего прямоугольника найденного скелета
                if 'skeleton_rectangle' in config and config['skeleton_rectangle'] is True:
                    all_layer_2 = 2  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 300:
                            continue

                        # 1. Минимальный отступ для ограничивающего прямоугольника
                        # 2. Максимальный отступ для ограничивающего прямоугольника
                        if k == 'min' or k == 'max':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        # Минимальный отсуп меньше максимального
                        if val['min'] < val['max']:
                            curr_valid_layer += 1

        # Сравнение общего количества разделов и валидных разделов в конфигурационном файле
        if all_layer != curr_valid_layer:
            # Вывод сообщения
            if out is True:
                print(self._invalid_file.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return False

        return True  # Результат

    # Загрузка и проверка конфигурационного файла
    def _load_config_json(self, resources = configs, config = 'amir.json', out = True):
        """
        Загрузка и проверка конфигурационного файла

        ([module, str, bool]) -> bool

        Аргументы:
            resources - Модуль с ресурсами
            config    - Конфигурационный файл
            out       - Печатать процесс выполнения

        Возвращает: True если файл загружен и валиден, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._load_config_json(resources, config, out) is False:
            return False

        return True

    # Автоматическая проверка конфигурационного файла в момент работы программы
    def _update_config_json(self, set_window_name = True):
        """
        Автоматическая проверка конфигурационного файла в момент работы программы

        ([bool]) -> bool

        Аргументы:
            set_window_name - Установка имени окна

        Возвращает: True если аргументы переданы верно, в обратном случае False
        """

        # Минимальный отступ для ограничивающего прямоугольника
        curr_min_padding = self._args['padding_rectangle']['min']
        # Максимальный отступ для ограничивающего прямоугольника
        curr_max_padding = self._args['padding_rectangle']['max']

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(set_window_name) is False:
            return False

        if self._automatic_update['invalid_config_file'] is False:
            # 1. Минимальный отступ для ограничивающего прямоугольника был изменен
            # 2. Максимальный отступ для ограничивающего прямоугольника был изменен
            if curr_min_padding != self._args['padding_rectangle']['min'] \
                or curr_max_padding != self._args['padding_rectangle']['max']:
                # Диапазон отступов отступов для ближайшего из найденных скелетов был изменен
                if self.range_padding(self._args['padding_rectangle']['min'],
                                      self._args['padding_rectangle']['max']) is False:
                    return False

        return True

    # Распознавание жестов
    def _gesture_recognition(self):
        """
        Распознавание жестов

        () -> bool

        Возвращает: True если обработка кадров для распознавания жеста успешна, в обратном случае False
        """

        # Отображения распознавания жестов
        if self._args['show_labels'] is False \
                and self._args['skeleton_tracking'] is False and self._args['skeleton_tracking_lines'] is False \
                and self._args['skeleton_rectangle'] is True:
            # Формирование прозрачного наложения на текущий кадр кадра
            self._frame_transparent()

        # Получение ближайшего скелета
        if self.get_near_body() is False:
            return False

        return True

    # Получение ориентиров скелета из Kinect 2
    def _get_bodies(self, draw = True, func = None, out = True):
        """
        Получение ориентиров скелета из Kinect 2

        ([bool, FunctionType, bool]) -> bool

        Аргументы:
            draw - Отрисовка ориентиров скелета
            func - Функция или метод
            out  - Печатать процесс выполнения

        Возвращает: True если операции над кадром произведены, в обратном случае False
        """

        # Выполнение функции из суперкласса
        if super()._get_bodies(draw, func, out) is True:
            self._gesture_recognition()  # Распознавание жестов

    # Операции над кадром
    def _frame_o(self, draw = False, func = None, out = True):
        """
        Операции над кадром

        ([bool, FunctionType, bool]) -> bool

        Аргументы:
            draw - Отрисовка ориентиров скелета
            func - Функция или метод
            out  - Печатать процесс выполнения

        Возвращает: True если операции над кадром произведены, в обратном случае False
        """

        # Выполнение функции из суперкласса
        if super()._frame_o(draw, func, out) is True:
            # Отображения распознавания жестов
            if self._args['show_labels'] is False \
                    and self._args['skeleton_tracking'] is False and self._args['skeleton_tracking_lines'] is False \
                    and self._args['skeleton_rectangle'] is True:
                self._composite()  # Формирование итогового кадра

    # Циклическое получение кадров из видеопотока
    def _loop(self, other_source = None, func = None, out = True):
        """
        Циклическое получение кадров из фото/видеопотока

        ([bool]) -> bool

        Аргументы:
           other_source - Ресурс извлечения фото/видеоданных
           func         - Функция или метод
           out          - Печатать процесс выполнения

        Возвращает: True если получение кадров осуществляется, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._loop(self._get_color_frame, self._frame_o, out) is False:
            return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def run(self, metadata = liberty, resources = configs, start = True, out = True):
        """
        Запуск

        ([module, module, bool, bool]) -> None

        Аргументы:
           metadata  - Модуль из которого необходимо извлечь информацию
           resources - Модуль с ресурсами
           start     - Запуск процесса извлечения изображений
           out       - Печатать процесс выполнения
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super().run(metadata, resources, False, out) is False:
            return False

        # Установка диапазона отступов для ближайшего из найденных скелетов
        if self.range_padding(self._args['padding_rectangle']['min'], self._args['padding_rectangle']['max']) is False:
            return False

        # Запуск процесса извлечения изображений
        if start is True:
            self.set_loop(self._loop)  # Циклическая функция извлечения изображений
            self.start()  # Запуск


def main():
    run = Run()

    run.run()


if __name__ == "__main__":
    main()