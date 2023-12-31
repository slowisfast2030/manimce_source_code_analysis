from manim import *
"""
将circle的点集设置为顺时针
在manimgl环境下会出现奇怪的效果

在manimce环境下(不论cairo还是opengl), 效果正常

尽管manimgl和manimce都支持opengl
但是渲染细节还是有不同
----linus
终于知道原因了
在manimgl环境下, 需要添加一行: ring.get_triangulation() 
就正常了

manim ring_merge_anticlock.py test -pql --renderer=cairo
"""
class test(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        if config.renderer == RendererType.CAIRO:
            ring = Circle(radius = 2, num_components=9).center()
            print("---run by cairo")
        else:
            ring = Circle(radius = 2, num_components=8).center()
            print("---run by opengl")
        
        ring.set_stroke(width = 0.5)
        ring.set_fill(RED,0.5)

        # 将ring的点集变为顺时针
        ring.rotate(PI, RIGHT)

        for index, point in enumerate(ring.points):
            dot = Dot(point)
            label = Text(str(index), font_size=24).next_to(dot, point-ring.get_center(), buff=0.1)
            self.add(dot, label)

        self.add(ring)
