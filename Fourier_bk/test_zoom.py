from manim import *

class MyZoomedScene(ZoomedScene):
    def construct(self):
        # Create a square
        square = Text("hello world").scale(1)
        self.add(square)

        # Activate Zooming
        self.activate_zooming(animate=False)

        # Move and set the zoomed camera frame
        self.zoomed_camera.frame.move_to(square)
        self.zoomed_camera.frame.set_color(PURPLE)
        self.zoomed_display.to_corner(UL)
        self.zoomed_display.scale(1)
        #self.zoomed_camera.frame.set_height(2)
        #self.zoomed_camera.frame.set_width(3)
        #self.zoomed_camera.frame.scale(2)
 
        # Animate the zoom
        #self.play(self.zoomed_camera.frame.animate.scale(0.5))
        #self.wait()
        self.play(square.animate.shift(RIGHT*1))
        
        # Additional animations or objects can be added here
