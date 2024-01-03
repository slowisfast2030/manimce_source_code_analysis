from manim import *

class GetRiemannRectanglesExample(Scene):
    def construct(self):
        # 创建坐标轴并设置x轴和y轴的配置
        ax = Axes(
            x_range=[-0.1, 4, 1],  # 从-0.5开始以确保0会显示
            y_range=[-0.5, 20, 2.5],  # 从-0.5开始以确保0会显示
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GRAY},  # 将坐标轴线条设置为灰色
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 1,2,3,4],  # 在x轴上只显示0, 5, 10
                "include_ticks": True
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 5, 10,15,20],  # 在y轴上也只显示0, 5, 10
                "numbers_with_elongated_ticks": [0, 5, 10,15,20],
                "decimal_number_config": {
                    "num_decimal_places": 0,  # 设置为0以显示整数
                    "color": BLUE,  # 设置x轴数字的颜色
                },
            },
        )
        
        # 设置坐标轴的颜BLUE
        #ax.set_color(GRAY)
        ax.set_opacity(1)
        # 绘制函数
        quadratic = ax.plot(lambda x: 2*PI*x, x_range=[0, 3.5], color=BLUE, stroke_width=2)

        # 获取黎曼矩形
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 3], dx=0.1, color=[BLUE, GREEN]
        )

        # 创建x轴标签并指定位置
        x_label = ax.get_x_axis_label("r", direction=UP + RIGHT, buff=0.05)


        self.add(
            ax, rects_left, quadratic, x_label
        )

        thinner_rects_list = [
            ax.get_riemann_rectangles(
                quadratic,
                x_range=[0,3],
                dx = 1./(10*n),
                stroke_width = 1./(n),
                color=[BLUE, GREEN]
            )
            for n in range(2, 6)
        ]

        for new_rects in thinner_rects_list:
            self.play(
                Transform(
                    rects_left, new_rects, 
                    lag_ratio = 0.3,
                    run_time = 1
                )
            )

        self.wait()