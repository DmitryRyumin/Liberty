#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Воспроизведение видеоданных из сенсора Kinect 2

python liberty/samples/kinect2play.py [<command> --config путь_к_конфигурационному_файлу
    --frames_to_update 25 --automatic_update --no_clear_shell]
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
from datetime import datetime  # Работа со временем

# Персональные
import liberty  # Воспроизведение фото/видео данных

from liberty import configs                              # Конфигурационные файлы
from liberty.modules.kinect2.viewer import KinectViewer  # Воспроизведение видеоданных из сенсора Kinect 2


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(KinectViewer):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._check_depth_not_received = self._('Ошибка! Карта глубины не получена ...')
        self._check_inf_not_received = self._('Ошибка! Инфракрасный кадр не получен ...')

        self._people = self._('Людей: {}')


# ######################################################################################################################
# Выполняем только в том случае, если файл запущен сам по себе
# ######################################################################################################################
class Run(Messages):
    """Класс для воспроизведения видеоданных из сенсора Kinect 2"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        # Добавление вариантов ошибок при автоматическом обновлении конфигурационного файла
        self._automatic_update['depth_not_received'] = False  # Карта глубины не получена
        self._automatic_update['inf_not_received'] = False  # Инфракрасный кадр не получен

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

        # Переопределение значений из конфигурационного файла (только те которые не нужны на данном этапе)
        config['repeat'] = False  # Повторение воспроизведения видеопотока
        config['clear_image_buffer'] = True  # Очистка буфера с изображением
        config['real_time'] = False  # Повторение воспроизведения видеопотока
        config['fps'] = 0  # Пользовательский FPS
        # Цвет текста повтора воспроизведения
        config['repeat_text_color'] = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 0}
        # Цвет фона повтора воспроизведения
        config['repeat_background_color'] = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 0}
        # Размер шрифта текста повтора воспроизведения
        config['repeat_size'] = 1
        # Ширина обводки текста повтора воспроизведения
        config['repeat_stroke'] = 0
        # Цвет обводки текста повтора воспроизведения
        config['repeat_stroke_color'] = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 0}

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._valid_json_config(config, out) is False:
            return False

        curr_all_layer = all_layer = 4  # Общее количество разделов
        curr_valid_layer = 0  # Валидное количество разделов

        # Проход по всем разделам конфигурационного файла
        for key, val in config.items():
            # 1. Отображение карты глубины
            # 2. Отображение инфракрасного кадра
            if key == 'show_depth' or key == 'show_infrared':
                # Проверка значения
                if type(val) is not bool:
                    continue

                # Общее количество разделов не изменялось
                if curr_all_layer == all_layer:
                    if config['show_infrared'] is True or config['show_depth'] is True:
                        # Добавляем:
                        #     1. Размер карты глубины и инфракрасного кадра для масштабирования
                        #     2. Координаты карты глубины и инфракрасного кадра относительно верхнего правого угла
                        all_layer += 2

                    if config['show_depth'] is True:
                        # Добавляем:
                        #     Отрисовка скелета на карте глубины
                        all_layer += 1

                    if config['show_infrared'] is True:
                        # Добавляем:
                        #     Нормализация значений инфракрасной камеры
                        all_layer += 1

                        if config['show_depth'] is True:
                            # Добавляем:
                            #     Расстояние между картой глубины и инфракрасным кадром
                            all_layer += 1

                curr_valid_layer += 1

            # Размер карты глубины и инфракрасного кадра для масштабирования
            if key == 'resize_depth_ir':
                # Отображение карты глубины и/или инфракрасного кадра
                if (('show_depth' in config and config['show_depth'] is True) or
                        ('show_infrared' in config and config['show_infrared'] is True)):
                    all_layer_2 = 1  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) == 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 512:
                            continue

                        # Ширина изображения для масштабирования
                        if k == 'width':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # Начальные координаты карты глубины и инфракрасного кадра относительно верхнего правого угла
            if key == 'labels_base_coords_depth_ir':
                # Отображение карты глубины и/или инфракрасного кадра
                if (('show_depth' in config and config['show_depth'] is True) or
                        ('show_infrared' in config and config['show_infrared'] is True)):
                    all_layer_2 = 2  # Общее количество подразделов в текущем разделе
                    curr_valid_layer_2 = 0  # Валидное количество подразделов в текущем разделе

                    # Проверка значения
                    if type(val) is not dict or len(val) == 0:
                        continue

                    # Проход по всем подразделам текущего раздела
                    for k, v in val.items():
                        # Проверка значения
                        if type(v) is not int or v < 0 or v > 100:
                            continue

                        # 1. Право
                        # 2. Вверх
                        if k == 'right' or k == 'top':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # Расстояние между картой глубины и инфракрасным кадром
            if key == 'distance_between_depth_ir':
                # Отображение карты глубины и инфракрасного кадра
                if ('show_depth' in config and config['show_depth'] is True and
                        'show_infrared' in config and config['show_infrared'] is True):
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 50:
                        continue

                    curr_valid_layer += 1

            # Нормализация значений инфракрасной камеры
            if key == 'norm_infrared':
                # Отображение инфракрасного кадра
                if 'show_infrared' in config and config['show_infrared'] is True:
                    # Проверка значения
                    if type(val) is not float or val < 0.01 or val > 1.0:
                        continue

                    curr_valid_layer += 1

            # Отрисовка скелета
            if key == 'skeleton_tracking':
                # Проверка значения
                if type(val) is not bool:
                    continue

                # Отрисовка скелета необходима
                if val is True:
                    # Добавляем:
                    #     1. Радиус точек скелетных суставов
                    #     2. Цвет фона точек скелетных суставов
                    #     3. Цвет обводки фона точек скелетных суставов
                    #     4. Ширина обводки фона точек скелетных суставов
                    all_layer += 4

                curr_valid_layer += 1

            # Отрисовка скелета на карте глубины
            if key == 'skeleton_depth_tracking':
                #  Отрисовка скелета
                if 'show_depth' in config and config['show_depth'] is True:
                    # Проверка значения
                    if type(val) is not bool:
                        continue

                    # Отрисовка скелета необходима
                    if val is True and 'skeleton_tracking' not in config:
                        # Добавляем:
                        #     1. Радиус точек скелетных суставов
                        #     2. Цвет фона точек скелетных суставов
                        #     3. Цвет обводки фона точек скелетных суставов
                        #     4. Ширина обводки фона точек скелетных суставов
                        all_layer += 4

                    curr_valid_layer += 1

            # Радиус точек скелетных суставов
            if key == 'skeleton_point_radius':
                #  Отрисовка скелета
                if 'skeleton_tracking' in config and config['skeleton_tracking'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 1 or val > 10:
                        continue

                    curr_valid_layer += 1

            # 1. Цвет фона точек скелетных суставов
            # 2. Цвет обводки фона точек скелетных суставов
            if key == 'skeleton_point_background_color' or key == 'skeleton_outline_color':
                #  Отрисовка скелета
                if 'skeleton_tracking' in config and config['skeleton_tracking'] is True:
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
                        # 3. Прозрачность
                        if k == 'red' or k == 'green' or k == 'blue' or k == 'alpha':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
                        curr_valid_layer += 1

            # Ширина обводки фона точек скелетных суставов
            if key == 'skeleton_outline_size':
                #  Отрисовка скелета
                if 'skeleton_tracking' in config and config['skeleton_tracking'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 10:
                        continue

                    curr_valid_layer += 1

            # Отрисовка линий скелета
            if key == 'skeleton_tracking_lines':
                # Проверка значения
                if type(val) is not bool:
                    continue

                # Отрисовка линий скелета необходима
                if val is True:
                    # Добавляем:
                    #     1. Толщина линии соединения скелетных суставов
                    #     2. Цвет линии соединения скелетных суставов
                    all_layer += 2

                curr_valid_layer += 1

            # Толщина линии соединения скелетных суставов
            if key == 'skeleton_lines_width':
                #  Отрисовка линий скелета
                if 'skeleton_tracking_lines' in config and config['skeleton_tracking_lines'] is True:
                    # Проверка значения
                    if type(val) is not int or val < 0 or val > 10:
                        continue

                    curr_valid_layer += 1

            # Цвет линии соединения скелетных суставов
            if key == 'skeleton_lines_color':
                #  Отрисовка линий скелета
                if 'skeleton_tracking_lines' in config and config['skeleton_tracking_lines'] is True:
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
                        # 3. Прозрачность
                        if k == 'red' or k == 'green' or k == 'blue' or k == 'alpha':
                            curr_valid_layer_2 += 1

                    if all_layer_2 == curr_valid_layer_2:
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
    def _load_config_json(self, resources = configs, config = 'kinect2.json', out = True):
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

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._update_config_json(set_window_name) is False:
            return False

        return True

    # Поиск шрифта из ресурсов пакета
    def _search_font(self, out = True):
        """
        Поиск шрифта из ресурсов пакета

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если шрифт найден, в обратном случае False
        """

        # Загрузка и проверка координат для отрисовки скелета
        if self._load_model_skeleton(out = out) is False:
            return False

        # Выполнение функции из суперкласса с отрицательным результатом
        if super()._search_font(out) is False:
            return False

        return True

    # Захват данных из сенсора Kinect 2
    def _grab_data(self, out = True):
        """
        Захват данных из сенсора Kinect 2

        ([bool]) -> bool

        Аргументы:
           out - Печатать процесс выполнения

        Возвращает: True если захват данных из сенсора Kinect 2 произведен, в обратном случае False
        """

        # Запуск Kinect 2
        if self.run_kinect(out) is False:
            return False

        return True

    # Получение цветного кадра из Kinect 2
    def _get_color_frame(self):
        """
        Получение цветного кадра из Kinect 2
        """

        self.get_color_frame()  # Получение цветного кадра из Kinect 2

        # Отображение скелета в окне воспроизведения
        if self._args['show_labels'] is False \
                and (self._args['skeleton_tracking'] is True or self._args['skeleton_tracking_lines'] is True):
            # Формирование прозрачного наложения на текущий кадр кадра
            self._frame_transparent()

    # Получение карты глубины из Kinect 2
    def _get_depth_frame(self, out = True):
        """
        Получение карты глубины из Kinect 2

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если карта глубины получена, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        self.get_depth_frame()  # Получение карты глубины из Kinect 2

        # Карта глубины не получена
        if self._curr_frame_depth is None:
            self._automatic_update['depth_not_received'] = True  # Карта глубины не получена

            # Отображение надписей в терминале
            if self._args['show_labels'] is False:
                if self._automatic_update['invalid_config_file'] is False:
                    # Надпись для терминала
                    self._stdout_write(
                        '[{}{}{}] {}'.format(
                            self.red, datetime.now().strftime(self._format_time), self.end,
                            self._check_depth_not_received
                        ),
                        out = out
                    )
            else:
                # Размеры текста
                (_, height_text), (_, _) = self._font['error'].font.getsize(self._check_depth_not_received)

                self._draw_info(
                    text = self._check_depth_not_received,
                    base_coords = (0, self._curr_frame.shape[0] - height_text - self._args['labels_padding'] * 2),
                    background_color = (self._args['error_background_color']['red'],
                                        self._args['error_background_color']['green'],
                                        self._args['error_background_color']['blue'],
                                        self._args['error_background_color']['alpha']),
                    text_color = (self._args['error_text_color']['red'],
                                  self._args['error_text_color']['green'],
                                  self._args['error_text_color']['blue'],
                                  self._args['error_text_color']['alpha']),
                    stroke = self._args['error_stroke'],
                    stroke_color = (self._args['error_stroke_color']['red'],
                                    self._args['error_stroke_color']['green'],
                                    self._args['error_stroke_color']['blue'],
                                    self._args['error_stroke_color']['alpha']),
                    font = self._font['error'],
                    out = out
                )

            return False
        else:
            self._automatic_update['depth_not_received'] = False  # Карта глубины получена

        # Отображение карты глубины
        if self._args['show_depth'] is True:
            # Изменение размеров изображения карты глубины не стандартные
            if self._args['resize_depth_ir']['width'] != 0:
                # Изменение размера карты глубины
                self._curr_frame_depth = self.resize_frame(
                    self._curr_frame_depth, self._args['resize_depth_ir']['width'], 0
                )

                # Изображение уменьшилось
                if self._curr_frame_depth is not None:
                    # Получение значений во сколько раз масштабировалась карта глубины
                    self._scale_depth['width'] = self._curr_frame_depth[1]
                    self._scale_depth['height'] = self._curr_frame_depth[2]

                    self._curr_frame_depth = self._curr_frame_depth[0]
                else:
                    # Получение значений во сколько раз масштабировалась карта глубины
                    self._scale_depth['width'] = self._scale_depth['height'] = 1.0

            # Правый отступ для карты глубины
            self._right_margin = self._curr_frame.shape[1] - self._curr_frame_depth.shape[1] \
                - self._args['labels_base_coords_depth_ir']['right']

            # Вставка карты глубины в основное изображение
            self._curr_frame[
                self._args['labels_base_coords_depth_ir']['top']:
                    self._args['labels_base_coords_depth_ir']['top'] + self._curr_frame_depth.shape[0],
                self._right_margin: self._right_margin + self._curr_frame_depth.shape[1]] = self._curr_frame_depth

        return True

    # Получение инфракрасного кадра из Kinect 2
    def _get_infrared_frame(self, out = True):
        """
        Получение инфракрасного кадра из Kinect 2

        ([bool]) -> bool

        Аргументы:
            out - Печатать процесс выполнения

        Возвращает: True если инфракрасный кадр получен, в обратном случае False
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Получение инфракрасного кадра из Kinect 2
        self.get_infrared_frame(self._args['norm_infrared'])

        # Инфракрасный кадр не получен
        if self._curr_frame_infrared is None:
            self._automatic_update['inf_not_received'] = True  # Инфракрасный кадр не получен

            # Отображение надписей в терминале
            if self._args['show_labels'] is False:
                if self._automatic_update['invalid_config_file'] is False \
                        and self._automatic_update['depth_not_received'] is False:
                    # Надпись для терминала
                    self._stdout_write(
                        '[{}{}{}] {}'.format(
                            self.red, datetime.now().strftime(self._format_time), self.end, self._check_inf_not_received
                        ),
                        out = out
                    )
            else:
                # Размеры текста
                (_, height_text), (_, _) = self._font['error'].font.getsize(self._check_inf_not_received)

                self._draw_info(
                    text = self._check_inf_not_received,
                    base_coords = (0, self._curr_frame.shape[0] - height_text - self._args['labels_padding'] * 2),
                    background_color = (self._args['error_background_color']['red'],
                                        self._args['error_background_color']['green'],
                                        self._args['error_background_color']['blue'],
                                        self._args['error_background_color']['alpha']),
                    text_color = (self._args['error_text_color']['red'],
                                  self._args['error_text_color']['green'],
                                  self._args['error_text_color']['blue'],
                                  self._args['error_text_color']['alpha']),
                    stroke = self._args['error_stroke'],
                    stroke_color = (self._args['error_stroke_color']['red'],
                                    self._args['error_stroke_color']['green'],
                                    self._args['error_stroke_color']['blue'],
                                    self._args['error_stroke_color']['alpha']),
                    font = self._font['error'],
                    out = out
                )

            return False
        else:
            self._automatic_update['inf_not_received'] = False  # Инфракрасный кадр получен

        # Отображение инфракрасного кадра
        if self._args['show_infrared'] is True:
            # Изменение размеров изображения карты глубины не стандартные
            if self._args['resize_depth_ir']['width'] != 0:
                # Изменение размера карты глубины
                self._curr_frame_infrared = self.resize_frame(
                    self._curr_frame_infrared, self._args['resize_depth_ir']['width'], 0
                )

                # Изображение уменьшилось
                if self._curr_frame_infrared is not None:
                    self._curr_frame_infrared = self._curr_frame_infrared[0]

            # Правый отступ для карты глубины
            right_margin = self._curr_frame.shape[1] - self._curr_frame_infrared.shape[1]\
                - self._args['labels_base_coords_depth_ir']['right']

            # Верхний отступ для инфракрасного кадра
            top_margin = self._args['labels_base_coords_depth_ir']['top']

            # Отображение карты глубины
            if self._args['show_depth'] is True and self._curr_frame_depth is not None:
                top_margin += self._curr_frame_depth.shape[0] + self._args['distance_between_depth_ir']

            # Вставка карты глубины в основное изображение
            self._curr_frame[
                top_margin: top_margin + self._curr_frame_infrared.shape[0],
                right_margin: right_margin + self._curr_frame_infrared.shape[1]] = self._curr_frame_infrared

        return True

    # Получение ориентиров скелета из Kinect 2
    def _get_bodies(self, out = True):
        """
        Получение ориентиров скелета из Kinect 2

        ([bool]) -> None

        Аргументы:
           out - Печатать процесс выполнения
        """

        # Проверка аргументов
        if type(out) is not bool:
            return False

        # Получение ориентиров скелета из Kinect 2
        self.get_bodies(
            show = self._args['skeleton_tracking'],
            show_lines = self._args['skeleton_tracking_lines'],
            point_radius = self._args['skeleton_point_radius'],
            point_background_color = (self._args['skeleton_point_background_color']['red'],
                                      self._args['skeleton_point_background_color']['green'],
                                      self._args['skeleton_point_background_color']['blue'],
                                      self._args['skeleton_point_background_color']['alpha']),
            outline_color = (self._args['skeleton_outline_color']['red'],
                             self._args['skeleton_outline_color']['green'],
                             self._args['skeleton_outline_color']['blue'],
                             self._args['skeleton_outline_color']['alpha']),
            outline_size = self._args['skeleton_outline_size'],
            lines_width = self._args['skeleton_lines_width'],
            lines_color = (self._args['skeleton_lines_color']['red'],
                             self._args['skeleton_lines_color']['green'],
                             self._args['skeleton_lines_color']['blue'],
                             self._args['skeleton_lines_color']['alpha']),
            out = out
        )

        # Отображение надписей в терминале
        if self._args['show_labels'] is False:
            if self._automatic_update['invalid_config_file'] is False\
                    and self._automatic_update['inf_not_received'] is False\
                    and self._automatic_update['depth_not_received'] is False:
                # Надпись для терминала
                self._stdout_write(
                    '[{}] {}, {}'.format(datetime.now().strftime(self._format_time), self._label_fps,
                                         self._people.format(self._cnt_bodies)),
                    out = out)
        else:
            # Координаты нижней левой точки определены (метка FPS)
            if self._fps_point2 is not None:
                # Нанесение информации на изображение
                self._draw_info(
                    text = self._people.format(self._cnt_bodies),
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
                    out = out
                )

    # Операции над кадром
    def _frame_o(self):
        """
        Операции над кадром
        """

        get_depth_frame = self._get_depth_frame()  # Получение карты глубины из Kinect 2

        get_infrared_frame = self._get_infrared_frame()  # Получение инфракрасного кадра из Kinect 2

        # 1. Карта глубины получена
        # 2. Инфракрасный кадр получен
        if get_depth_frame is True and get_infrared_frame is True:
            self._get_bodies()  # Получение ориентиров скелета из Kinect 2

        # Отображение скелета в окне воспроизведения
        if self._args['show_labels'] is False \
                and (self._args['skeleton_tracking'] is True or self._args['skeleton_tracking_lines'] is True):
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

        # Запуск процесса извлечения изображений
        if start is True:
            self.set_loop(self._loop)  # Циклическая функция извлечения изображений
            self.start()  # Запуск


def main():
    run = Run()

    run.run()


if __name__ == "__main__":
    main()