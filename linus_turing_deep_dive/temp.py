from manim import *

class MoveAndZoomCamera(Scene):
    def construct(self):
        circle = Circle(color=BLUE) # 创建一个蓝色的圆形
        square = Square(color=RED) # 创建一个红色的正方形
        self.add(circle, square) # 将圆形和正方形添加到场景中
        self.play(Create(circle), Create(square)) # 播放创建圆形和正方形的动画
        self.wait() # 等待一秒
        self.play(self.camera.frame.animate.move_to(square)) # 播放移动Camera的frame到正方形的位置的动画
        self.wait() # 等待一秒
        self.play(self.camera.frame.animate.scale(0.5)) # 播放缩小Camera的frame一半的动画
        self.wait() # 等待一秒

with tempconfig({"quality": "medium_quality", "preview": True}):
    scene = MoveAndZoomCamera()
    scene.render()