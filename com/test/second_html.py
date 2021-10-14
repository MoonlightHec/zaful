"""这个展示了GridBox方式的布局.
    grid布局允许以一种灵活的方式定义布局
    使用GridBox.define_grid，传递一个二维可迭代对象作为参数。
    被定义在grid中的每个元素, 是一个关键部分对于GridBox.append函数
    在这个例子中, 模型是一些字符串, 每个字符都被用来当作key.
    一个key可以在定义的模型中出现多次, 使组件覆盖更大的空间.
    每个在布局中的纵列和横行的大小都可以通过GridBox.style被定义,
     style参数是类似这样的
     {'grid-template-columns':'10% 90%', 'grid-template-rows':'10% 90%'}.
"""

import remi.gui as gui
from remi import start, App
import os


class MyApp(App):
    def main(self):
        # 创建一个grid格式的容器
        main_container = gui.HBox(width='100%', height='100%')

        select_app_lal = gui.Label('请选择系统')
        select_app_lal.style['background-color'] = 'blue'

        select_app_dd = gui.DropDown('Change layout', height='100%')
        select_app_dd.style.update({'font-size': 'large'})
        # 设置样式
        select_app_dd.add_class("form-control dropdown")
        # 添加下拉框内容
        select_app_item1 = gui.DropDownItem('OMS')
        select_app_item2 = gui.DropDownItem('SOA')
        select_app_dd.append(select_app_item1, 'item1')
        select_app_dd.append(select_app_item2, 'item2')

        main_container.append([
            select_app_lal,
            select_app_dd
        ])

        # returning the root widget
        return main_container


if __name__ == "__main__":
    start(MyApp, debug=True)
