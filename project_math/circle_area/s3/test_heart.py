from manim import *

class SVGExample(Scene):
    def construct(self):
        # 替换下面的路径为您的SVG文件的路径
        svg_file = "heart.svg"
        
        # 使用SVGMobject读取SVG文件
        svg_object = SVGMobject(svg_file).set_fill(RED, 1)
        
        # 将SVG对象添加到场景
        self.add(svg_object)
