from manim import *

class MyZoomedScene(ZoomedScene):
    def construct(self):
        # Create a square
        square = Text("hello world").scale(1)
        self.add(square)

        # Activate Zooming
        self.activate_zooming(animate=False)

        # 缩放镜头有一个属性frame，它是一个Square，可以用来调整镜头的大小和位置
        self.zoomed_camera.frame.move_to(square)
        self.zoomed_camera.frame.set_color(PURPLE)
        self.zoomed_camera.frame.scale(1)

        # 放大的区域
        self.zoomed_display.to_corner(UL)
        self.zoomed_display.scale(1)

        self.zoomed_camera.cairo_line_width_multiple =0.02
        self.zoomed_camera.default_frame_stroke_width=22
        
 
        # Animate the zoom
        #self.play(self.zoomed_camera.frame.animate.scale(0.5))
        #self.wait()
        self.play(square.animate.shift(RIGHT*1))
        
        # Additional animations or objects can be added here

class ZoomedScene(ZoomedScene):
    def construct(self):
        # Create a square
        square = Square(color=BLUE, fill_opacity=0.5)
        self.add(square)

        # Set up the zoom
        self.zoomed_camera.frame.move_to(square)
        self.zoomed_camera.frame.set_color(PURPLE)
        self.zoomed_camera.frame.set_stroke(width=1)
        self.activate_zooming(animate=True)

        # Animate
        self.play(square.animate.scale(0.3))
        self.wait(1)

        # More animations inside the zoomed camera
        self.play(square.animate.rotate(PI/4))
        self.wait(1)

