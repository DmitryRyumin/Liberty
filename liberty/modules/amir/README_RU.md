# Управление ассистивным мобильным информационным роботом посредством автоматического распознавания жестовой информации

| [Документация на английском](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/amir) |
| --- |

---

>  **Примечание!** Требуется операционная система Windows >= 8.0

---

## Аргументы командной строки

| Аргумент&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Тип | Описание | Допустимые значения |
| -------------------------- | ---  | -------- | ------------------- |
| command | str | Язык<br>`Значение по умолчанию: en` | `en`<br>`ru` |
| --config | str | Путь к конфигурационному файлу | - |
| --frames_to_update | int | Через какое количество шагов проверять конфигурационный файл (работает при `--automatic_update`)<br>`Значение по умолчанию: 25` | От `0` до `∞` |
| --automatic_update | bool | Автоматическая проверка конфигурационного файла в момент работы программы (работает при заданном `--config`) | Без значений |
| --no_clear_shell | bool | Не очищать консоль перед выполнением | Без значений |

## [Конфигурационный файл](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/configs/amir.json)

### Параметры

| Параметр `json` | Тип | Описание | Допустимые значения |
| ---------------- | ---  | -------- | ------------------- |
| hide_metadata | bool | Скрытие метаданных | - |
| window_name | str | Имя окна | - |
| resize | dict | Размер окна для масштабирования | От `0` до `∞` |
| info_text_color | dict | Цвет текстов информационных уведомлений | От `0` до `255` |
| info_background_color | dict | Цвет фона информационных уведомлений | От `0` до `255` |
| info_size | int | Размер шрифта информационных уведомлений | От `1` до `60` |
| info_stroke | int | Ширина обводки текста информационных уведомлений | От `0` до `4` |
| info_stroke_color | int | Цвет обводки текста информационных уведомлений | От `0` до `255` |
| error_text_color | dict | Цвет текстов уведомлений об ошибках | От `0` до `255` |
| error_background_color | dict | Цвет фона уведомлений об ошибках | От `0` до `255` |
| error_size | int | Размер шрифта уведомлений об ошибках | От `1` до `60` |
| error_stroke | int | Ширина обводки текста уведомлений об ошибках | От `0` до `4` |
| error_stroke_color | int | Цвет обводки текста уведомлений об ошибках | От `0` до `255` |
| labels_base_coords | int | Начальные координаты верхних левых информационных уведомлений | От `0` до `100` |
| labels_padding | int | Внутренний отступ для всех текстов уведомлений | От `0` до `30` |
| labels_distance | int | Расстояние между текстами | От `0` до `15` |
| show_labels | bool | Отображение надписей в окне воспроизведения | - |
| show_depth | bool | Отображение карты глубины | - |
| show_infrared | bool | Отображение инфракрасного кадра | - |
| resize_depth_ir | dict | Размер карты глубины и инфракрасного кадра для масштабирования<br>`"show_depth" = true` или `"show_infrared" = true` | От `0` до `512` |
| labels_base_coords_depth_ir | dict | Начальные координаты карты глубины и инфракрасного кадра относительно верхнего правого угла<br>`"show_depth" = true` или `"show_infrared" = true` | От `0` до `100` |
| distance_between_depth_ir | int | Расстояние между картой глубины и инфракрасным кадром<br>`"show_depth" = true` и `"show_infrared" = true` | От `0` до `50` |
| norm_infrared | float | Нормализация значений инфракрасной камеры<br>`"show_infrared" = true` | От `0.01` до `1.0` |
| skeleton_tracking | bool | Отображение скелетных суставов | - |
| skeleton_depth_tracking | bool | Отрисовка скелетных суставов на карте глубины<br>`"show_depth" = true` | - |
| skeleton_point_radius | int | Радиус точек скелетных суставов<br>`"skeleton_tracking" = true` | От `1` до `10` |
| skeleton_point_background_color | dict | Цвет фона точек скелетных суставов<br>`"skeleton_tracking" = true` | От `0` до `255` |
| skeleton_outline_color | dict | Цвет обводки фона точек скелетных суставов<br>`"skeleton_tracking" = true` | От `0` до `255` |
| skeleton_outline_size | int | Ширина обводки фона точек скелетных суставов<br>`"skeleton_tracking" = true` | От `0` до `10` |
| skeleton_tracking_lines | bool | Соединение скелетный суставов линиями | - |
| skeleton_lines_width | int | Толщина линии соединения скелетных суставов<br>`"skeleton_tracking_lines" = true` | От `0` до `10` |
| skeleton_lines_color | dict | Цвет линии соединения скелетных суставов<br>`"skeleton_tracking_lines" = true` | От `0` до `255` |
| skeleton_rectangle | bool | Отображение ограничивающего прямоугольника ближайшего найденного скелета | - |
| skeleton_rectangle_outline_color | dict | Цвет рамки ограничивающего прямоугольника ближайшего найденного скелета<br>`"skeleton_rectangle" = true` | От `0` до `255` |
| skeleton_rectangle_outline_size | int | Толщина рамки ограничивающего прямоугольника ближайшего найденного скелета<br>`"skeleton_rectangle" = true` | От `0` до `10` |
| skeleton_rectangle_background_color | dict | Цвет фона ограничивающего прямоугольника ближайшего найденного скелета<br>`"skeleton_rectangle" = true` | От `0` до `255` |
| padding_rectangle | dict | Отступы для ограничивающего прямоугольника ближайщего ближайшего скелета<br>`"skeleton_rectangle" = true` | От `0` до `300` |

### Горячие клавиши

| Клавиши | Сценарий |
| ------- | -------- |
| `esc` | Закрытие окна приложения |

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

---

1. Стриминг с сенсора Kinect 2 с автоматическим обновлением конфигурационного файла (Язык: `Русский`)

    > CMD
    >
    > ```shell script
    > liberty_amir_play ru --config путь_к_конфигурационному_файлу --automatic_update
    > ```

2. Стриминг с сенсора Kinect 2 с автоматическим обновлением конфигурационного файла (Язык: `Английский`)

    > CMD
    >
    > ```shell script
    > liberty_amir_play en --config путь_к_конфигурационному_файлу --automatic_update
    > ```
