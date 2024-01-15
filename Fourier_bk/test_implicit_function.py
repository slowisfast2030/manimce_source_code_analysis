from manim import *

class ImplicitFunctionExample(Scene):
    def construct(self):
        graph = ImplicitFunction(
            lambda x, y: x * y ** 2 - x ** 2 * y - 2,
            color=YELLOW
        )
        self.add(NumberPlane(), graph)