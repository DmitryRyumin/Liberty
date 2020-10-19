#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Детектирование лиц

python liberty/samples/facesdet_play.py [<command> --file путь_к_фото_видео_файлу_ или_каталогу_с_фото_файлами
    --config путь_к_конфигурационному_файлу --frames_to_update 25 --automatic_update --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os  # Работа с файловой системой

from datetime import datetime  # Работа со временем

import sys
sys.path.append('/Users/dl/GitHub/Liberty/')

# Персональные
import liberty  # Воспроизведение фото/видео данных

from liberty import configs  # Конфигурационные файлы
from liberty.modules.facesdet.detection import Detection  # Детектирование лиц
from liberty.modules.trml.shell import Shell   # Работа с Shell


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(Detection):
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
    """Класс для поиска лиц"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        # Набор методов для поиска лиц
        self._methods_data = (
            'opencv_dnn',  # Детектирование лиц с помощью глубокого обучения в OpenCV
            ''  # Для будущих методов
        )

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Построение аргументов командной строки
    def _build_args(self, description, conv_to_dict = True):
        """
        Построение аргументов командной строки

        (str [, bool]) -> None or dict

        Аргументы:
            description  - Описание парсера командной строки
            conv_to_dict - Преобразование списка аргументов командной строки в словарь

        Возвращает: dict если парсер командной строки окончательный, в обратном случае None
        """

        super()._build_args(description, False)  # Выполнение функции из суперкласса

        # Преобразование списка аргументов командной строки в словарь
        if conv_to_dict is True:
            args, _ = self._ap.parse_known_args()
            return vars(args)  # Преобразование списка аргументов командной строки в словарь

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

        all_layer = 5  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # Метод детекции лиц
            if key == 'method':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                # Детектирование лиц с помощью глубокого обучения в OpenCV
                if val == 'opencv_dnn':
                    curr_valid_layer += 1

            # Размер изображения для масштабирования
            if key == 'size':
                all_layer_2 = 1  # Общее количество подразделов в текущем разделе
                curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                # Проверка значения
                if type(val) is not dict or len(val) is 0:
                    continue

                # Проход по всем подразделам текущего раздела
                for k, v in val.items():
                    # Проверка значения
                    if type(v) is not int or v < 0:
                        continue

                    # Ширина изображения для масштабирования
                    if k == 'width':
                        curr_valid_layer_2 += 1

                    # Высота изображения для масштабирования
                    if k == 'height':
                        all_layer_2 += 1
                        curr_valid_layer_2 += 1

                if all_layer_2 == curr_valid_layer_2:
                    curr_valid_layer += 1

            # Метод детекции лиц 'opencv_dnn'
            if 'method' in config and config['method'] == 'opencv_dnn':
                # Тип нейронной сети, работает при "method" = opencv_dnn
                if key == 'dnn':
                    # Проверка значения
                    if type(val) is not str or not val:
                        continue

                    # Указан верный ключ
                    if val == 'tensorflow' or val == 'tf' or val == 'caffe':
                        curr_valid_layer += 1

            # Отображение ограничивающих прямоугольников детектированных лиц
            if key == 'face_rectangle':
                # Проверка значения
                if type(val) is not bool:
                    continue

                if config['face_rectangle'] is True:
                    # Добавляем:
                    #     1. Цвет рамки ограничивающих прямоугольников детектированных лиц
                    #     2. Толщина рамки ограничивающих прямоугольников детектированных лиц
                    #     3. Цвет фона ограничивающих прямоугольников детектированных лиц
                    #     4. Внутренние отступы ограничивающих прямоугольников детектированных лиц
                    #     5. Отображение процентов рядом с каждым детектированным лицом
                    all_layer += 5

                curr_valid_layer += 1

            # Доверительный порог детекции лиц
            if key == 'conf_face_threshold':
                # Проверка значения
                if type(val) is not float or val < 0.0 or val > 1.0:
                    continue

                curr_valid_layer += 1

            # Отображение процентов рядом с каждым детектированным лицом
            if key == 'draw_precent':
                # Отображение ограничивающих прямоугольников детектированных лиц
                if 'face_rectangle' in config and config['face_rectangle'] is True:
                    # Проверка значения
                    if type(val) is not bool:
                        continue

                    if val is True:
                        # Добавляем:
                        #     1. Цвет текстов процентов для детектированных лиц
                        #     2. Цвет фона процентов для детектированных лиц
                        #     3. Размер шрифта процентов для детектированных лиц
                        #     4. Ширина обводки текстов процентов для детектированных лиц
                        #     5. Цвет обводки текстов процентов для детектированных лиц
                        #     6. Расстояние между текстами процентов и ограничивающих прямоугольникоа найденных лиц
                        #     7. Внутренний отступ текстов процентов
                        all_layer += 7

                    curr_valid_layer += 1

            # 1. Цвет рамки ограничивающих прямоугольников детектированных лиц
            # 2. Цвет фона ограничивающих прямоугольников детектированных лиц
            if key == 'face_rectangle_outline_color' or key == 'face_rectangle_background_color':
                # Отображение ограничивающих прямоугольников детектированных лиц
                if 'face_rectangle' in config and config['face_rectangle'] is True:
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

            # Толщина рамки ограничивающих прямоугольников детектированных лиц
            if key == 'face_rectangle_outline_size':
                # Отображение ограничивающих прямоугольников детектированных лиц
                if 'face_rectangle' in config and config['face_rectangle'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 10:
                        continue

                    curr_valid_layer += 1

            # Внутренние отступы ограничивающих прямоугольников детектированных лиц
            if key == 'padding_face':
                # Отображение ограничивающих прямоугольников детектированных лиц
                if 'face_rectangle' in config and config['face_rectangle'] is True:
                    all_layer_2 = 2  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) is 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 100:
                            continue

                        # 1. Отступ по левому и правому краю для ограничивающего прямоугольника
                        # 2. Отступ по верхнему и нижнему краю для ограничивающего прямоугольника
                        if k == 'width' or k == 'height':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # 1. Цвет текстов процентов для детектированных лиц
            # 2. Цвет фона процентов для детектированных лиц
            # 3. Цвет обводки текстов процентов для детектированных лиц
            if key == 'face_text_color' or key == 'face_background_color' or key == 'face_stroke_color':
                # 1. Отображение ограничивающих прямоугольников детектированных лиц
                # 2. Отображение процентов рядом с каждым детектированным лицом
                if 'face_rectangle' in config and config['face_rectangle'] is True and \
                   'draw_precent' in config and config['draw_precent'] is True:
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

            # Размер шрифта процентов для детектированных лиц
            if key == 'face_size':
                # 1. Отображение ограничивающих прямоугольников детектированных лиц
                # 2. Отображение процентов рядом с каждым детектированным лицом
                if 'face_rectangle' in config and config['face_rectangle'] is True and \
                   'draw_precent' in config and config['draw_precent'] is True:
                    # Проверка значения
                    if type(val) is not int or val <= 0 or val > 60:
                        continue

                    curr_valid_layer += 1

            # Ширина обводки текстов процентов для детектированных лиц
            if key == 'face_stroke':
                # 1. Отображение ограничивающих прямоугольников детектированных лиц
                # 2. Отображение процентов рядом с каждым детектированным лицом
                if 'face_rectangle' in config and config['face_rectangle'] is True and \
                   'draw_precent' in config and config['draw_precent'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 4:
                        continue

                    curr_valid_layer += 1

            # Внутренний отступ текстов процентов
            if key == 'face_padding':
                # 1. Отображение ограничивающих прямоугольников детектированных лиц
                # 2. Отображение процентов рядом с каждым детектированным лицом
                if 'face_rectangle' in config and config['face_rectangle'] is True and \
                   'draw_precent' in config and config['draw_precent'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 30:
                        continue

                    curr_valid_layer += 1

            # Расстояние между текстами процентов и ограничивающих прямоугольникоа найденных лиц
            if key == 'labels_distance':
                # 1. Отображение ограничивающих прямоугольников детектированных лиц
                # 2. Отображение процентов рядом с каждым детектированным лицом
                if 'face_rectangle' in config and config['face_rectangle'] is True and \
                   'draw_precent' in config and config['draw_precent'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 15:
                        continue

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
    def _load_config_json(self, resources = configs, config = 'facesdet.json', out = True):
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

        # Установка имени окна
        if set_window_name is True:
            curr_window_name = self.title_faces_method_en  # Текущее значение имени окна

        curr_method = self._args['method']  # Текущее значение метода детектирования лиц
        curr_dnn = self._args['dnn']  # Текущее значение типа нейронной сети
        curr_size = self._args['size']  # Текущее значение размера изображения

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(set_window_name) is False:
            return False

        # Необходимые значения в конфигурационном файле найдены в момент работы программы
        if self._automatic_update['invalid_config_file'] is False:
            # 1. Метод был изменен
            # 2. Размер окна был изменен
            # 3. Размеры изображения были изменены
            if curr_method != self._args['method'] or curr_dnn != self._args['dnn'] \
                    or curr_size['width'] != self._args['size']['width'] \
                    or curr_size['height'] != self._args['size']['height']:
                print()
                Shell.add_line()  # Добавление линии во весь экран
                # Загрузка модели поиска лиц
                if self._load_faces_model() is False:
                    # Модель была загружена на прошлой проверке
                    if self._automatic_update['faces_model_not_load'] is False:
                        # Модель не загружена в момент работы программы
                        self._automatic_update['faces_model_not_load'] = True
                else:
                    # Модель загружена в момент работы программы
                    self._automatic_update['faces_model_not_load'] = False

            # Установка имени окна и имя окна было изменено
            if set_window_name is True and curr_window_name != self.title_faces_method_en:
                self.set_window_name(self.title_faces_method_en)  # Установка имени окна

        return True

    # Загрузка модели поиска лиц
    def _load_faces_model(self, out = True):
        """
        Загрузка модели поиска лиц

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если модель загружена, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Детектор лиц на основе глубокого обучения в OpenCV
        if self._args['method'] == self._methods_data[0]:
            return self.load_faces_model_opencv_dnn(dnn = self._args['dnn'], out = out)

    # Детектирование лиц
    def _faces_detection(self):
        """
        Детектирование лиц
        """

        # Отображение скелета лиц окне воспроизведения
        if self._args['show_labels'] is False and self._args['face_rectangle'] is True:
            # Формирование прозрачного наложения на текущий кадр кадра
            self._frame_transparent()

        res_detection = None  # Результат метода поиска лиц

        # Детектирование лиц с помощью глубокого обучения в OpenCV
        if self._args['method'] == self._methods_data[0]:
            res_detection = self.opencv_faces_dnn(
                net = self.model_faces,
                frame = self._curr_frame,
                width = self._args['size']['width'],
                height = self._args['size']['height'],
                conf_threshold = self._args['conf_face_threshold'],
                draw = self._args['face_rectangle'],
                draw_precent = self._args['draw_precent'],
                out = True
            )

        # Метод поиска лиц не выполнен
        if res_detection is None:
            return False

    # Захват фото
    def _grab_data(self, out = True):
        """
        Захват фото

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если захват фото произведен, в обратном случае False
        """

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._grab_data(out) is False:
            return False

        return True

    # Операции над кадром
    def _frame_o(self, func = None, out = True):
        """
        Операции над кадром

        ([FunctionType, bool]) -> bool

        Аргументы:
            func - Функция или метод
            out  - Печатать процесс выполнения

        Возвращает: True если операции над кадром произведены, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self._frame_o.__name__)

            return False

        self._faces_detection()  # Детектирование лиц

        # Отображение скелета в окне воспроизведения
        if self._args['show_labels'] is False and self._args['face_rectangle'] is True:
            self._composite()  # Формирование итогового кадра

        return True

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
        if super()._loop(other_source, self._frame_o, out) is False:
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

        # Загрузка модели поиска лиц
        if self._load_faces_model(out) is False:
            return False

        self.window_name = self.title_faces_method_en  # Установка имени окна

        # Запуск процесса извлечения изображений
        if start is True:
            self.set_loop(self._loop)  # Циклическая функция извлечения изображений
            self.start()  # Запуск


def main():
    run = Run()

    run.run()


if __name__ == "__main__":
    main()
