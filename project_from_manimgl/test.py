from manim import *

"""
使用不同的后端渲染略微不一样


"""
class test(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
        self.wait()

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)
        self.play(Transform(circle, square))
        self.wait()