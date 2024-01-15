from manim import *

class CameraFocusExample(MovingCameraScene):
#class CameraFocusExample(Scene):
    #AttributeError: 'Camera' object has no attribute 'frame'
    def construct(self):
        # Create some objects
        square = Square(color=BLUE, fill_opacity=0.5)
        circle = Circle(color=RED, fill_opacity=0.5).shift(LEFT * 3)
        triangle = Triangle(color=GREEN, fill_opacity=0.5).shift(RIGHT * 3)

        # Add objects to the scene
        self.add(square, circle, triangle)
        zoomed_display = ImageMobjectFromCamera(self.camera)
        zoomed_display.scale(0.5)
        zoomed_display.move_to(UP * 2.5)
        zoomed_display.add_display_frame()
        zoomed_display.display_frame.set_color(RED)
        self.add(zoomed_display)



        # Focus on the square
        self.play(self.camera.frame.animate.move_to(square).set(width=square.width * 5))

        # Wait and then focus on the circle
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(circle).set(width=circle.width * 5))

        # Wait and then focus on the triangle
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(triangle).set(width=triangle.width * 5))

        # Zoom out to show all objects
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(square).set(width=10))

        self.wait(1)
