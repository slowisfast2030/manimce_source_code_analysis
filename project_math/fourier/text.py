import svgwrite

# 创建一个新的 SVG 绘图
dwg = svgwrite.Drawing('text.svg', size=(200, 200))

# 添加英文字母
# 您可以通过设置 'insert' 来改变文字的位置
# 'fill' 用来设置文字颜色
dwg.add(dwg.text('A', insert=(50, 50), fill='black'))
dwg.add(dwg.text('B', insert=(50, 80), fill='red'))
dwg.add(dwg.text('C', insert=(50, 110), fill='blue'))

# 保存文件
dwg.save()
