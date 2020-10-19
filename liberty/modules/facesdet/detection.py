#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Детектирование лиц
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os             # Работа с файловой системой
import cv2            # Алгоритмы компьютерного зрения
import pkg_resources  # Работа с ресурсами внутри пакетов
import numpy as np    # Научные вычисления

from datetime import datetime  # Работа со временем

# Персональные
from liberty.samples import play  # Пример воспроизведения фото/видео данных


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(play.Run):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._description = self._('Детектирование лиц')
        self._description_time = '{}{}' + self._description + ' ...{}'

        self._load_faces_model_start = self._('[{}] Загрузка модели "{}" ...')
        self._model_not_load = self._('[{}{}{}] Модель "{}" не загружена ...')
        self._face_found_in_frame = self._('Лиц: {}')
        self._face_not_found_in_frame = self._('Лица не найдены ...')
        self._face_precent = '{:.2f}%'


# ######################################################################################################################
# Анализ лицевых характеристик человека в маске
# ######################################################################################################################
class Detection(Messages):
    """Анализ лицевых характеристик человека в маске"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self.title_faces_method = self._('Метод')  # Название метода
        self.title_faces_method_en = 'Method'  # Название метода на английском (для окна приложения)

        # Необходимые расширения для моделей
        self._required_extension_models = (
            'pbtxt', 'pb',  # Детектирование лиц с помощью глубокого обучения в OpenCV (TensorFlow)
            'prototxt', 'caffemodel',  # Детектирование лиц с помощью глубокого обучения в OpenCV (Caffe)
        )

        self._dnn = ('tf', 'caffe')  # Модели нейронной сети

        # Данные методов
        self._packages_functions = {
            'opencv_dnn': {
                'all': self._('Детектирование лиц с помощью глубокого обучения в OpenCV'),
                'en': 'Faces detection with deep learning in OpenCV'
            },
        }

        # Названия моделей и их конфигурационных файлов
        self._path_to_files_models = {
            'opencv_dnn': {
                'tf': {
                    'path_to_model': 'opencv_face_detector_uint8.pb',
                    'path_to_config_model': 'opencv_face_detector.pbtxt'
                },
                'caffe': {
                    'path_to_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
                    'path_to_config_model': 'deploy.prototxt'
                }
            }
        }

        # Путь к моделям
        self._path_to_models = pkg_resources.resource_filename(
            'liberty',
            os.path.join('modules', 'facesdet', 'models')
        )

        # Добавление вариантов ошибок при автоматическом обновлении конфигурационного файла
        self._automatic_update['faces_model_not_load'] = False  # Модель не загружена

        self._model_faces = None  # Модель поиска лиц

        # Шрифты
        #    1. Для лиц
        self._fonts.append('face')

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение названия метода
    @property
    def title_faces_method(self):
        return self._title_faces_method

    # Установка названия метода
    @title_faces_method.setter
    def title_faces_method(self, name):
        self._title_faces_method = name

    # Получение названия метода на английском
    @property
    def title_faces_method_en(self):
        return self._title_faces_method_en

    # Установка названия метода на английском
    @title_faces_method_en.setter
    def title_faces_method_en(self, name):
        self._title_faces_method_en = name

    # Получение названий методов
    @property
    def packages_functions(self):
        return self._packages_functions

    # Получение модели
    @property
    def model_faces(self):
        return self._model_faces

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Загрузка модели для глубокого обучения в OpenCV
    def load_faces_model_opencv_dnn(self, path_to_model = None, path_to_config_model = None, dnn = 'tf', out = True):
        """
        Загрузка модели для метода Виолы-Джонса в OpenCV
        (str, str, str [, bool]) -> bool
        Аргументы:
            path_to_model        - Путь к модели
            path_to_config_model - Путь к конфигурационному файлу модели
            dnn                  - Модель нейронной сети
            out                  - Печатать процесс выполнения
        Возвращает: True если модель загружена, в обратном случае False
        """

        none = 'DL'  # Замена None

        # Путь к модели по умолчанию
        if path_to_model is None:
            path_to_model = none

        # Путь к конфигурационному файлу модели по умолчанию
        if path_to_config_model is None:
            path_to_config_model = none

        # Проверка аргументов
        if type(path_to_model) is not str or not path_to_model or type(path_to_config_model) is not str \
                or not path_to_config_model or type(dnn) is not str or not dnn or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.load_faces_model_opencv_dnn.__name__)

            return False

        # Модель нейронной сети не совпадает с необходимыми
        if dnn not in self._dnn:
            return False

        # Путь к модели по умолчанию
        if path_to_model is none:
            path_to_model = \
                os.path.join(self._path_to_models, self._path_to_files_models['opencv_dnn'][dnn]['path_to_model'])

        # Путь к конфигурационному файлу модели по умолчанию
        if path_to_config_model is none:
            path_to_config_model = os.path.join(
                self._path_to_models, self._path_to_files_models['opencv_dnn'][dnn]['path_to_config_model']
            )

        required_extension_model = None  # Необходимое расширения файла модели
        required_extension_config_model = None  # Необходимое расширения конфигурационного файла модели

        # 8-битная квантованная версия с использованием TensorFlow
        if dnn == self._dnn[0]:
            # Необходимое расширения файла модели
            required_extension_model = self._required_extension_models[1]

            # Необходимое расширения конфигурационного файла модели
            required_extension_config_model = self._required_extension_models[0]

        # Версия FP16 оригинальной реализации Caffe
        if dnn == self._dnn[1]:
            # Необходимое расширения файла модели
            required_extension_model = self._required_extension_models[3]

            # Необходимое расширения конфигурационного файла модели
            required_extension_config_model = self._required_extension_models[2]

        # Файл модели не найден
        if self.search_file(path_to_model, required_extension_model, False, out) is False:
            return False

        # Конфигурационный файл модели не найден
        if self.search_file(path_to_config_model, required_extension_config_model, False, out) is False:
            return False

        # Вывод сообщения
        if out is True:
            print(self._load_faces_model_start.format(
                datetime.now().strftime(self._format_time),
                self.packages_functions['opencv_dnn']['all']
            ))

        try:
            # 8-битная квантованная версия с использованием TensorFlow
            if dnn == self._dnn[0]:
                # Чтение модели нейронной сети в формате TensorFlow
                self._model_faces = cv2.dnn.readNetFromTensorflow(path_to_model, path_to_config_model)

            # Версия FP16 оригинальной реализации Caffe
            if dnn == self._dnn[1]:
                # Чтение модели нейронной сети в формате Caffe
                self._model_faces = cv2.dnn.readNetFromCaffe(path_to_config_model, path_to_model)
        except SystemError:
            # Вывод сообщения
            if out is True:
                print(self._model_not_load.format(self.red, datetime.now().strftime(self._format_time), self.end,
                                                  os.path.basename(path_to_model)))

            return False

        # Установка названия метода
        self.title_faces_method = self.packages_functions['opencv_dnn']['all']  # Перевод на текущий язык
        self.title_faces_method_en = self.packages_functions['opencv_dnn']['en']  # Английский

        return True

    # Детектирование лиц с помощью глубокого обучения в OpenCV
    def opencv_faces_dnn(self, net, frame, width = 300, height = 0, conf_threshold = 0.7, draw = True,
                         draw_precent = True, out = True):
        """
        Детектирование лиц с помощью глубокого обучения в OpenCV

        (cv2.dnn_Net, numpy.ndarray [, int, int, float, bool, bool, bool]) -> tuple or None

        Аргументы:
            net            - Нейронная сеть
            frame          - Изображение
            width          - Ширина изображения для масштабирования
            height         - Высота изображения для масштабирования
            conf_threshold - Доверительный порог
            draw           - Рисование на изображении областей с лицами
            draw_precent   - Рисование на изображении процентов для каждого найденного лица
            out            - Печатать процесс выполнения

        Возвращает кортеж:
            1. Обработанное изображение
            2. Список координат лиц
        """

        # Проверка аргументов
        if (type(net) is not cv2.dnn_Net or type(frame) is not np.ndarray or len(frame) is 0
                or type(height) is not int or height < 0 or type(width) is not int or width < 0
                or type(conf_threshold) is not float or conf_threshold < 0 or conf_threshold > 1
                or type(draw) is not bool or type(draw_precent) is not bool or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.opencv_faces_dnn.__name__)

            return None

        # Формат изображения
        if frame.shape[2] == 3:
            frame_clone = frame.frame.copy()  # Копирование изображения
        elif frame.shape[2] == 4:
            frame_clone = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)  # Копирование изображения
        else:
            return None

        frame_height = frame_clone.shape[0]  # Высота изображения
        frame_width = frame_clone.shape[1]  # Ширина изображения

        # Параметр ширины не указан
        if not width:
            width = frame_width

        # Параметр высоты не указан
        if not height:
            height = int(frame_height * width / frame_width)  # Масштабирование ширины относительно ширины

        # Обработка входного изображения
        # - Вычитание среднего значения из элементов каждого канала
        # - Масштабирование изображения
        blob = cv2.dnn.blobFromImage(frame_clone, 1.0, (width, height), [104, 117, 123], False, False)

        net.setInput(blob)  # Прогонка обработанного входного изображения через сеть
        detections = net.forward()  # Прогнозы с обнаруженными лицами

        faces_boxes = []  # Список кординат лиц

        # Пройтись по всем прогнозам с лицами
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Получение текущего прогноза

            # Прогноз больше доверительного порога
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frame_width)  # Начальная координата по оси X
                y1 = int(detections[0, 0, i, 4] * frame_height)  # Начальная координата по оси Y
                x2 = int(detections[0, 0, i, 5] * frame_width)  # Конечная координата по оси X
                y2 = int(detections[0, 0, i, 6] * frame_height)  # Конечная координата по оси Y

                # Получение ограничивающего прямоугольника лица
                rectangle_face = self.get_rectangle_face(x1, y1, x2, y2)
                # Координаты ограничивающего прямоугольника найдены
                if rectangle_face is not None:
                    x1, y1, x2, y2 = rectangle_face

                faces_boxes.append([x1, y1, x2, y2])  # Добавление прямоугольной области с лицом в список координат лиц

                # Рисование прямоугольной области с лицом на изображении
                if draw is True:
                    # Рисование на изображении процентов для каждого найденного лица
                    if draw_precent is True:
                        label_face = self._face_precent.format(confidence * 100)  # Процент лица

                        # Размеры текста
                        (width_text_top, height_text_top), (offset_x_top, offset_y_top) = \
                            self._font['face'].font.getsize(label_face)

                        # Верхняя левая точка прямоугольника
                        labels_base_coords = [
                            x1,
                            y1 - height_text_top - (self._args['face_padding'] * 2) - self._args['face_distance']
                        ]

                        # Координаты выходят за рамки
                        if labels_base_coords[1] <= 0:
                            labels_base_coords[1] = y1
                        # Выполнять пока текст не будет входить в рамки окна
                        while True:
                            if labels_base_coords[0] + width_text_top + (self._args['face_padding'] * 2) > \
                                    self._curr_frame.shape[1]:
                                labels_base_coords[0] -= 1
                                continue

                            break

                        # Нанесение информации на изображение (проценты найденного лица)
                        self._draw_info(
                            text = label_face,
                            base_coords = (
                            labels_base_coords[0], labels_base_coords[1]),
                            background_color = (self._args['face_background_color']['red'],
                                                self._args['face_background_color']['green'],
                                                self._args['face_background_color']['blue'],
                                                self._args['face_background_color']['alpha']),
                            text_color = (self._args['face_text_color']['red'],
                                          self._args['face_text_color']['green'],
                                          self._args['face_text_color']['blue'],
                                          self._args['face_text_color']['alpha']),
                            stroke = self._args['face_stroke'],
                            stroke_color = (self._args['face_stroke_color']['red'],
                                            self._args['face_stroke_color']['green'],
                                            self._args['face_stroke_color']['blue'],
                                            self._args['face_stroke_color']['alpha']),
                            padding = self._args['face_padding'],
                            font = self._font['face'],
                            out = out
                        )

        # Всего лиц
        cnt_bodies = self._face_found_in_frame.format(len(faces_boxes))

        # Отображение надписей в терминале
        if self._args['show_labels'] is False and self._automatic_update['faces_model_not_load'] is False \
                and self._switch_file is False:
            # Лица не найдены
            if len(faces_boxes) == 0:
                cnt_bodies = self._face_not_found_in_frame

            # Надпись для терминала
            self._curr_stdout += ', {}'.format(cnt_bodies.lower())
        else:
            # Координаты нижней левой точки определены (метка FPS)
            if self._fps_point2 is not None:
                # Нанесение информации на изображение
                self._draw_info(
                    text = cnt_bodies,
                    base_coords = (self._args['labels_base_coords']['left'],
                                   self._fps_point2[1] + self._args['labels_distance']),
                    background_color = (self._args['info_background_color']['red'],
                                        self._args['info_background_color']['green'],
                                        self._args['info_background_color']['blue'],
                                        self._args['info_background_color']['alpha']),
                    text_color = (self._args['info_text_color']['red'],
                                  self._args['info_text_color']['green'],
                                  self._args['info_text_color']['blue'],
                                  self._args['info_text_color']['alpha']),
                    stroke = self._args['info_stroke'],
                    stroke_color = (self._args['info_stroke_color']['red'],
                                    self._args['info_stroke_color']['green'],
                                    self._args['info_stroke_color']['blue'],
                                    self._args['info_stroke_color']['alpha']),
                    font = self._font['info'],
                    padding = self._args['labels_padding'],
                    out = out
                )

        # Результат
        return frame_clone, faces_boxes

    # Получение ограничивающего прямоугольника лица
    def get_rectangle_face(self, x1, y1, x2, y2):
        """
        Получение ограничивающего прямоугольника лица

        (int, int, int, int) -> list or None

        Аргументы:
            x1 - Начальная координата по оси X
            y1 - Начальная координата по оси Y
            x2 - Конечная координата по оси X
            y2 - Конечная координата по оси Y

        Возвращает список координат лиц если отрисовка ограничивающего прямоугольника лица успешна или None
        """

        # Проверка аргументов
        if type(x1) is not int or type(y1) is not int or type(x2) is not int or type(y2) is not int:
            return None

        # Координаты ограничивающего прямоугольника найденного лица
        left = self._curr_frame.shape[1]  # X самой левой точки
        right = 0  # X самой правой точки
        top = self._curr_frame.shape[0]  # Y самой верхней точки
        bottom = 0  # Y самой нижней точки

        # Отступы
        padding_x = int(round((x2 - x1) * self._args['padding_face']['width'] / 43))
        padding_y = int(round((y2 - y1) * self._args['padding_face']['height'] / 58))

        # Координаты ограничивающего прямоугольника найденного лица
        try:
            left = min([left, x1])
            right = max([right, x2])
            top = min([top, y1])
            bottom = max([bottom, y2])
        except ValueError:
            return None

        # Координаты ограничивающего прямоугольника найденного лица
        left = left - padding_x if left - padding_x > 0 else 0
        top = top - padding_y if top - padding_y > 0 else 0
        right = right + padding_x if right + padding_x < self._curr_frame.shape[1] \
            else self._curr_frame.shape[1] - self._args['face_rectangle_outline_size']
        bottom = bottom + padding_y if bottom + padding_y < self._curr_frame.shape[0] \
            else self._curr_frame.shape[0] - self._args['face_rectangle_outline_size']

        # Рисование прямоугольной области с лицом на изображении
        if self._args['face_rectangle'] is True:
            # Ограничивающий прямоугольник найденного скелета
            self._curr_frame_pil_obj.rectangle(
                [left, top, right, bottom],
                outline = (self._args['face_rectangle_outline_color']['red'],
                           self._args['face_rectangle_outline_color']['green'],
                           self._args['face_rectangle_outline_color']['blue'],
                           self._args['face_rectangle_outline_color']['alpha']),
                fill = (self._args['face_rectangle_background_color']['red'],
                        self._args['face_rectangle_background_color']['green'],
                        self._args['face_rectangle_background_color']['blue'],
                        self._args['face_rectangle_background_color']['alpha']),
                width = self._args['face_rectangle_outline_size']
            )

        return [left, top, right, bottom]
