# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/13 18:01 
# @Author : lijun7 
# @File : simple_gui_demo.py
# @desc :
"""
import PySimpleGUI as sg

# 窗口内的所有控件.
layout = [
    [sg.Button('oms')],
    [sg.Button('soa')],
    [sg.Cancel()],
    [sg.Menu(menu_def, tearoff=False, pad=(20, 1))],
    [sg.ButtonMenu('ButtonMenu', key='-BMENU-', menu_def=menu_def[0])]
]
# 生成窗口
window = sg.Window('Window Title', layout)

# 消息处理和输入消息接收
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    print('You entered ', values[0])

window.close()
