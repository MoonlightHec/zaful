# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/8 13:55 
# @Author : mhec 
# @File : pay_params.py
# @desc :
"""
import os

from moon_util.sort_yaml import ordered_yaml_load

#
page_path = os.path.dirname(os.path.abspath(__file__))
user_config_datas = ordered_yaml_load(page_path + '\pps_user_config_cases')