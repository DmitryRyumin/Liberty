# Assistive mobile information robot control by automatic gesture recognition

| [Documentation in Russian](https://github.com/DmitryRyumin/Liberty/tree/master/liberty/modules/amir/README_RU.md) |
| --- |

---

>  **Note!** Requires Windows operating system >= 8.0

---

## Command line arguments

| Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description | Valid Values |
| -------------------------- | ---  | -------- | ------------------- |
| command | str | Language<br>`Default value: en` | `en`<br>`ru` |
| --config | str | Path to configuration file | - |
| --frames_to_update | int | How many steps to check the configuration file (works with `--automatic_update`)<br>`Default value: 25` | From `0` to `∞` |
| --automatic_update | bool | Automatic verification of the configuration file at the time the program is running (it works with `--config`) | No value |
| --no_clear_shell | bool | Do not clean the console before running | No value |

## [Configuration file](https://github.com/DmitryRyumin/Liberty/blob/master/liberty/configs/amir.json)

### Parameters

| `Json` parameter | Type | Description | Valid Values |
| ---------------- | ---- | ----------- | ------------ |
| hide_metadata | bool | Hide metadata | - |
| window_name | str | Window name | - |
| resize | dict | Window size for resize | From `0` to `∞` |
| info_text_color | dict | Text color of information notifications | From `0` to `255` |
| info_background_color | dict | Background color of information notifications | From `0` to `255` |
| info_size | int | Font size for information notification | From `1` to `60` |
| info_stroke | int | Stroke width for information notifications | From `0` to `4` |
| info_stroke_color | int | Stroke color for informational notifications text | From `0` to `255` |
| error_text_color | dict | Text color of error notifications | From `0` to `255` |
| error_background_color | dict | Background color of error notifications | From `0` to `255` |
| error_size | int | Font size for error notification | From `1` to `60` |
| error_stroke | int | Stroke width for error notifications | From `0` to `4` |
| error_stroke_color | int | Stroke color for error notifications text | From `0` to `255` |
| labels_base_coords | int | The start coordinate for the upper left informational notifications | From `0` to `100` |
| labels_padding | int | Padding size for all notification texts | From `0` to `30` |
| labels_distance | int | Text spacing | From `0` to `15` |
| show_labels | bool | Display labels in the playback window | - |
| show_depth | bool | Display depth map | - |
| show_infrared | bool | Display infrared | - |
| resize_depth_ir | dict | Depth map and infrared frame size<br>`"show_depth" = true` or `"show_infrared" = true` | From `0` to `512` |
| labels_base_coords_depth_ir | dict | The base coordinates of the depth map and infrared relative to the upper right corner<br>`"show_depth" = true` or `"show_infrared" = true` | From `0` to `100` |
| distance_between_depth_ir | int | Distance between depth map and infrared<br>`"show_depth" = true` and `"show_infrared" = true` | From `0` to `50` |
| norm_infrared | float | Normalizing infrared values<br>`"show_infrared" = true` | From `0.01` to `1.0` |
| skeleton_tracking | bool | Drawing skeletal joints | - |
| skeleton_depth_tracking | bool | Drawing skeletal joints on a depth map<br>`"show_depth" = true` | - |
| skeleton_point_radius | int | The radius of the points of the skeletal joints<br>`"skeleton_tracking" = true` | From `1` to `10` |
| skeleton_point_background_color | dict | Skeletal points background color<br>`"skeleton_tracking" = true` | From `0` to `255` |
| skeleton_outline_color | dict | Skeletal outline background stroke color<br>`"skeleton_tracking" = true` | From `0` to `255` |
| skeleton_outline_size | int | Skeletal outline background stroke width<br>`"skeleton_tracking" = true` | From `0` to `10` |
| skeleton_tracking_lines | bool | Joint skeletal joints with lines | - |
| skeleton_lines_width | int | Skeletal joint line thickness<br>`"skeleton_tracking_lines" = true` | From `0` to `10` |
| skeleton_lines_color | dict | Skeletal joint line color<br>`"skeleton_tracking_lines" = true` | From `0` to `255` |
| skeleton_rectangle | bool | Drawing the bounding box of the closest found skeleton | - |
| skeleton_rectangle_outline_color | dict | The color of the bounding box border of the closest found skeleton<br>`"skeleton_rectangle" = true` | From `0` to `255` |
| skeleton_rectangle_outline_size | int | The thickness of the bounding box of the nearest found skeleton<br>`"skeleton_rectangle" = true` | From `0` to `10` |
| skeleton_rectangle_background_color | dict | The background color of the bounding box of the closest found skeleton<br>`"skeleton_rectangle" = true` | From `0` to `255` |
| padding_rectangle | dict | Bounding rectangle margins of the nearest found skeleton<br>`"skeleton_rectangle" = true` | From `0` to `300` |

### Hotkeys

| Keyboard key | Execution |
| ------------ | --------- |
| `esc` | Closing the app window |

<h4 align="center"><span style="color:#EC256F;">Examples</span></h4>

---

1. Streaming from a Kinect 2 sensor with automatic update of the configuration file (Language: `Russian`)

    > CMD
    >
    > ```shell script
    > liberty_amir_play ru --config path_to_config_file --automatic_update
    > ```

2. Streaming from a Kinect 2 sensor with automatic update of the configuration file (Language: `English`)

    > CMD
    >
    > ```shell script
    > liberty_amir_play en --config path_to_config_file --automatic_update
    > ```
