#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/2/19
# @Author: Neil Steven
import re
import winreg

from reg_operation import RegOperation


class NetworkList(RegOperation):
    NETWORK_LIST_PATH = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList"
    NETWORK_LIST_SIGNATURES_UNMANAGED = NETWORK_LIST_PATH + r"\Signatures\Unmanaged"
    NETWORK_LIST_PROFILE = NETWORK_LIST_PATH + r"\Profiles"

    @classmethod
    def delete_old_networks(cls):
        try:
            unmanaged_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cls.NETWORK_LIST_SIGNATURES_UNMANAGED)
            profile_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cls.NETWORK_LIST_PROFILE)
            cls._get_unmanaged_keys(unmanaged_reg_key, profile_reg_key)
            winreg.CloseKey(unmanaged_reg_key)
            winreg.CloseKey(profile_reg_key)
        except EnvironmentError:
            print("The reg key", cls.NETWORK_LIST_PROFILE, "does not exist, ignored.")

    @classmethod
    def _get_unmanaged_keys(cls, unmanaged_reg_key, profile_reg_key):
        saved_networks_name = []
        old_networks_name = []

        network_keys = cls.enum_keys(unmanaged_reg_key)
        for network_key in network_keys:
            network_value_reg_key = winreg.OpenKey(unmanaged_reg_key, network_key)
            network_values = cls.enum_values(network_value_reg_key)

            network_name = None
            network_profile_guid = None
            for network_value in network_values:
                if network_value.name == "FirstNetwork":
                    network_name = network_value.data
                if network_value.name == "ProfileGuid":
                    network_profile_guid = network_value.data

            if network_name is None or network_profile_guid is None:
                print("Invalid key! 'FirstNetwork' or 'ProfileGuid' does not exist.")

            saved_networks_name.append(network_name)

            # Delete the signature unmanaged key and profile key
            if re.match(r"网络[ \d+]?", network_name) is not None:
                winreg.DeleteKey(unmanaged_reg_key, network_key)
                winreg.DeleteKey(profile_reg_key, network_profile_guid)
                old_networks_name.append(network_name)

        print("Deleted networks: ")
        for name in old_networks_name:
            print(name)

        print("\nCurrent networks:")
        for name in list(set(saved_networks_name).difference(set(old_networks_name))):
            print(name)
