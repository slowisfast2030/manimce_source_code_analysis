from manim import *

#config.background_color = WHITE
# config.frame_width = 9
# config.frame_height = 16

# config.pixel_width = 1080
# config.pixel_height = 1920

class simpleScene(Scene):
    def construct(self):
        plane = NumberPlane(x_range=(-4.5, 4.5), y_range=(-8, 8))
        t = Triangle(color=PURPLE, fill_opacity=0.5)
        self.add(plane, t)
        self.wait()


class CodeFromString(Scene):
    def construct(self):
        # pixel_height = config["pixel_height"]  #  1080 is default
        # pixel_width = config["pixel_width"]  # 1920 is default
        # frame_width = config["frame_width"]
        # frame_height = config["frame_height"]
        # config["frame_width"] = 9
        # config["frame_height"] = 16
        # config["pixel_height"] = 1920
        # config["pixel_width"] = 1080
        config.media_width = "40%"
        code = '''
                from manim import Scene, Square

                class FadeInSquare(Scene):
                    def construct(self):
                        s = Square()
                        self.play(FadeIn(s))
                        self.play(s.animate.scale(2))
                        self.wait()
                '''
        rendered_code = Code(code=code, tab_width=4, background="window",
                            language="Python", font="Monospace")
        self.play(Write(rendered_code))
        self.wait()

class plotExample(Scene):
    def construct(self):
        # construct the axes
        ax_1 = Axes(
            x_range=[0.001, 6],
            y_range=[-8, 2],
            x_length=5,
            y_length=3,
            tips=False,
        )
        ax_2 = ax_1.copy()
        ax_3 = ax_1.copy()

        # position the axes
        ax_1.to_corner(UL)
        ax_2.to_corner(UR)
        ax_3.to_edge(DOWN)
        axes = VGroup(ax_1, ax_2, ax_3)

        # create the logarithmic curves
        def log_func(x):
            return np.log(x)

        # a curve without adjustments; poor interpolation.
        curve_1 = ax_1.plot(log_func, color=PURE_RED)

        # disabling interpolation makes the graph look choppy as not enough
        # inputs are available
        curve_2 = ax_2.plot(log_func, use_smoothing=False, color=ORANGE)

        # taking more inputs of the curve by specifying a step for the
        # x_range yields expected results, but increases rendering time.
        curve_3 = ax_3.plot(
            log_func, x_range=(0.001, 6, 0.001), color=PURE_GREEN
        )

        curves = VGroup(curve_1, curve_2, curve_3)

        self.add(axes, curves)
        self.wait()