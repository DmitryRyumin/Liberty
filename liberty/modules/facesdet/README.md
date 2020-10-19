# Faces detection

| [Documentation in Russian](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/modules/facesdet/README_RU.md) |
| --- |

## Command line arguments

| Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description | Valid Values |
| -------------------------- | ---  | -------- | ------------------- |
| command | str | Language<br>`Default value: en` | `en`<br>`ru` |
| --file | str | Path to photo/video file or folder with photo files<br>`Default value: 0` | - |
| --config | str | Path to configuration file | - |
| --frames_to_update | int | How many steps to check the configuration file (works with `--automatic_update`)<br>`Default value: 25` | From `0` to `∞` |
| --automatic_update | bool | Automatic verification of the configuration file at the time the program is running (it works with `--config`) | No value |
| --no_clear_shell | bool | Do not clean the console before running | No value |

## [Configuration file](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/configs/pvv.json)

### Parameters

| `Json` parameter | Type | Description | Valid Values |
| ---------------- | ---- | ----------- | ------------ |
| hide_metadata | bool | Hide metadata | - |
| window_name | str | Window name | - |
| method | str | Faces detection method | `opencv_dnn` |
| dnn | str | Neural network type | `tf`<br>`caffe` |
| size | dict | Neural network image size<br>`Recommended: 300×300` | - |
| resize | dict | Window size for resize | From `100` to `1920` |
| switch_text_color | dict | Text color of error notification texts when switching photos | From `0` to `255` |
| switch_size | int | Font size for error notification texts when switching photos | From `1` to `60` |
| switch_stroke | int | Stroke width for error notification texts when switching photos | From `0` to `4` |
| switch_stroke_color | int | Stroke color for error notifications texts when switching photos | From `0` to `255` |
| info_text_color | dict | Text color of information notifications | From `0` to `255` |
| info_background_color | dict | Background color of information notifications | From `0` to `255` |
| info_size | int | Font size for information notification | From `1` to `60` |
| info_stroke | int | Stroke width for information notifications | From `0` to `4` |
| info_stroke_color | int | Stroke color for informational notifications text | From `0` to `255` |
| error_text_color | dict | Text color of error notifications | From `0` to `255` |
| error_background_color | dict | Background color of error notifications | From `0` to `255` |
| error_size | int | Font size for error notifications | From `1` to `60` |
| error_stroke | int | Stroke width for error notifications | From `0` to `4` |
| error_stroke_color | int | Stroke color for error notifications text | From `0` to `255` |
| repeat_text_color | dict | Text color of repeat playing | From `0` to `255` |
| repeat_background_color | dict | Background color of repeat playing | From `0` to `255` |
| repeat_size | int | Font size for repeat playing | From `1` to `120` |
| repeat_stroke | int | Stroke width for repeat playing | From `0` to `4` |
| repeat_stroke_color | int | Stroke color for repeat playing | From `0` to `255` |
| labels_base_coords | int | The start coordinate for the upper left informational notifications | From `0` to `100` |
| labels_padding | int | Padding size for all notification texts | From `0` to `30` |
| labels_distance | int | Text spacing | From `0` to `15` |
| clear_image_buffer | bool | Clear image buffer | - |
| real_time | bool | Playing a photo/video data with a real time of FPS | - |
| repeat | bool | Repeat video stream playback | - |
| fps | int | Custom FPS<br>`"real_time" = true` | From `0` to `60` |
| show_labels | bool | Display labels in the playback window | - |
| face_rectangle | bool | Showing bounding boxes of detected faces | - |
| conf_face_threshold | float | Confidence threshold for faces detection | From `0.0` to `1.0` |
| draw_precent | bool | Percentage show next to each detected face<br>`"face_rectangle" = true` | - |
| face_rectangle_outline_color | dict | Frame color of bounding boxes of detected faces<br>`"face_rectangle" = true` | From `0` to `255` |
| face_rectangle_outline_size | int | Frame thickness of bounding boxes of detected faces<br>`"face_rectangle" = true` | From `1` to `10` |
| face_rectangle_background_color | dict | Background color of bounding boxes of detected faces<br>`"face_rectangle" = true` | From `0` to `255` |
| padding_face | dict | Inner padding of bounding boxes of detected faces<br>`"face_rectangle" = true` | From `1` to `100` |
| face_text_color | dict | Percentage text color for detected faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `255` |
| face_background_color | dict | Percentage background color for detected faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `255` |
| face_size | int | Percentage font size for detected faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `1` to `60` |
| face_stroke | int | Percentage text stroke width for detected faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `4` |
| face_stroke_color | dict | Stroke color of text percentages for detected faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `255` |
| face_padding | int | Inner padding of text percentages<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `30` |
| face_distance | int | Distance between percent and bounding boxes text of found faces<br>`"face_rectangle" = true` and `"draw_precent" = true` | From `0` to `15` |

### Hotkeys

| Keyboard key | Execution |
| ------------ | --------- |
| `esc` | Closing the app window |
| `r` | Repeat video stream playback |
| `> (right arrow)` | Switch to next photo file |
| `> (left arrow)` | Switch to previous photo file |

<h4 align="center"><span style="color:#EC256F;">Examples</span></h4>

---

>  **Note!** Supported Formats

| Video | Photo | Directories |
| ----- | ----- | ----------- |
| `mp4` and `avi` | `png` and `jpg` | With `png` and `jpg` files |

---

1. Faces detection on the video file being played with automatic updating of the configuration file (Language: `Russian`)

    > CMD
    >
    > ```shell script
    > liberty_facesdet ru --file path_to_video_file --config path_to_config_file --automatic_update
    > ```

2. Faces detection on streaming from a WEB-camera with automatic updating of the configuration file every 50 frames (Language: `English`)

    > CMD
    >
    > ```shell script
    > liberty_facesdet en --file 0 --config path_to_config_file --automatic_update --frames_to_update 50
    > ```

3. Faces detection on playable photo files with automatic update of the configuration file (Language: `Russian`)

    > CMD
    >
    > ```shell script
    > liberty_facesdet ru --file path_to_directory_photo_files --config path_to_config_file --automatic_update
    > ```