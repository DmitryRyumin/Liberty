# Liberty - компьютерное зрение в реальном времени

![PyPI](https://img.shields.io/pypi/v/liberty)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liberty)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/liberty)
![PyPI - Status](https://img.shields.io/pypi/status/liberty)
![PyPI - License](https://img.shields.io/pypi/l/liberty)

| [История релизов](https://github.com/DmitryRyumin/Liberty/blob/master/README_RU.md) | [Документация на английском](https://github.com/DmitryRyumin/Liberty) |
| --- | --- |

## Установка

```shell script
pip install liberty
```

---

>  **Примечание для Windows!**

1. Удалить `PyOpenGL` и `PyOpenGL-accelerate`

    ```shell script
    pip uninstall PyOpenGL
    pip uninstall PyOpenGL-accelerate
    ```

2. Скачать и установить [PyOpenGL и PyOpenGL-accelerate](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

---

## Обновление

```shell script
pip install --upgrade liberty
```

## Зависимости

| Пакет | Минимальная версия | Текущая версия |
| ----- | ------------------ | -------------- |
`numpy` | `1.18.4` | ![PyPI](https://img.shields.io/pypi/v/numpy) |
`opencv-contrib-python` | `4.2.0.34` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) |
`PyOpenGL` | `3.1.5` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL) |
`PyOpenGL-accelerate` | `3.1.5` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL-accelerate) |
`Pillow` | `7.1.2` | ![PyPI](https://img.shields.io/pypi/v/Pillow) |

## Модули

| Название | Описание | Конфигурационный файл | Примеры |
| -------- | -------- | --------------------- | ------- |
| [trml](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/trml) | Работа с Shell | | |
| [core](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/core) | Ядро модулей | | |
| [filem](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/filem) | Работа с файлами | | |
| [pvv](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/pvv) | Воспроизведение фото/видео данных | [+](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/configs/config.json) | [+](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/samples/play.py) |
