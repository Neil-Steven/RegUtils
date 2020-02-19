#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/2/19
# @Author: Neil Steven
import winreg

from reg_operation import RegOperation


class MsTSC(RegOperation):
    TERMINAL_SERVER_PATH = r"SYSTEM\CurrentControlSet\Control\Terminal Server"
    RDP_TCP = TERMINAL_SERVER_PATH + r"\WinStations\RDP-Tcp"
    TDS_TCP = TERMINAL_SERVER_PATH + r"\Wds\rdpwd\Tds\tcp"

    @classmethod
    def change_port(cls, port=3389):
        try:
            rdp_tcp_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cls.RDP_TCP)
            tds_tcp_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cls.TDS_TCP)

            winreg.SetValueEx(rdp_tcp_reg_key, "PortNumber", 0, winreg.REG_DWORD, port)
            winreg.SetValueEx(tds_tcp_reg_key, "PortNumber", 0, winreg.REG_DWORD, port)

            winreg.CloseKey(rdp_tcp_reg_key)
            winreg.CloseKey(tds_tcp_reg_key)
        except EnvironmentError as e:
            print(e)
