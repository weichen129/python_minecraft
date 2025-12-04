"""
File: minecraft_character.py
Name: Your Name
----------------------
TODO: Create a Minecraft-style character with 3D cube and facial features,
      plus interactive brick cube generator with mouse clicks
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GRect, GPolygon, GLabel, GLine
from campy.gui.events.mouse import onmouseclicked
import random

# 全域變數
window = GWindow(width=800, height=600, title="Minecraft Character & Brick Generator")
brick_cubes = []  # 儲存所有生成的磚塊立方體


def main():
    # 设置背景颜色
    background = GRect(800, 600, x=0, y=0)
    background.filled = True
    background.fill_color = (240, 240, 240)
    window.add(background)

    # Steve 的比例
    head_size = 100
    body_width = 90
    body_height = 120
    arm_width = 35
    arm_height = 120
    leg_width = 40
    leg_height = 120

    center_x = window.width // 2
    center_y = window.height // 2 + 80

    # 按照從下到上的順序繪製，確保層次正確
    # 1. 右腳 (最底層)
    draw_cube_leg(window, center_x + 5, center_y - 20, leg_width, leg_height, is_left=False)

    # 2. 左腳
    draw_cube_leg(window, center_x - leg_width - 5, center_y - 20, leg_width, leg_height, is_left=True)

    # 3. 右手
    draw_cube_arm(window, center_x + body_width // 2 - 5, center_y - 140, arm_width, arm_height, is_left=False)

    # 4. 身體
    draw_cube_body(window, center_x - body_width // 2, center_y - 140, body_width, body_height)

    # 5. 左手
    draw_cube_arm(window, center_x - body_width // 2 - arm_width + 5, center_y - 140, arm_width, arm_height, is_left=True)

    # 6. 頭 (最上層)
    draw_cube(window, center_x - head_size // 2-5, center_y - 240, head_size)

    # 添加標題
    title = GLabel("Minecraft Character & Brick Generator")
    title.font = "Arial-24"
    title.color = (0, 0, 0)
    title.x = (window.width - title.width) / 2
    title.y = 50
    window.add(title)

    # 添加說明
    instruction = GLabel("HI,I am Steve, just a simple minecraft character, from student's simple homework")
    instruction.font = "Arial-14"
    instruction.color = (100, 100, 100)
    instruction.x = 30
    instruction.y = 80
    window.add(instruction)

    instruction2 = GLabel("I love building something, just like coder and bee. Click anywhere to create brick cubes!")
    instruction2.font = "Arial-14"
    instruction2.color = (100, 100, 100)
    instruction2.x = 30
    instruction2.y = 100
    window.add(instruction2)

    # 註冊滑鼠點擊事件
    onmouseclicked(create_brick_cube)


def create_brick_cube(event):
    # 隨機大小 (50-120)
    size = random.randint(50, 120)

    # 滑鼠點擊位置作為立方體中心
    x = event.x - size // 2
    y = event.y - size // 2

    # 確保不會超出視窗邊界
    if x < 0:
        x = 10
    if y < 0:
        y = 10
    if x + size > window.width:
        x = window.width - size - 10
    if y + size > window.height:
        y = window.height - size - 10

    # 繪製磚塊立方體
    draw_brick_cube(window, x, y, size)

    # 儲立方體資訊
    brick_cubes.append((x, y, size))


def draw_brick_cube(window, x, y, size):
    # 立方體的深度（透視效果）
    depth = size // 3

    # 顏色定義 - 不同面使用不同亮度
    front_brick_color = (157, 78, 58)      # 正面紅褐色磚塊
    top_brick_color = (180, 100, 80)       # 頂面更亮的紅褐色磚塊
    side_brick_color = (130, 60, 40)       # 側面更暗的紅褐色磚塊

    front_mortar_color = (180, 180, 180)   # 正面灰色灰漿
    top_mortar_color = (200, 200, 200)     # 頂面更亮的灰色灰漿
    side_mortar_color = (150, 150, 150)    # 側面更暗的灰色灰漿

    border_color = (180, 180, 180)         # 邊框顏色

    # 繪製立方體的正面磚塊
    draw_brick_face(window, x + depth, y, size, size, front_brick_color, front_mortar_color)

    # 繪製立方體的頂面磚塊
    draw_brick_top(window, x, y, size, depth, top_brick_color, top_mortar_color)

    # 繪製立方體的側面磚塊
    draw_brick_side(window, x, y, size, depth, side_brick_color, side_mortar_color)

    # 添加立方體的邊框線，增強立體感
    # 使用多條線段來模擬更粗的邊框
    border_width = 2  # 邊框寬度

    # 正面邊框 - 使用多個矩形來模擬粗邊框
    for i in range(border_width):
        front_border = GRect(size - 2*i, size - 2*i, x=x + depth + i, y=y + i)
        front_border.filled = False
        front_border.color = border_color
        window.add(front_border)

    # 頂面邊框 - 使用多個多邊形來模擬粗邊框
    for i in range(border_width):
        top_border = GPolygon()
        top_border.add_vertex((x + depth + i, y + i))
        top_border.add_vertex((x + i, y - depth + i))
        top_border.add_vertex((x + size - i, y - depth + i))
        top_border.add_vertex((x + size + depth - i, y + i))
        top_border.filled = False
        top_border.color = border_color
        window.add(top_border)

    # 側面邊框 - 使用多個多邊形來模擬粗邊框
    for i in range(border_width):
        side_border = GPolygon()
        side_border.add_vertex((x + i, y - depth + i))
        side_border.add_vertex((x + i, y - depth + size - i))
        side_border.add_vertex((x + depth - i, y + size - i))
        side_border.add_vertex((x + depth - i, y + i))
        side_border.filled = False
        side_border.color = border_color
        window.add(side_border)


def draw_brick_face(window, x, y, width, height, brick_color, mortar_color):
    # 先繪製灰色灰漿背景
    background = GRect(width, height, x=x, y=y)
    background.filled = True
    background.fill_color = mortar_color
    window.add(background)

    # 磚塊排列模式
    # 每排有兩種模式：完整兩個磚頭 或 半個+一個+半個
    patterns = [
        "full",    # 第一排：完整兩個磚頭
        "half",    # 第二排：半個+一個+半個
        "full",    # 第三排：完整兩個磚頭
        "half"     # 第四排：半個+一個+半個
    ]

    # 每排的高度
    row_height = height // 4

    for row in range(4):
        pattern = patterns[row]
        row_y = y + row * row_height

        if pattern == "full":
            # 完整兩個磚頭
            brick_width = width // 2

            # 左磚塊
            left_brick = GRect(brick_width, row_height, x=x, y=row_y)
            left_brick.filled = True
            left_brick.fill_color = brick_color
            window.add(left_brick)

            # 右磚塊
            right_brick = GRect(brick_width, row_height, x=x + brick_width, y=row_y)
            right_brick.filled = True
            right_brick.fill_color = brick_color
            window.add(right_brick)

        else:  # half pattern
            # 半個+一個+半個
            quarter_width = width // 4
            half_width = width // 2

            # 左半磚塊
            left_brick = GRect(quarter_width, row_height, x=x, y=row_y)
            left_brick.filled = True
            left_brick.fill_color = brick_color
            window.add(left_brick)

            # 中間完整磚塊
            middle_brick = GRect(half_width, row_height, x=x + quarter_width, y=row_y)
            middle_brick.filled = True
            middle_brick.fill_color = brick_color
            window.add(middle_brick)

            # 右半磚塊
            right_brick = GRect(quarter_width, row_height, x=x + quarter_width + half_width, y=row_y)
            right_brick.filled = True
            right_brick.fill_color = brick_color
            window.add(right_brick)

    # 添加磚塊之間的分隔線 - 使用灰色線條
    line_color = mortar_color
    line_width = 1  # 線條寬度

    # 水平分隔線 - 使用多條線段來模擬粗線
    for i in range(1, 4):
        line_y = y + i * row_height
        for offset in range(line_width):
            line = GLine(x, line_y + offset, x + width, line_y + offset)
            line.color = line_color
            window.add(line)

    # 垂直分隔線 - 根據不同模式
    for row in range(4):
        pattern = patterns[row]
        row_y = y + row * row_height

        if pattern == "full":
            # 在兩個磚塊之間添加垂直線
            line_x = x + width // 2
            for offset in range(line_width):
                line = GLine(line_x + offset, row_y, line_x + offset, row_y + row_height)
                line.color = line_color
                window.add(line)
        else:  # half pattern
            # 在半磚塊和完整磚塊之間添加垂直線
            line1_x = x + width // 4
            line2_x = x + 3 * width // 4
            for offset in range(line_width):
                line1 = GLine(line1_x + offset, row_y, line1_x + offset, row_y + row_height)
                line1.color = line_color
                window.add(line1)
                line2 = GLine(line2_x + offset, row_y, line2_x + offset, row_y + row_height)
                line2.color = line_color
                window.add(line2)


def draw_brick_top(window, x, y, size, depth, brick_color, mortar_color):
    # 頂面多邊形的四個頂點
    top_points = [
        (x + depth, y),           # 右下
        (x, y - depth),           # 左上
        (x + size, y - depth),    # 右上
        (x + size + depth, y)     # 左下
    ]

    # 先繪製灰色灰漿背景
    top_background = GPolygon()
    for point in top_points:
        top_background.add_vertex(point)
    top_background.filled = True
    top_background.fill_color = mortar_color
    window.add(top_background)

    # 磚塊排列模式（與正面對應）
    patterns = [
        "full",    # 第一排
        "half",    # 第二排
        "full",    # 第三排
        "half"     # 第四排
    ]

    # 在頂面上繪製磚塊
    for row in range(4):
        pattern = patterns[row]

        # 計算頂面磚塊的位置（使用參數化座標）
        for brick in range(2 if pattern == "full" else 3):
            # 計算磚塊在頂面上的四個頂點
            brick_points = []

            # 計算磚塊在參數空間中的位置
            if pattern == "full":
                u_start = brick / 2
                u_end = (brick + 1) / 2
            else:  # half pattern
                if brick == 0:  # 左半磚塊
                    u_start = 0
                    u_end = 0.25
                elif brick == 1:  # 中間完整磚塊
                    u_start = 0.25
                    u_end = 0.75
                else:  # 右半磚塊
                    u_start = 0.75
                    u_end = 1.0

            v_start = row / 4
            v_end = (row + 1) / 4

            # 計算四個頂點
            for u, v in [(u_start, v_start), (u_end, v_start), (u_end, v_end), (u_start, v_end)]:
                # 使用雙線性插值計算頂面座標
                point_x = (1-u)*(1-v)*top_points[1][0] + u*(1-v)*top_points[2][0] + u*v*top_points[3][0] + (1-u)*v*top_points[0][0]
                point_y = (1-u)*(1-v)*top_points[1][1] + u*(1-v)*top_points[2][1] + u*v*top_points[3][1] + (1-u)*v*top_points[0][1]
                brick_points.append((point_x, point_y))

            # 繪製磚塊
            brick_poly = GPolygon()
            for point in brick_points:
                brick_poly.add_vertex(point)
            brick_poly.filled = True
            brick_poly.fill_color = brick_color
            window.add(brick_poly)

    # 添加頂面磚塊之間的分隔線 - 使用灰色線條
    line_color = mortar_color
    line_width = 1  # 線條寬度

    # 水平分隔線
    for row in range(1, 4):
        v = row / 4
        for offset in range(line_width):
            line_points = []
            for u in [0, 1]:
                point_x = (1-u)*(1-v)*top_points[1][0] + u*(1-v)*top_points[2][0] + u*v*top_points[3][0] + (1-u)*v*top_points[0][0]
                point_y = (1-u)*(1-v)*top_points[1][1] + u*(1-v)*top_points[2][1] + u*v*top_points[3][1] + (1-u)*v*top_points[0][1]
                line_points.append((point_x, point_y))

            # 稍微偏移線條位置以模擬粗線
            offset_factor = offset * 0.5
            line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                         line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
            line.color = line_color
            window.add(line)

    # 垂直分隔線 - 根據不同模式
    for row in range(4):
        pattern = patterns[row]
        v_start = row / 4
        v_end = (row + 1) / 4

        if pattern == "full":
            # 在兩個磚塊之間添加垂直線
            u = 0.5
            for offset in range(line_width):
                line_points = []
                for v in [v_start, v_end]:
                    point_x = (1-u)*(1-v)*top_points[1][0] + u*(1-v)*top_points[2][0] + u*v*top_points[3][0] + (1-u)*v*top_points[0][0]
                    point_y = (1-u)*(1-v)*top_points[1][1] + u*(1-v)*top_points[2][1] + u*v*top_points[3][1] + (1-u)*v*top_points[0][1]
                    line_points.append((point_x, point_y))

                # 稍微偏移線條位置以模擬粗線
                offset_factor = offset * 0.5
                line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                             line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
                line.color = line_color
                window.add(line)
        else:  # half pattern
            # 在半磚塊和完整磚塊之間添加垂直線
            for u in [0.25, 0.75]:
                for offset in range(line_width):
                    line_points = []
                    for v in [v_start, v_end]:
                        point_x = (1-u)*(1-v)*top_points[1][0] + u*(1-v)*top_points[2][0] + u*v*top_points[3][0] + (1-u)*v*top_points[0][0]
                        point_y = (1-u)*(1-v)*top_points[1][1] + u*(1-v)*top_points[2][1] + u*v*top_points[3][1] + (1-u)*v*top_points[0][1]
                        line_points.append((point_x, point_y))

                    # 稍微偏移線條位置以模擬粗線
                    offset_factor = offset * 0.5
                    line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                                 line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
                    line.color = line_color
                    window.add(line)


def draw_brick_side(window, x, y, size, depth, brick_color, mortar_color):
    # 側面多邊形的四個頂點
    side_points = [
        (x, y - depth),           # 左上
        (x, y - depth + size),    # 左下
        (x + depth, y + size),    # 右下
        (x + depth, y)            # 右上
    ]

    # 先繪製灰色灰漿背景
    side_background = GPolygon()
    for point in side_points:
        side_background.add_vertex(point)
    side_background.filled = True
    side_background.fill_color = mortar_color
    window.add(side_background)

    # 磚塊排列模式（與正面對應）
    patterns = [
        "full",    # 第一排
        "half",    # 第二排
        "full",    # 第三排
        "half"     # 第四排
    ]

    # 在側面上繪製磚塊
    for row in range(4):
        pattern = patterns[row]

        # 計算側面磚塊的位置（使用參數化座標）
        for brick in range(2 if pattern == "full" else 3):
            # 計算磚塊在側面上的四個頂點
            brick_points = []

            # 計算磚塊在參數空間中的位置
            if pattern == "full":
                u_start = brick / 2
                u_end = (brick + 1) / 2
            else:  # half pattern
                if brick == 0:  # 左半磚塊
                    u_start = 0
                    u_end = 0.25
                elif brick == 1:  # 中間完整磚塊
                    u_start = 0.25
                    u_end = 0.75
                else:  # 右半磚塊
                    u_start = 0.75
                    u_end = 1.0

            v_start = row / 4
            v_end = (row + 1) / 4

            # 計算四個頂點
            for u, v in [(u_start, v_start), (u_end, v_start), (u_end, v_end), (u_start, v_end)]:
                # 使用雙線性插值計算側面座標
                point_x = (1-u)*(1-v)*side_points[0][0] + u*(1-v)*side_points[3][0] + u*v*side_points[2][0] + (1-u)*v*side_points[1][0]
                point_y = (1-u)*(1-v)*side_points[0][1] + u*(1-v)*side_points[3][1] + u*v*side_points[2][1] + (1-u)*v*side_points[1][1]
                brick_points.append((point_x, point_y))

            # 繪製磚塊
            brick_poly = GPolygon()
            for point in brick_points:
                brick_poly.add_vertex(point)
            brick_poly.filled = True
            brick_poly.fill_color = brick_color
            window.add(brick_poly)

    # 添加側面磚塊之間的分隔線 - 使用灰色線條
    line_color = mortar_color
    line_width = 1  # 線條寬度

    # 水平分隔線
    for row in range(1, 4):
        v = row / 4
        for offset in range(line_width):
            line_points = []
            for u in [0, 1]:
                point_x = (1-u)*(1-v)*side_points[0][0] + u*(1-v)*side_points[3][0] + u*v*side_points[2][0] + (1-u)*v*side_points[1][0]
                point_y = (1-u)*(1-v)*side_points[0][1] + u*(1-v)*side_points[3][1] + u*v*side_points[2][1] + (1-u)*v*side_points[1][1]
                line_points.append((point_x, point_y))

            # 稍微偏移線條位置以模擬粗線
            offset_factor = offset * 0.5
            line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                         line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
            line.color = line_color
            window.add(line)

    # 垂直分隔線 - 根據不同模式
    for row in range(4):
        pattern = patterns[row]
        v_start = row / 4
        v_end = (row + 1) / 4

        if pattern == "full":
            # 在兩個磚塊之間添加垂直線
            u = 0.5
            for offset in range(line_width):
                line_points = []
                for v in [v_start, v_end]:
                    point_x = (1-u)*(1-v)*side_points[0][0] + u*(1-v)*side_points[3][0] + u*v*side_points[2][0] + (1-u)*v*side_points[1][0]
                    point_y = (1-u)*(1-v)*side_points[0][1] + u*(1-v)*side_points[3][1] + u*v*side_points[2][1] + (1-u)*v*side_points[1][1]
                    line_points.append((point_x, point_y))

                # 稍微偏移線條位置以模擬粗線
                offset_factor = offset * 0.5
                line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                             line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
                line.color = line_color
                window.add(line)
        else:  # half pattern
            # 在半磚塊和完整磚塊之間添加垂直線
            for u in [0.25, 0.75]:
                for offset in range(line_width):
                    line_points = []
                    for v in [v_start, v_end]:
                        point_x = (1-u)*(1-v)*side_points[0][0] + u*(1-v)*side_points[3][0] + u*v*side_points[2][0] + (1-u)*v*side_points[1][0]
                        point_y = (1-u)*(1-v)*side_points[0][1] + u*(1-v)*side_points[3][1] + u*v*side_points[2][1] + (1-u)*v*side_points[1][1]
                        line_points.append((point_x, point_y))

                    # 稍微偏移線條位置以模擬粗線
                    offset_factor = offset * 0.5
                    line = GLine(line_points[0][0] + offset_factor, line_points[0][1] + offset_factor,
                                 line_points[1][0] + offset_factor, line_points[1][1] + offset_factor)
                    line.color = line_color
                    window.add(line)


def draw_cube(window, x, y, size):
    # 立方體的深度（透視效果）
    depth = size // 3

    # 繪製立方體的正面
    front = GRect(size, size, x=x + depth, y=y)
    front.filled = True
    # 偏粉膚色調
    front.fill_color = (209, 164, 126)  # #D1A47E
    front.color = (80, 120, 200)
    window.add(front)
    draw_face(window, x + depth, y, size)

    # 繪製立方體的頂面 - 完全用頭髮填滿
    top_points = GPolygon()
    top_points.add_vertex((x + depth, y))  # 右上
    top_points.add_vertex((x, y - depth))  # 左上
    top_points.add_vertex((x + size, y - depth))  # 左中
    top_points.add_vertex((x + size + depth, y))  # 左下
    top_points.filled = True
    top_points.fill_color = (111, 78, 55)  # 頭髮顏色
    top_points.color = (100, 140, 220)
    window.add(top_points)

    # 繪製立方體的側面
    side_points = GPolygon()
    side_points.add_vertex((x, y - depth))  # 左上
    side_points.add_vertex((x, y - depth + size))  # 左下
    side_points.add_vertex((x + depth, y + size))  # 右下
    side_points.add_vertex((x + depth, y))  # 右上
    side_points.filled = True
    side_points.fill_color = (198, 140, 109)  # #C68C6D 較暗面
    side_points.color = (60, 110, 180)
    window.add(side_points)

    # 在側面繪製頭髮 - 使用像素方塊方式
    draw_side_hair_pixels(window, x, y, size, depth)

    # 添加立方體的邊框線，增強立體感
    # 正面邊框
    front_border = GRect(size, size, x=x + depth, y=y)
    front_border.filled = False
    front_border.color = (60, 100, 180)
    window.add(front_border)

    # 頂面邊框
    top_border = GPolygon()
    top_border.add_vertex((x + depth, y))
    top_border.add_vertex((x, y - depth))
    top_border.add_vertex((x + size, y - depth))
    top_border.add_vertex((x + size + depth, y))
    top_border.filled = False
    top_border.color = (60, 100, 180)
    window.add(top_border)

    # 側面邊框
    side_border = GPolygon()
    side_border.add_vertex((x, y - depth))
    side_border.add_vertex((x, y - depth + size))
    side_border.add_vertex((x + depth, y + size))
    side_border.add_vertex((x + depth, y))
    side_border.filled = False
    side_border.color = (60, 100, 180)
    window.add(side_border)


def draw_cube_body(window, x, y, width, height):
    # 身體的深度（透視效果）
    depth = width // 3

    # 身體顏色 - 青色系列
    front_color = (0, 170, 170)   # 基礎青色
    top_color = (0, 190, 190)     # 較亮的青色
    side_color = (0, 140, 140)    # 較暗的青色
    border_color = (0, 100, 100)  # 邊框顏色

    # 繪製身體的正面
    front = GRect(width, height, x=x + depth, y=y)
    front.filled = True
    front.fill_color = front_color
    front.color = border_color
    window.add(front)

    # 繪製身體的頂面
    top_points = GPolygon()
    top_points.add_vertex((x + depth, y))  # 右上
    top_points.add_vertex((x, y - depth))  # 左上
    top_points.add_vertex((x + width, y - depth))  # 左中
    top_points.add_vertex((x + width + depth, y))  # 左下
    top_points.filled = True
    top_points.fill_color = top_color
    top_points.color = border_color
    window.add(top_points)

    # 繪製身體的側面
    side_points = GPolygon()
    side_points.add_vertex((x, y - depth))  # 左上
    side_points.add_vertex((x, y - depth + height))  # 左下
    side_points.add_vertex((x + depth, y + height))  # 右下
    side_points.add_vertex((x + depth, y))  # 右上
    side_points.filled = True
    side_points.fill_color = side_color
    side_points.color = border_color
    window.add(side_points)

    # 添加身體的邊框線，增強立體感
    # 正面邊框
    front_border = GRect(width, height, x=x + depth, y=y)
    front_border.filled = False
    front_border.color = border_color
    window.add(front_border)

    # 頂面邊框
    top_border = GPolygon()
    top_border.add_vertex((x + depth, y))
    top_border.add_vertex((x, y - depth))
    top_border.add_vertex((x + width, y - depth))
    top_border.add_vertex((x + width + depth, y))
    top_border.filled = False
    top_border.color = border_color
    window.add(top_border)

    # 側面邊框
    side_border = GPolygon()
    side_border.add_vertex((x, y - depth))
    side_border.add_vertex((x, y - depth + height))
    side_border.add_vertex((x + depth, y + height))
    side_border.add_vertex((x + depth, y))
    side_border.filled = False
    side_border.color = border_color
    window.add(side_border)


def draw_cube_arm(window, x, y, width, height, is_left=True):
    # 手臂的深度（透視效果）
    depth = width // 3

    # 手臂顏色 - 皮膚色系列
    skin_front_color = (205, 158, 122)  # 基礎皮膚色
    skin_top_color = (220, 173, 137)    # 較亮的皮膚色
    skin_side_color = (180, 130, 100)   # 較暗的皮膚色

    # 袖子顏色 - 青色系列（與身體相同）
    sleeve_front_color = (0, 170, 170)   # 基礎青色
    sleeve_top_color = (0, 190, 190)     # 較亮的青色
    sleeve_side_color = (0, 140, 140)    # 較暗的青色

    border_color = (60, 100, 180)  # 邊框顏色

    # 手臂分段 - 上半段是袖子，下半段是皮膚
    sleeve_height = height // 3

    # 繪製袖子部分（上半段）
    # 袖子正面
    sleeve_front = GRect(width, sleeve_height, x=x + depth, y=y)
    sleeve_front.filled = True
    sleeve_front.fill_color = sleeve_front_color
    sleeve_front.color = border_color
    window.add(sleeve_front)

    # 袖子頂面
    sleeve_top_points = GPolygon()
    sleeve_top_points.add_vertex((x + depth, y))  # 右上
    sleeve_top_points.add_vertex((x, y - depth))  # 左上
    sleeve_top_points.add_vertex((x + width, y - depth))  # 左中
    sleeve_top_points.add_vertex((x + width + depth, y))  # 左下
    sleeve_top_points.filled = True
    sleeve_top_points.fill_color = sleeve_top_color
    sleeve_top_points.color = border_color
    window.add(sleeve_top_points)

    # 袖子側面
    sleeve_side_points = GPolygon()
    sleeve_side_points.add_vertex((x, y - depth))  # 左上
    sleeve_side_points.add_vertex((x, y - depth + sleeve_height))  # 左下
    sleeve_side_points.add_vertex((x + depth, y + sleeve_height))  # 右下
    sleeve_side_points.add_vertex((x + depth, y))  # 右上
    sleeve_side_points.filled = True
    sleeve_side_points.fill_color = sleeve_side_color
    sleeve_side_points.color = border_color
    window.add(sleeve_side_points)

    # 繪製皮膚部分（下半段）
    skin_y = y + sleeve_height

    # 皮膚正面
    skin_front = GRect(width, height - sleeve_height, x=x + depth, y=skin_y)
    skin_front.filled = True
    skin_front.fill_color = skin_front_color
    skin_front.color = border_color
    window.add(skin_front)

    # 皮膚側面
    skin_side_points = GPolygon()
    skin_side_points.add_vertex((x, skin_y - depth))  # 左上
    skin_side_points.add_vertex((x, skin_y - depth + (height - sleeve_height)))  # 左下
    skin_side_points.add_vertex((x + depth, skin_y + (height - sleeve_height)))  # 右下
    skin_side_points.add_vertex((x + depth, skin_y))  # 右上
    skin_side_points.filled = True
    skin_side_points.fill_color = skin_side_color
    skin_side_points.color = border_color
    window.add(skin_side_points)

    # 添加手臂的邊框線，增強立體感
    # 袖子正面邊框
    sleeve_front_border = GRect(width, sleeve_height, x=x + depth, y=y)
    sleeve_front_border.filled = False
    sleeve_front_border.color = border_color
    window.add(sleeve_front_border)

    # 皮膚正面邊框
    skin_front_border = GRect(width, height - sleeve_height, x=x + depth, y=skin_y)
    skin_front_border.filled = False
    skin_front_border.color = border_color
    window.add(skin_front_border)

    # 頂面邊框
    top_border = GPolygon()
    top_border.add_vertex((x + depth, y))
    top_border.add_vertex((x, y - depth))
    top_border.add_vertex((x + width, y - depth))
    top_border.add_vertex((x + width + depth, y))
    top_border.filled = False
    top_border.color = border_color
    window.add(top_border)

    # 側面邊框
    side_border = GPolygon()
    side_border.add_vertex((x, y - depth))
    side_border.add_vertex((x, y - depth + height))
    side_border.add_vertex((x + depth, y + height))
    side_border.add_vertex((x + depth, y))
    side_border.filled = False
    side_border.color = border_color
    window.add(side_border)


def draw_cube_leg(window, x, y, width, height, is_left=True):
    # 腿的深度（透視效果）
    depth = width // 3

    # 褲子顏色 - 藍色系列
    pants_front_color = (60, 90, 180)   # 基礎藍色
    pants_top_color = (80, 110, 200)    # 較亮的藍色
    pants_side_color = (40, 70, 140)    # 較暗的藍色

    # 鞋子顏色 - 灰色系列
    shoe_front_color = (150, 150, 150)  # 基礎灰色
    shoe_top_color = (170, 170, 170)    # 較亮的灰色
    shoe_side_color = (120, 120, 120)   # 較暗的灰色

    border_color = (60, 100, 180)  # 邊框顏色

    # 腿分段 - 上半段是褲子，下半段是鞋子
    shoe_height = height // 4

    # 繪製褲子部分（上半段）
    pants_height = height - shoe_height

    # 褲子正面
    pants_front = GRect(width, pants_height, x=x + depth, y=y)
    pants_front.filled = True
    pants_front.fill_color = pants_front_color
    pants_front.color = border_color
    window.add(pants_front)

    # 褲子頂面
    pants_top_points = GPolygon()
    pants_top_points.add_vertex((x + depth, y))  # 右上
    pants_top_points.add_vertex((x, y - depth))  # 左上
    pants_top_points.add_vertex((x + width, y - depth))  # 左中
    pants_top_points.add_vertex((x + width + depth, y))  # 左下
    pants_top_points.filled = True
    pants_top_points.fill_color = pants_top_color
    pants_top_points.color = border_color
    window.add(pants_top_points)

    # 褲子側面
    pants_side_points = GPolygon()
    pants_side_points.add_vertex((x, y - depth))  # 左上
    pants_side_points.add_vertex((x, y - depth + pants_height))  # 左下
    pants_side_points.add_vertex((x + depth, y + pants_height))  # 右下
    pants_side_points.add_vertex((x + depth, y))  # 右上
    pants_side_points.filled = True
    pants_side_points.fill_color = pants_side_color
    pants_side_points.color = border_color
    window.add(pants_side_points)

    # 繪製鞋子部分（下半段）
    shoe_y = y + pants_height

    # 鞋子正面
    shoe_front = GRect(width, shoe_height, x=x + depth, y=shoe_y)
    shoe_front.filled = True
    shoe_front.fill_color = shoe_front_color
    shoe_front.color = border_color
    window.add(shoe_front)

    # 鞋子側面
    shoe_side_points = GPolygon()
    shoe_side_points.add_vertex((x, shoe_y - depth))  # 左上
    shoe_side_points.add_vertex((x, shoe_y - depth + shoe_height))  # 左下
    shoe_side_points.add_vertex((x + depth, shoe_y + shoe_height))  # 右下
    shoe_side_points.add_vertex((x + depth, shoe_y))  # 右上
    shoe_side_points.filled = True
    shoe_side_points.fill_color = shoe_side_color
    shoe_side_points.color = border_color
    window.add(shoe_side_points)

    # 添加腿的邊框線，增強立體感
    # 褲子正面邊框
    pants_front_border = GRect(width, pants_height, x=x + depth, y=y)
    pants_front_border.filled = False
    pants_front_border.color = border_color
    window.add(pants_front_border)

    # 鞋子正面邊框
    shoe_front_border = GRect(width, shoe_height, x=x + depth, y=shoe_y)
    shoe_front_border.filled = False
    shoe_front_border.color = border_color
    window.add(shoe_front_border)

    # 頂面邊框
    top_border = GPolygon()
    top_border.add_vertex((x + depth, y))
    top_border.add_vertex((x, y - depth))
    top_border.add_vertex((x + width, y - depth))
    top_border.add_vertex((x + width + depth, y))
    top_border.filled = False
    top_border.color = border_color
    window.add(top_border)

    # 側面邊框
    side_border = GPolygon()
    side_border.add_vertex((x, y - depth))
    side_border.add_vertex((x, y - depth + height))
    side_border.add_vertex((x + depth, y + height))
    side_border.add_vertex((x + depth, y))
    side_border.filled = False
    side_border.color = border_color
    window.add(side_border)


def draw_face(window, front_x, front_y, size):
    """
    在正面加上 8x8 Minecraft 臉部像素
    """
    unit = size / 8  # 每一像素的寬/高
    center_x = front_x + size / 2  # 正面中心 X 座標
    center_y = front_y + size / 2  # 正面中心 Y 座標

    def add_pixel(rel_x, rel_y, color):
        """
        以相對座標繪製像素
        rel_x, rel_y: 相對於臉部中心的座標（單位：像素）
        """
        pixel_x = center_x + rel_x * unit
        pixel_y = center_y + rel_y * unit
        pixel = GRect(unit, unit, x=pixel_x, y=pixel_y)
        pixel.filled = True
        pixel.fill_color = color
        pixel.color = color
        window.add(pixel)

    # 顏色定義
    hair_color = (111, 78, 55)  # 咖啡色頭髮
    skin_color = (205, 158, 122)  # 臉部膚色
    eye_white = (255, 255, 255)  # 眼白
    pupil_color = (130, 0, 200)  # 紫色瞳孔
    mouth_color = (82, 50, 33)  # 嘴巴色
    nose_color = (140, 90, 60)  # 鼻子顏色

    # 繪製臉部背景（整個正面區域）
    for i in range(8):
        for j in range(8):
            add_pixel(i - 4, j - 4, skin_color)

    # 繪製頭髮 - 根據您的需求
    # 第一排頭髮（最上方）- 全部覆蓋
    for i in range(8):
        add_pixel(i - 4, -4, hair_color)

    # 第二排頭髮 - 全部覆蓋
    for i in range(8):
        add_pixel(i - 4, -3, hair_color)

    # 第三排頭髮 - 只有最左邊和最右邊是頭髮
    add_pixel(-4, -2, hair_color)  # 最左邊
    add_pixel(3, -2, hair_color)  # 最右邊
    # 中間6格保持皮膚色（不畫頭髮）

    # 繪製嘴巴
    add_pixel(-2, 2, mouth_color)
    add_pixel(1, 2, mouth_color)
    add_pixel(-2, 3, mouth_color)
    add_pixel(1, 3, mouth_color)
    add_pixel(-1, 3, mouth_color)
    add_pixel(0, 3, mouth_color)

    # 繪製眼睛
    # 左眼
    add_pixel(-3, 0, eye_white)
    add_pixel(-2, 0, pupil_color)
    # 右眼
    add_pixel(1, 0, pupil_color)
    add_pixel(2, 0, eye_white)

    # 繪製鼻子
    add_pixel(-1, 1, nose_color)
    add_pixel(0, 1, nose_color)


def draw_side_hair_pixels(window, x, y, size, depth):
    """
    在立方體側面使用像素方塊方式繪製頭髮
    使用類似正面的方式，用座標系統精確控制每個像素
    """
    hair_color = (111, 78, 55)  # 咖啡色頭髮

    # 側面的尺寸
    side_width = depth
    side_height = size

    # 將側面劃分為網格
    cols = 8  # 水平方向（深度方向）的網格數
    rows = 8  # 垂直方向的網格數

    # 計算每個像素的寬度和高度
    pixel_width = side_width / cols
    pixel_height = side_height / rows

    # 定義側面頭髮的像素圖案
    # 使用二維列表表示，1表示有頭髮，0表示沒有
    # 這裡是一個示例圖案，您可以根據需要修改
    hair_pattern = [
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第1行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第2行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第3行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第4行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第5行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第6行
        [1, 1, 1, 1, 1, 1, 1, 1],  # 第7行
        [1, 1, 0, 0, 0, 0, 1, 1]   # 第8行
    ]

    # 根據圖案繪製側面頭髮
    for row in range(rows):
        for col in range(cols):
            if hair_pattern[row][col] == 1:
                # 計算像素的位置
                pixel_x = x + col * pixel_width
                pixel_y = y - depth + row * pixel_height

                # 繪製像素
                pixel = GRect(pixel_width, pixel_height, x=pixel_x, y=pixel_y)
                pixel.filled = True
                pixel.fill_color = hair_color
                pixel.color = hair_color
                window.add(pixel)


if __name__ == '__main__':
    main()