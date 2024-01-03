from manim import *

class GetRiemannRectanglesExample(Scene):
    def construct(self):
        # 创建坐标轴并设置x轴和y轴的配置
        ax = Axes(
            x_range=[-0.5, 4, 1],  # 从-0.5开始以确保0会显示
            y_range=[-0.5, 20, 2.5],  # 从-0.5开始以确保0会显示
            x_length=6,
            y_length=6,
            tips=False,
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 1,2,3,4],  # 在x轴上只显示0, 5, 10
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 5, 10,15,20],  # 在y轴上也只显示0, 5, 10
            }
        )
        
        ax.set_opacity(0.5)
        # 绘制函数
        quadratic = ax.plot(lambda x: 2*PI*x, x_range=[0, 3], color=TEAL, stroke_width=2)

        # 获取黎曼矩形
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 3], dx=0.1, color=[BLUE, GREEN]
        )

        self.add(
            ax, rects_left, quadratic
        )
