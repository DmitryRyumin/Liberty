# Liberty - Real-time computer vision

![PyPI](https://img.shields.io/pypi/v/liberty)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liberty)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/liberty)
![PyPI - Status](https://img.shields.io/pypi/status/liberty)
![PyPI - License](https://img.shields.io/pypi/l/liberty)

| [Release history](https://github.com/DmitryRyumin/Liberty/blob/master/NOTES.md) | [Documentation in Russian](https://github.com/DmitryRyumin/Liberty/blob/master/README_RU.md) |
| --- | --- |

## Installation

```shell script
pip install liberty
```

---

>  **Note for Windows!**

1. Delete `PyOpenGL` and  `PyOpenGL-accelerate`

    ```shell script
    pip uninstall PyOpenGL
    pip uninstall PyOpenGL-accelerate
    ```

2. Download and installing [PyOpenGL и PyOpenGL-accelerate](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

---

## Update

```shell script
pip install --upgrade liberty
```

## Required packages

| Package | Min version | Current version |
| ------- | ----------- | --------------- |
`numpy` | `1.18.4` | ![PyPI](https://img.shields.io/pypi/v/numpy) |
`opencv-contrib-python` | `4.2.0.34` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) |
`PyOpenGL` | `3.1.5` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL) |
`PyOpenGL-accelerate` | `3.1.5` | ![PyPI](https://img.shields.io/pypi/v/PyOpenGL-accelerate) |
`Pillow` | `7.1.2` | ![PyPI](https://img.shields.io/pypi/v/Pillow) |

## Modules

| Title | Description | Config file | Examples |
| ----- | ----------- | ----------- | -------- |
| [trml](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/trml) | Operation with Shell | | |
| [core](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/core) | Module core | | |
| [filem](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/filem) | Operation with Files | | |
| [pvv](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/pvv) | Playing photo/video data | [+](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/configs/config.json) | [+](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/samples/play.py) |