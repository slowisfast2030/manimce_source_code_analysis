from manim import *

class Space(Scene):
    def construct(self):
        
        grid = NumberPlane()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.to_corner(UL)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                          + np.array(
                    [
                        0,
                        #np.sin(p[1]),
                        0,
                        #np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()