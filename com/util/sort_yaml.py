# _*_ coding: utf-8 _*_
"""
# @Time : 2021/1/8 23:23
# @Author : River
# @File : sort_yaml.py
# @desc : 按顺序读写yaml文件
"""
from collections import OrderedDict

import yaml


def ordered_yaml_load(yaml_path, _loader=yaml.Loader,
                      object_pairs_hook=OrderedDict):
    """
    按顺序读取yaml文件
    """

    class OrderedLoader(_loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path, encoding='utf8') as stream:
        return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, _dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(_dumper):
        """
        按顺序生成aml文件
        """
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)
