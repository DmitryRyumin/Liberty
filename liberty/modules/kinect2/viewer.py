#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение видеоданных из сенсора Kinect 2
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import time         # Работа со временем
import numpy as np  # Научные вычисления
import cv2          # Алгоритмы компьютерного зрения

from datetime import datetime               # Работа со временем
from _testcapi import USHRT_MAX             # Максимально доступное число для формата ushort
from types import ModuleType                # Проверка объектов на модуль, метод, функцию
from types import FunctionType, MethodType  # Проверка объектов на метод, функцию

# Персональные
from liberty.modules.kinect2.core.cap import Cap        # Заглушка
from liberty.modules.kinect2 import xml as kinect2_xml  # XML файлы
from liberty.samples import play                        # Пример воспроизведения фото/видео данных

# ######################################################################################################################
# Заглушка
# ######################################################################################################################

cap = Cap()

if cap.win8_later() is False:
    raise SystemExit(0)

from liberty.modules.kinect2.core import PyKinectRuntime, PyKinectV2  # Работа с Kinect 2


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

        self._description = self._('Воспроизведение видеоданных из сенсора Kinect 2')
        self._description_time = '{}{}' + self._description + ' ...{}'

        self._kinect_run = self._('[{}] Запуск сенсора Kinect 2 ...')
        self._kinect_not_found = ' ' * 4 + \
                                 self._('[{}{}{}] Достигнут лимит ожидания запуска сенсора Kinect 2 в {} секунд ...')


# ######################################################################################################################
# Воспроизведение видеоданных из сенсора Kinect 2
# ######################################################################################################################
class KinectViewer(Messages):
    """Класс для Воспроизведения видеоданных из сенсора Kinect 2"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._kinect = None  # Kinect 2
        # Текущие кадры
        self._curr_frame_depth = None  # Карта глубины
        self._depth_frame = None  # Карта глубины с сырыми данными
        self._curr_frame_infrared = None  # Инфракрасный кадр

        self._wait = 10  # Количество секунд для ожидания включения Kinect 2

        self._cnt_bodies = 0  # Количество найденных скелетов

        self._skeleton_landmarks_color = {}  # Ориентиры скелетов для соединения линиями
        self._skeleton_landmarks_depth = {}  # Ориентиры скелетов карт глубины

        self._list_landmarks_skeleton = []  # Массив с координатами ориентиров скелета для соединения линиями

        self._load_model_skeleton_one = False  # Функция заполнения массива с координатами ориентиров не выполнена

        # Получение значений во сколько раз масштабировалась карта глубины
        self._scale_depth = {
            'width': 1.0,
            'height': 1.0
        }

        self._right_margin = 0  # Правый отступ для карты глубины

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение Kinect 2
    @property
    def kinect(self):
        return self._kinect

    # ------------------------------------------------------------------------------------------------------------------
    #  Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Извлечение кординат скелетной точки
    def __draw_body_bone_color(self, joint_points, joints, joint):
        """
        Извлечение кординат скелетной точки

        TODO: Описание
        """

        # TODO: Проверка аргументов

        joint_state = joints[joint].TrackingState  # Отслеживание состояние сустава

        # Координаты сустава не отслежены
        if joint_state == PyKinectV2.TrackingState_NotTracked or joint_state == PyKinectV2.TrackingState_Inferred:
            return None

        # Координаты сустава
        x = int(joint_points[joint].x)
        y = int(joint_points[joint].y)

        # Координаты сустава
        return {
            'x': 0 if x < 0 else x,
            'y': 0 if y < 0 else y
        }

    # Извлечение кординат скелетной точки из карты глубины
    def __draw_body_bone_depth(self, joint_points, joints, joint):
        """
        Извлечение кординат скелетной точки из карты глубины

        TODO: Описание
        """

        # TODO: Проверка аргументов

        joint_state = joints[joint].TrackingState  # Отслеживание состояние сустава

        # Координаты сустава не отслежены
        if joint_state == PyKinectV2.TrackingState_NotTracked or joint_state == PyKinectV2.TrackingState_Inferred:
            return None

        # Координаты сустава
        x = int(joint_points[joint].x)
        y = int(joint_points[joint].y)
        z = int(self._depth_frame[y, x])

        # Координаты сустава
        return {
            'x': 0 if x < 0 else x,
            'y': 0 if y < 0 else y,
            'z': 0 if z < 0 else z
        }

    # Проверка XML файла на валидность
    def _valid_xml_skeleton(self, data, out = True):
        """
        Проверка настроек JSON на валидность

        (dict [, bool]) -> bool

        Аргументы:
            data - Словарь из XML файла
            out  - Печатать процесс выполнения

        Возвращает: True если файл валидный, в обратном случае False
        """

        # Проверка аргументов
        if type(data) is not dict or len(data) is 0 or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self._valid_xml_skeleton.__name__)

            return False

        # Словарь пуст
        if len(data) == 0:
            # Вывод сообщения
            if out is True:
                print(self._config_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return False

        # Вывод сообщения
        if out is True:
            print(self._check_config_file_valid.format(datetime.now().strftime(self._format_time)))

        # Значения словаря
        for key, val in data.items():
            if key != 'model' or type(val) is not dict:
                return False

            for key2, val2 in val.items():
                if key2 != 'skeleton' or type(val2) is not dict:
                    return False

                for key3, val3 in val2.items():
                    if key3 != 'points' or type(val3) is not list:
                        return False

                    for val4 in val3:
                        if type(val4) is not dict:
                            return False

                        for key5, val5 in val4.items():
                            val5 = int(val5)

                            # Проверка координат на валидность
                            if (key5 != '@a' and key5 != '@b') or val5 > 24 or val5 < 0:
                                return False

                        self._list_landmarks_skeleton.append({'a': int(val4['@a']), 'b': int(val4['@b'])})

        return True

    # Загрузка и проверка координат для отрисовки скелета
    def _load_model_skeleton(self, resources = kinect2_xml, xml = 'skeleton_lines.xml', out = True):
        """
        Загрузка и проверка координат для отрисовки скелета

        ([module, str, bool]) -> bool

        Аргументы:
            resources - Модуль с ресурсами
            xml       - XML файл
            out       - Печатать процесс выполнения

        Возвращает: True если файл загружен и валиден, в обратном случае False
        """

        if self._load_model_skeleton_one is True:
            return True

        # Проверка аргументов
        if type(out) is not bool or not isinstance(resources, ModuleType) or type(xml) is not str or not xml:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self._load_model_skeleton.__name__)

            return False

        # Загрузка XML файла из ресурсов модуля
        skeleton_json = self.load_resources_xml(resources, xml, out)

        # XML файл не загружен
        if skeleton_json is None:
            return False

        # Проверка XML файла на валидность
        res_valid_xml = self._valid_xml_skeleton(skeleton_json, out)

        # XML файл не валидный
        if res_valid_xml is False:
            return False

        # Функция заполнения массива с координатами ориентиров выполнена
        self._load_model_skeleton_one = True

        return self._load_model_skeleton_one

    # Нормализация ориентиров скелете из карты глубины
    def _norm_lines_depth(self, value, scale):
        """
        (int, float) -> int

        Аргументы:
            value - X или Y координата ориантира скелета
            scale - Значение во сколько раз масштабировалось изображение

        Возвращает: нормализованное значение координаты X или Y
        """

        # Проверка аргументов
        if type(value) is not int or value < 0 or type(scale) is not float or scale < 0:
            return None

        return round(value / scale, 0)

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Запуск
    def run_kinect(self, out = True):
        """
        Запуск Kinect 2

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если запуск Kinect произведен, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Вывод сообщения
        if out is True:
            print(self._kinect_run.format(datetime.now().strftime(self._format_time)))

        # Инициализация Kinect 2 на получение цветного изображения, карты глубины и скелетных моделей
        # noinspection PyUnreachableCode
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color
            | PyKinectV2.FrameSourceTypes_Body
            | PyKinectV2.FrameSourceTypes_Depth
            | PyKinectV2.FrameSourceTypes_Infrared
            | PyKinectV2.FrameSourceTypes_BodyIndex
        )

        start_time = time.time()  # Отсчет времени выполнения

        # Ожидаем получение информации из Kinect 2
        while True:
            if self._kinect.has_new_color_frame() and \
                    self._kinect.has_new_depth_frame() and \
                    self._kinect.has_new_infrared_frame():
                return True

            end_time = round(time.time() - start_time, 2)  # Конец времени выполнения

            if end_time >= self._wait:
                # Вывод сообщения
                if out is True:
                    print(self._kinect_not_found.format(
                        self.red, datetime.now().strftime(self._format_time), self.end, self._wait
                    ))

                return False

    # Получение цветного кадра из Kinect 2
    def get_color_frame(self):
        """
        Получение цветного кадра из Kinect 2
        """

        out_frame = self.kinect.get_last_color_frame()  # Получение цветного кадра с Kinect

        # Преобразование кадра в необходимый формат (1920, 1080, RGBA)
        self._curr_frame = cv2.cvtColor(out_frame.reshape(1080, 1920, -1).astype(np.uint8), cv2.COLOR_BGR2RGBA)

    # Получение карты глубины из Kinect 2
    def get_depth_frame(self):
        """
        Получение карты глубины из Kinect 2
        """

        out_frame = self.kinect.get_last_depth_frame()  # Получение карты глубины с Kinect

        # Преобразование карты глубины в необходимый формат (512, 424)
        self._depth_frame = out_frame.reshape((424, 512)).astype(np.uint16)

        out_frame = cv2.applyColorMap(
            cv2.convertScaleAbs(self._depth_frame, alpha = 255 / (4500 - 500)), cv2.COLORMAP_JET
        )

        self._curr_frame_depth = cv2.cvtColor(out_frame, cv2.COLOR_RGB2RGBA)

    # Получение инфракрасного кадра из Kinect 2
    def get_infrared_frame(self, norm = 0.32, out = True):
        """
        Получение инфракрасного кадра из Kinect 2

        ([float, bool]) -> None

        Аргументы:
            norm - Нормализация значений инфракрасной камеры
            out  - Печатать процесс выполнения
        """

        # Проверка аргументов
        if type(norm) is not float or norm < 0.01 or norm > 1 or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.get_infrared_frame.__name__)

            return None

        out_frame = self.kinect.get_last_infrared_frame()  # Получение инфракрасного кадра с Kinect

        # Преобразование инфракрасного кадра в необходимый формат (512, 424)
        out_frame = out_frame.reshape((424, 512)).astype(np.uint16)

        # Нормализация значений инфракрасной камеры
        if norm < 1.0:
            out_frame = cv2.max(
                0.01, cv2.min(
                    1.0, (out_frame / USHRT_MAX) / norm
                )
            ) * USHRT_MAX

        self._curr_frame_infrared = \
            cv2.cvtColor(cv2.convertScaleAbs(out_frame, alpha = 255 / USHRT_MAX), cv2.COLOR_GRAY2RGBA)

    # Отрисовка ориентиров скелета
    def draw_bodies(self):
        """
        Отрисовка ориентиров скелета
        """

        # Проход по ориентирам скелетов для соединения линиями
        for key, val in self._skeleton_landmarks_color.items():
            # Отрисовка линий соединения скелетных суставов
            if self._args['skeleton_tracking_lines'] is True:
                # Суставы скелетной модели
                skeleton_tracking_lines = list(val.values())

                # 1. Отображение карты глубины
                # 2. Отрисовка скелета на карте глубины
                if self._args['show_depth'] is True and self._args['skeleton_depth_tracking'] is True:
                    skeleton_tracking_lines_depth = list(self._skeleton_landmarks_depth[key].values())

                try:
                    # Пройтись по всем ориентирам скелета, которые получены из XML файла
                    for landmark_skeleton in self._list_landmarks_skeleton:
                        # Координата не определена
                        if skeleton_tracking_lines[landmark_skeleton['a']] is None \
                                or skeleton_tracking_lines[landmark_skeleton['b']] is None:
                            continue

                        # 1. Отображение карты глубины
                        # 2. Отрисовка скелета на карте глубины
                        if self._args['show_depth'] is True and self._args['skeleton_depth_tracking'] is True:
                            # Соединение ориентиров скелета линией
                            self._curr_frame_pil_obj.line(
                                [self._norm_lines_depth(
                                    skeleton_tracking_lines_depth[landmark_skeleton['a']]['x'],
                                    self._scale_depth['width']
                                ) + self._right_margin,
                                 self._norm_lines_depth(
                                     skeleton_tracking_lines_depth[landmark_skeleton['a']]['y'],
                                     self._scale_depth['height']
                                 ) + self._args['labels_base_coords_depth_ir']['top'],
                                 self._norm_lines_depth(
                                     skeleton_tracking_lines_depth[landmark_skeleton['b']]['x'],
                                     self._scale_depth['width']
                                 ) + self._right_margin,
                                 self._norm_lines_depth(
                                     skeleton_tracking_lines_depth[landmark_skeleton['b']]['y'],
                                     self._scale_depth['height']
                                 ) + self._args['labels_base_coords_depth_ir']['top']],
                                # Цвет фона точек скелетных суставов
                                fill = (self._args['skeleton_lines_color']['red'],
                                        self._args['skeleton_lines_color']['green'],
                                        self._args['skeleton_lines_color']['blue'],
                                        self._args['skeleton_lines_color']['alpha']),
                                # Ширина обводки фона точек скелетных суставов
                                width = self._args['skeleton_lines_width']
                            )

                        # Соединение ориентиров скелета линией
                        self._curr_frame_pil_obj.line(
                            [skeleton_tracking_lines[landmark_skeleton['a']]['x'],
                             skeleton_tracking_lines[landmark_skeleton['a']]['y'],
                             skeleton_tracking_lines[landmark_skeleton['b']]['x'],
                             skeleton_tracking_lines[landmark_skeleton['b']]['y']],
                            # Цвет фона точек скелетных суставов
                            fill = (self._args['skeleton_lines_color']['red'],
                                    self._args['skeleton_lines_color']['green'],
                                    self._args['skeleton_lines_color']['blue'],
                                    self._args['skeleton_lines_color']['alpha']),
                            width = self._args['skeleton_lines_width']  # Ширина обводки фона точек скелетных суставов
                        )
                except KeyError:
                    pass

            # 1. Отображение карты глубины
            # 2. Отрисовка скелета на карте глубины
            # 3. Отрисовка скелета
            if self._args['skeleton_tracking'] is True and self._args['show_depth'] is True \
                    and self._args['skeleton_depth_tracking'] is True:
                # Проход по всем точкам точкам скелета
                for k, v in self._skeleton_landmarks_depth[key].items():
                    # Точка не определена
                    if v is None:
                        continue

                    self._curr_frame_pil_obj.ellipse(
                        [self._norm_lines_depth(
                            v['x'],
                            self._scale_depth['width']
                        ) + self._right_margin - self._args['skeleton_point_radius'],
                         self._norm_lines_depth(
                             v['y'],
                             self._scale_depth['height']
                         ) + self._args['labels_base_coords_depth_ir']['top'] - self._args['skeleton_point_radius'],
                         self._norm_lines_depth(
                             v['x'],
                             self._scale_depth['width']
                         ) + self._right_margin + self._args['skeleton_point_radius'],
                         self._norm_lines_depth(
                             v['y'],
                             self._scale_depth['height']
                         ) + self._args['labels_base_coords_depth_ir']['top'] + self._args['skeleton_point_radius']],
                        # Цвет обводки фона точек скелетных суставов
                        outline = (self._args['skeleton_outline_color']['red'],
                                   self._args['skeleton_outline_color']['green'],
                                   self._args['skeleton_outline_color']['blue'],
                                   self._args['skeleton_outline_color']['alpha']),
                        # Цвет фона точек скелетных суставов
                        fill = (self._args['skeleton_point_background_color']['red'],
                                self._args['skeleton_point_background_color']['green'],
                                self._args['skeleton_point_background_color']['blue'],
                                self._args['skeleton_point_background_color']['alpha']),
                        width = self._args['skeleton_outline_size']  # Ширина обводки фона точек скелетных суставов
                    )

            # Отрисовка скелета
            if self._args['skeleton_tracking'] is True:
                # Проход по всем точкам точкам скелета
                for k, v in val.items():
                    # Точка не определена
                    if v is None:
                        continue

                    # Нанесение точки на кадр
                    self._curr_frame_pil_obj.ellipse(
                        [v['x'] - self._args['skeleton_point_radius'], v['y'] - self._args['skeleton_point_radius'],
                         v['x'] + self._args['skeleton_point_radius'], v['y'] + self._args['skeleton_point_radius']],
                        # Цвет обводки фона точек скелетных суставов
                        outline = (self._args['skeleton_outline_color']['red'],
                                 self._args['skeleton_outline_color']['green'],
                                 self._args['skeleton_outline_color']['blue'],
                                 self._args['skeleton_outline_color']['alpha']),
                        # Цвет фона точек скелетных суставов
                        fill = (self._args['skeleton_point_background_color']['red'],
                                self._args['skeleton_point_background_color']['green'],
                                self._args['skeleton_point_background_color']['blue'],
                                self._args['skeleton_point_background_color']['alpha']),
                        width = self._args['skeleton_outline_size']  # Ширина обводки фона точек скелетных суставов
                    )

    # Получение ориентиров скелета
    def get_bodies(self, draw = True, func = None, out = True):
        """
        Получение ориентиров скелета

        ([bool, FunctionType, bool])

        Аргументы:
            draw - Отрисовка ориентиров скелета
            func - Функция или метод
            out  - Печатать процесс выполнения
        """

        # Проверка аргументов
        if type(draw) is not bool or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.get_bodies.__name__)

            return None

        bodies = self.kinect.get_last_body_frame()  # Получение ориентиров скелета

        out_joints_color = {}  # Словарь с найдеными скелетами
        out_joints_depth = {}  # Словарь с найдеными скелетами карты глубины

        self._cnt_bodies = 0  # Обнуление количества найденных скелетов

        # Ориентиры скелета возможно присутствуют
        if bodies is not None:
            # Суставы скелетной модели
            joints_type = {
                'neck': PyKinectV2.JointType_Neck,                     # Шея
                'spine_shoulder': PyKinectV2.JointType_SpineShoulder,  # Позвоночник на уровне плеч
                'spine_mid': PyKinectV2.JointType_SpineMid,            # Позвоночник по центру тела
                'spine_base': PyKinectV2.JointType_SpineBase,          # Позвоночник на уровне ног (центр таза)
                'shoulder_right': PyKinectV2.JointType_ShoulderRight,  # Правое плечо
                'elbow_right': PyKinectV2.JointType_ElbowRight,        # Правый локоть
                'wrist_right': PyKinectV2.JointType_WristRight,        # Правое запястье
                'shoulder_left': PyKinectV2.JointType_ShoulderLeft,    # Левое плечо
                'elbow_left': PyKinectV2.JointType_ElbowLeft,          # Левый локоть
                'wrist_left': PyKinectV2.JointType_WristLeft,          # Левое запястье
                'hand_right': PyKinectV2.JointType_HandRight,          # Правая рука
                'hand_left': PyKinectV2.JointType_HandLeft,            # Левая рука
                'trumb_right': PyKinectV2.JointType_ThumbRight,        # Большой палец правой руки
                'hand_tip_right': PyKinectV2.JointType_HandTipRight,   # 4 пальца правой руки
                'trumb_left': PyKinectV2.JointType_ThumbLeft,          # Большой палец левой руки
                'hand_tip_left': PyKinectV2.JointType_HandTipLeft,     # 4 пальца левой руки
                'hip_right': PyKinectV2.JointType_HipRight,            # Правое бедро
                'knee_right': PyKinectV2.JointType_KneeRight,          # Правое колено
                'ankle_right': PyKinectV2.JointType_AnkleRight,        # Правая лодыжка
                'foot_right': PyKinectV2.JointType_FootRight,          # Правая нога
                'hip_left': PyKinectV2.JointType_HipLeft,              # Левое бедро
                'knee_left': PyKinectV2.JointType_KneeLeft,            # Левое колено
                'ankle_left': PyKinectV2.JointType_AnkleLeft,          # Левая лодыжка
                'foot_left': PyKinectV2.JointType_FootLeft,            # Левая нога
                'head': PyKinectV2.JointType_Head                      # Голова
            }

            # Пройтись по всем возможным скелетам
            for i in range(0, self.kinect.max_body_count):
                body = bodies.bodies[i]  # Скелетная модель
                # Скелетная модель не найдена
                if not body.is_tracked:
                    continue

                self._cnt_bodies += 1  # Увеличение счетчика количества найденных скелетов

                temp_joints_color = {}  # Ориентиры найденного скелета
                temp_joints_depth = {}  # Ориентиры найденного скелета карты глубины

                joints = body.joints  # Скелетная модель

                # Получение скелетной модели для цветного кадра
                joint_points_color = self.kinect.body_joints_to_color_space(joints)

                # Получение скелетной модели для карты глубины
                joint_points_depth = self.kinect.body_joints_to_depth_space(joints)

                # Проход по всем возможным суставам скелетной модели
                for key, val in joints_type.items():
                    # Извлечение кординат скелетной точки
                    temp_joints_color[key] = self.__draw_body_bone_color(joint_points_color, joints, val)

                    # Извлечение кординат скелетной точки карт глубины
                    temp_joints_depth[key] = self.__draw_body_bone_depth(joint_points_depth, joints, val)

                # Добавление скелета в словарь со всеми найденными скелетами
                out_joints_color[self._cnt_bodies] = temp_joints_color  # Цветное изображение
                out_joints_depth[self._cnt_bodies] = temp_joints_depth  # Карта глубины

                # Выполнение функции/метода
                if func is not None and (type(func) is MethodType or type(func) is FunctionType) and \
                        self._automatic_update['invalid_config_file'] is False:
                    func()  # Выполнение операций над изображением

        # Ориентиры скелетов
        self._skeleton_landmarks_color = out_joints_color  # Цветная камера
        self._skeleton_landmarks_depth = out_joints_depth  # Карта глубины

        # Отрисовка ориентиров скелета
        if draw is True:
            self.draw_bodies()  # Отрисовка ориентиров скелета
