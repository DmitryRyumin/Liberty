#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Управление ассистивным мобильным информационным роботом посредством автоматического распознавания жестовой информации
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import numpy as np  # Научные вычисления

# Персональные
from liberty.samples import kinect2play  # Пример воспроизведения фото/видео данных


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(kinect2play.Run):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._description = self._(
            'Управление ассистивным мобильным информационным роботом '
            'посредством автоматического распознавания жестовой информации'
        )
        self._description_time = '{}{}' + self._description + ' ...{}'


# ######################################################################################################################
# Распознавание жестов
# ######################################################################################################################
class GestureRecognizer(Messages):
    """Класс для распознавания жестов"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._mean_zs = None  # Минимальное значение глубины (ближайший человек)
        self._near_bodies = 0  # Ближайший из найденных скелетов

        self._range_padding = None  # Диапазон отступов
        self._range_depth = list(range(450, 4501, 1))  # Диапазон карты глубины

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Установка диапазона отступов
    def range_padding(self, min_padd, max_padd, out = True):
        """
        Установка диапазона отступов

        (int, int, bool) -> bool

        Аргументы:
            min_padd - Минимальный отступ для ограничивающего прямоугольника
            max_padd - Максимальный отступ для ограничивающего прямоугольника
            out      - Печатать процесс выполнения

        Возвращает: True если диапазон отступов установлен, в обратном случае False
        """

        # Проверка аргументов
        if type(min_padd) is not int or min_padd < 0 or type(max_padd) is not int or max_padd < 0 \
                or min_padd >= max_padd or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                self._inv_args(__class__.__name__, self.range_padding.__name__)

            return False

        self._range_padding = np.linspace(max_padd, min_padd, num = 4500 - 500 + 1)

        return True

    # Получение ограничивающего прямоугольника ближайшего скелета
    def get_rectangle_bodies(self):
        """
        Получение ограничивающего прямоугольника ближайшего скелета

        () -> bool

        Возвращает: True если обработка кадра для распознавания жеста успешна, в обратном случае False
        """

        # Координаты ограничивающего прямоугольника найденного скелета
        left = self._curr_frame.shape[1]  # X самой левой точки
        right = 0  # X самой правой точки
        top = self._curr_frame.shape[0]  # Y самой верхней точки
        bottom = 0  # Y самой нижней точки

        # Списки координат суставов
        xs = []
        ys = []

        # Проход по суставам ближайшей скелетной модели
        for k, v in self._skeleton_landmarks_color[self._near_bodies].items():
            # Точка не определена
            if v is None:
                continue

            xs.append(v['x'])  # Координата X
            ys.append(v['y'])  # Координата Y

        # Координаты ограничивающего прямоугольника найденного скелета
        try:
            left = min(xs)
            right = max(xs)
            top = min(ys)
            bottom = max(ys)
        except ValueError:
            return False

        # Вычисление отступов для ограничивающего прямоугольника
        try:
            padding = int(round(self._range_padding[self._range_depth.index(int(round(self._mean_zs, 0)))], 0))
        except ValueError:
            return False

        # Координаты ограничивающего прямоугольника найденного скелета
        left = left - padding if left - padding > 0 else 0
        top = top - padding if top - padding > 0 else 0
        right = right + padding if top + padding < self._curr_frame.shape[1] \
            else self._curr_frame.shape[1] - self._args['skeleton_rectangle_outline_size']
        bottom = bottom + padding if bottom + padding < self._curr_frame.shape[0] \
            else self._curr_frame.shape[0] - self._args['skeleton_rectangle_outline_size']

        # Отрисовка ограничивающих прямоугольников найденных скелетов
        if self._args['skeleton_rectangle'] is True:
            # Ограничивающий прямоугольник найденного скелета
            self._curr_frame_pil_obj.rectangle(
                [left, top, right, bottom],
                outline = (self._args['skeleton_rectangle_outline_color']['red'],
                           self._args['skeleton_rectangle_outline_color']['green'],
                           self._args['skeleton_rectangle_outline_color']['blue'],
                           self._args['skeleton_rectangle_outline_color']['alpha']),
                fill = (self._args['skeleton_rectangle_background_color']['red'],
                        self._args['skeleton_rectangle_background_color']['green'],
                        self._args['skeleton_rectangle_background_color']['blue'],
                        self._args['skeleton_rectangle_background_color']['alpha']),
                width = self._args['skeleton_rectangle_outline_size']
            )

    # Получение ближайшего скелета
    def get_near_body(self):
        """
        Получение ближайшего скелета

        () -> bool

        Возвращает: True если ближайший скелет получен, в обратном случае False
        """

        # Скелеты не найдены
        if self._cnt_bodies == 0:
            return None

        # Проход по ориентирам скелетов для соединения линиями
        for key, val in self._skeleton_landmarks_depth.items():
            zs = []

            # Проход по карте глубины
            for k, v in val.items():
                # Точка не определена
                if v is None:
                    continue

                if v['z'] > 0:
                    zs.append(v['z'])  # Координата Z

            # Средняя координата Z
            try:
                zs = round(np.mean(zs), 3)
            except ValueError:
                return False

            # Ближайший скелет не определен
            if self._mean_zs is None or self._mean_zs > zs:
                self._near_bodies = key  # Ближайший из найденных скелетов
                self._mean_zs = zs  # Минимальное расстояние до ближайшего скелета

        self.get_rectangle_bodies()  # Получение ограничивающего прямоугольника ближайшего скелета

        self.draw_bodies()  # Отрисовка ориентиров скелета

        self._mean_zs = None  # Минимальное значение глубины (ближайший человек)

        return True
