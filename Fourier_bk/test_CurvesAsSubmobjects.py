from manim import *

class LineGradientExample(Scene):
    def construct(self):
        curve = ParametricFunction(lambda t: [t, np.sin(t), 0], t_range=[-PI, PI, 0.01], stroke_width=10)
        curve.set_color_by_gradient(BLUE, RED)
        
        new_curve = CurvesAsSubmobjects(curve)
        print(len(new_curve))# 这个值主要是由t_range数组的个数决定
        new_curve.set_color_by_gradient(BLUE, RED)
        self.add(new_curve.shift(UP), curve)
        
        self.wait()