from manim import *

"""
开场
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s0(Scene):
    def setup(self):
        pass

    def construct(self):
        pass

    # 屏幕从上至下出现3种解法
    """
    有一个很炫的转场
    开场中间出现了一个三角形
    然后这个三角形被分成了三个部分：上中下
    然后在上中下三个三角形的基础上分别显示三种解法

    非常丝滑
    """
    def introduce_three_methods(self):
        
        # self.introduce_first_method()
        # self.introduce_second_method()
        # self.introduce_third_method()

        pass    

    # 第一种解法
    def introduce_first_method(self):

        pass

    # 第二种解法
    def introduce_second_method(self):

        pass

    # 第三种解法    
    def introduce_third_method(self):

        pass

    