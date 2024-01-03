from manim import *

class ring2rect(Scene):
    def construct(self):
        ring = self.get_ring(radius = 1, dR = 0.1)
        self.add(ring)
        rect = self.get_rect(ring)  
        self.add(rect)

        self.show_point_label(ring)
        self.show_point_label(rect, dr=LEFT)

        self.play(MoveToTarget(ring))
        self.wait()
        pass
    
    def show_point_label(self, vm: VMobject, dr=UP):

        bezier_points = vm.get_points()
        
        # Iterate over each point and add a label
        for i, point in enumerate(bezier_points):
            dot = Dot(point, color=RED).scale(0.5)  # Create a small red dot at the point
            label = Text(f"{i}", font_size=20).next_to(dot, dr)  # Create a label with the index number
            if i<=22:
                self.add(dot, label)  # Add the dot and label to the scene
        
        pass

    def get_ring(self, radius, dR, color = GREEN):
        ring = VMobject()
        """
        为何要旋转90度
        当旋转90度后, 圆的起点正好在正上方
        后续需要将这个圆环展开横向的长条, 开口放在正上方比较好看

        如果不旋转, 就会将开口放在右侧
        这样比较适合展开为竖直的长条

        以cairo作为后端
        circle的点集数目是多少?
        """
        #print(len(Circle(radius=radius+dR).rotate(PI/2).get_points()))
        # 经过打印后发现点集的数目是32，不是64
        # 奇怪：为何一开始写64呢？
        # 圆是由8段圆弧拼接而成，每一段圆弧由4个点构成
        outer_circle = Circle(radius=radius+dR).rotate(0*PI).get_points()[4:28]
        inner_circle = Circle(radius=radius).rotate(0*PI).get_points()[4:28][::-1]

        # 遵守manimce的约定，每一段贝塞尔曲线由4个点构成
        line1 = [outer_circle[-1], 
                 interpolate(outer_circle[-1], inner_circle[0], 0.3),
                 interpolate(outer_circle[-1], inner_circle[0], 0.6),
                 inner_circle[0]]
        
        line2 = [inner_circle[-1],
                interpolate(inner_circle[-1], outer_circle[0], 0.3),
                interpolate(inner_circle[-1], outer_circle[0], 0.6),
                outer_circle[0]]
        
        """
        将内环和外环的点集
        加上连接内外环的直线
        一起作为新的点集
        """
        points_to_add = list(outer_circle) + line1 + list(inner_circle) + line2

        ring.append_points(points_to_add)
        ring.set_stroke(width = 0)
        """
        我非常奇怪的一点:
        这样人工构造出了点集之后
        着色的时候是如何区分区域的内外呢？

        cairo后端似乎很容易
        opengl后端不容易理解
        """
        ring.set_fill(color, opacity = 1)
        # 在这里明确了ring的位置
        ring.move_to(LEFT*2)
        ring.R = radius 
        ring.dR = dR

        return ring
    
    def get_rect(self, ring: VMobject):
        # 内外环一共16段曲线，外加两条直线，一共18段
        n_anchors = ring.get_num_curves()
        print(n_anchors)            
        target = VMobject()
        target.set_points_as_corners([
            interpolate(ORIGIN,  DOWN, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ]+[
            interpolate(DOWN+RIGHT, RIGHT, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ])
        # 将折线闭合
        #target.add_line_to(ORIGIN)    
        line = [target.get_points()[-1], 
                interpolate(target.get_points()[-1], target.get_points()[0], 0.3),
                interpolate(target.get_points()[-1], target.get_points()[0], 0.6),
                target.get_points()[0]] 
        target.append_points(line)


        target.stretch_to_fit_height(2*PI*ring.R)
        target.stretch_to_fit_width(ring.dR)
        target.move_to(RIGHT*2)
        target.set_stroke(BLACK, 1)
        target.set_fill(ring.get_fill_color(), 1)

        print(len(ring.get_points()))
        print(len(target.get_points()))

        ring.target = target
        ring.original_ring = ring.copy()
        return target