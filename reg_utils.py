#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/2/19
# @Author: Neil Steven
import logging
import os

from mstsc import MsTSC
from network_list import NetworkList


def main():
    print("Welcome to use the Reg Utils!\n")
    while True:
        print("Please choose the action: ")
        print("[1] Change MsTSC port")
        print("[2] Clear old networks")
        user_input = input().strip()

        if user_input == '1':
            port = int(input("Please input your port number: "))
            MsTSC.change_port(port)
        elif user_input == '2':
            NetworkList.delete_old_networks()

        os.system("pause")
        print()


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        logging.exception(e)
