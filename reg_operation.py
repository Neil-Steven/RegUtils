#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/2/19
# @Author: Neil Steven
import winreg


class RegValue:
    def __init__(self, value_name, value_data, value_type):
        self.name = value_name
        self.data = value_data
        self.type = value_type


class RegOperation:
    @staticmethod
    def enum_keys(reg_key):
        result = []
        try:
            index = 0
            while True:
                key = winreg.EnumKey(reg_key, index)
                result.append(key)
                index += 1
        except OSError:
            pass
        return result

    @staticmethod
    def enum_values(reg_key):
        result = []
        try:
            index = 0
            while True:
                value = winreg.EnumValue(reg_key, index)
                result.append(RegValue(value[0], value[1], value[2]))
                index += 1
        except OSError:
            pass
        return result
