#!/usr/bin/env python3.6
# 

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])) + os.path.sep + 'lib' + os.path.sep + 'python' + os.path.sep + 'crabtable')

from CrabTable import *

import glob
import math
import numpy
import astropy
from astropy import units
from astropy.io import fits
import re
import json





#########################################
#               Functions               #
#########################################

def recognize_Col_Source(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        Pattern = re.compile("^[_]*(SOURCE)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(OBJECT)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(NAME)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(SOURCE_[a-zA-Z]*)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(OBJECT_[a-zA-Z]*)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(NAME_[a-zA-Z]*)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
    return list(set(recognized_list))


def recognize_Col_ID(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        Pattern = re.compile("^[_]*(ID)[^a-zA-Z]*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(id)[^a-zA-Z]*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(ID_[a-zA-Z]*)[^a-zA-Z]*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(id_[a-zA-Z]*)[^a-zA-Z]*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(NUMBER)[^a-zA-Z]*", re.IGNORECASE)
        if Pattern.match(input_str):
            recognized_list.append(input_str)
    return list(set(recognized_list))


def recognize_Col_FLUX(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        # skip FLAG
        Pattern_Flag = re.compile(".*(_FLAG_).*", re.IGNORECASE)
        if Pattern_Flag.match(input_str):
            continue
        # fix FLUX_ERR -> FLUX
        if input_str.find('FLUX_ERR')>=0:
            input_str2 = input_str.replace('FLUX_ERR','FLUXERR')
        else:
            input_str2 = input_str
        # recognize FLUX
        Pattern = re.compile("^[_]*(FLUX_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(f)([0-9]+).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(f_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^.*(_FLUX_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(f)(ch[0-9]+)")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(f)(K)")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
    # 
    if special_file_name.find('Laigle')>=0:
        special_remove_list = ['FLUX_RADIUS', 'FLUX_814W', 'FLUX_XMM_0.5_2', 'FLUX_XMM_2_10', 'FLUX_XMM_5_10', 'FLUX_CHANDRA_0.5_2', 'FLUX_CHANDRA_2_10', 'FLUX_CHANDRA_0.5_10', 'FLUX_NUSTAR_3_24', 'FLUX_NUSTAR_3_8', 'FLUX_NUSTAR_8_24']
        # 'FLUX_814W' is actually MAG instead of FLUX in Laigle+ catalog
        for special_remove_item in special_remove_list:
            if special_remove_item in recognized_list:
                recognized_list.remove(special_remove_item)
    # 
    return recognized_list


def recognize_Col_FLUXERR(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        # skip FLAG
        Pattern_Flag = re.compile(".*(_FLAG_).*", re.IGNORECASE)
        if Pattern_Flag.match(input_str):
            continue
        # fix FLUX_ERR -> FLUX
        if input_str.find('FLUX_ERR')>=0:
            input_str2 = input_str.replace('FLUX_ERR','FLUXERR')
        else:
            input_str2 = input_str
        # recognize FLUXERR
        Pattern = re.compile("^[_]*(FLUXERR_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(FLUX_ERR_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(df)([0-9]+).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(df_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(e_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^.*(_FLUXERR_).*")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(df)(ch[0-9]+)")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(df)(K)")
        if Pattern.match(input_str2):
            recognized_list.append(input_str)
    # 
    if special_file_name.find('Laigle')>=0:
        special_remove_list = ['FLUXERR_814W', 'FLUXERR_NUSTAR_3_24', 'FLUXERR_NUSTAR_3_8', 'FLUXERR_NUSTAR_8_24']
        # 'FLUX_814W' is actually MAG instead of FLUX in Laigle+ catalog
        for special_remove_item in special_remove_list:
            if special_remove_item in recognized_list:
                recognized_list.remove(special_remove_item)
    # 
    return recognized_list


def recognize_Col_MAG(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        Pattern = re.compile("^[_]*(MAG_).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(m)([0-9]+).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(m_).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
    return recognized_list


def recognize_Col_MAGERR(input_list, special_file_name=''):
    recognized_list = []
    if type(input_list) is not list:
        input_list = [input_list]
    for input_str in input_list:
        if type(input_str) is not str:
            input_str = str(input_str)
        Pattern = re.compile("^[_]*(MAGERR_).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(MAG_ERR_).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(e)([0-9]+).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
        Pattern = re.compile("^[_]*(e_).*")
        if Pattern.match(input_str):
            recognized_list.append(input_str)
    return recognized_list


def recognize_Filter_Instrument_by_Short_Name(input_str, catalog_name = ''):
    Filter_Dict = {}
    Filter_Dict['IA427'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA464'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA484'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA505'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA527'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA574'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA624'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA679'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA709'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA738'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA767'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IA827'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB427'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB464'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB484'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB505'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB527'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB574'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB624'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB679'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB709'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB738'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB767'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['IB827'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['NB711'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['NB816'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
    Filter_Dict['SPLASH_1'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['SPLASH_2'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['SPLASH_3'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['SPLASH_4'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['ch1'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['ch2'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['ch3'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['ch4'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['IRAC1'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['IRAC2'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['IRAC3'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    Filter_Dict['IRAC4'] = 'Spitzer IRAC' # Laigle+2016 Table 1
    if type(catalog_name) is str:
        if catalog_name.find('Laigle')>=0:
            Filter_Dict['u'] = 'CFHT MegaCam' # Laigle+2016 Table 1
            Filter_Dict['B'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['V'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['r'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['ip'] ='Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['zp'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['zpp'] = 'Subaru Suprime Cam' # Laigle+2016 Table 1
            Filter_Dict['yHSC'] = 'VISTA VIRCAM' # Laigle+2016 Table 1
            Filter_Dict['Y'] = 'VISTA VIRCAM' # Laigle+2016 Table 1
            Filter_Dict['J'] = 'VISTA VIRCAM' # Laigle+2016 Table 1
            Filter_Dict['H'] = 'VISTA VIRCAM' # Laigle+2016 Table 1
            Filter_Dict['Hw'] = 'CFHT WIRCam' # Laigle+2016 Table 1
            Filter_Dict['Ks'] = 'VISTA VIRCAM' # Laigle+2016 Table 1
            Filter_Dict['Ksw'] = 'CFHT WIRCam' # Laigle+2016 Table 1
    if type(catalog_name) is str:
        if catalog_name.find('Jin')>=0:
            Filter_Dict['K'] = 'CFHT WIRCam or VISTA VIRCAM' # Jin+2018 used McCraken+2010 catalog, or Muzzin+2013 catalog.
    if type(input_str) is str:
        if input_str in Filter_Dict:
            return Filter_Dict[input_str]
    return 'unknown_' + input_str


def recognize_Filter_Wavelength_by_Short_Name(input_str):
    Filter_Dict = {}
    Filter_Dict['u'] = 3823.3e-4 # Laigle+2016 Table 1
    Filter_Dict['B'] = 4458.3e-4 # Laigle+2016 Table 1
    Filter_Dict['V'] = 5477.8e-4 # Laigle+2016 Table 1
    Filter_Dict['r'] = 6288.7e-4 # Laigle+2016 Table 1
    Filter_Dict['ip'] = 7683.9e-4 # Laigle+2016 Table 1
    Filter_Dict['zp'] = 9105.7e-4 # Laigle+2016 Table 1
    Filter_Dict['zpp'] = 9105.7e-4 # Laigle+2016 Table 1
    Filter_Dict['yHSC'] = 10214.2e-4 # Laigle+2016 Table 1
    Filter_Dict['Y'] = 10214.2e-4 # Laigle+2016 Table 1
    Filter_Dict['J'] = 12534.6e-4 # Laigle+2016 Table 1
    Filter_Dict['H'] = 16453.4e-4 # Laigle+2016 Table 1
    Filter_Dict['Hw'] = 16453.4e-4 # Laigle+2016 Table 1
    Filter_Dict['K'] = 21539.9e-4 # Laigle+2016 Table 1
    Filter_Dict['Ks'] = 21539.9e-4 # Laigle+2016 Table 1
    Filter_Dict['Ksw'] = 21539.9e-4 # Laigle+2016 Table 1
    Filter_Dict['IA427'] = 4263.4e-4 # Laigle+2016 Table 1
    Filter_Dict['IA464'] = 4635.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IA484'] = 4849.2e-4 # Laigle+2016 Table 1
    Filter_Dict['IA505'] = 5062.5e-4 # Laigle+2016 Table 1
    Filter_Dict['IA527'] = 5261.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IA574'] = 5764.8e-4 # Laigle+2016 Table 1
    Filter_Dict['IA624'] = 6233.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IA679'] = 6781.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IA709'] = 7073.6e-4 # Laigle+2016 Table 1
    Filter_Dict['IA738'] = 7361.6e-4 # Laigle+2016 Table 1
    Filter_Dict['IA767'] = 7684.9e-4 # Laigle+2016 Table 1
    Filter_Dict['IA827'] = 8244.5e-4 # Laigle+2016 Table 1
    Filter_Dict['IB427'] = 4263.4e-4 # Laigle+2016 Table 1
    Filter_Dict['IB464'] = 4635.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IB484'] = 4849.2e-4 # Laigle+2016 Table 1
    Filter_Dict['IB505'] = 5062.5e-4 # Laigle+2016 Table 1
    Filter_Dict['IB527'] = 5261.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IB574'] = 5764.8e-4 # Laigle+2016 Table 1
    Filter_Dict['IB624'] = 6233.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IB679'] = 6781.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IB709'] = 7073.6e-4 # Laigle+2016 Table 1
    Filter_Dict['IB738'] = 7361.6e-4 # Laigle+2016 Table 1
    Filter_Dict['IB767'] = 7684.9e-4 # Laigle+2016 Table 1
    Filter_Dict['IB827'] = 8244.5e-4 # Laigle+2016 Table 1
    Filter_Dict['NB711'] = 7119.9e-4 # Laigle+2016 Table 1
    Filter_Dict['NB816'] = 8149.4e-4 # Laigle+2016 Table 1
    Filter_Dict['SPLASH_1'] = 35634.3e-4 # Laigle+2016 Table 1
    Filter_Dict['SPLASH_2'] = 45110.1e-4 # Laigle+2016 Table 1
    Filter_Dict['SPLASH_3'] = 57593.4e-4 # Laigle+2016 Table 1
    Filter_Dict['SPLASH_4'] = 79594.9e-4 # Laigle+2016 Table 1
    Filter_Dict['ch1'] = 35634.3e-4 # Laigle+2016 Table 1
    Filter_Dict['ch2'] = 45110.1e-4 # Laigle+2016 Table 1
    Filter_Dict['ch3'] = 57593.4e-4 # Laigle+2016 Table 1
    Filter_Dict['ch4'] = 79594.9e-4 # Laigle+2016 Table 1
    Filter_Dict['IRAC1'] = 35634.3e-4 # Laigle+2016 Table 1
    Filter_Dict['IRAC2'] = 45110.1e-4 # Laigle+2016 Table 1
    Filter_Dict['IRAC3'] = 57593.4e-4 # Laigle+2016 Table 1
    Filter_Dict['IRAC4'] = 79594.9e-4 # Laigle+2016 Table 1
    if type(input_str) is str:
        if input_str in Filter_Dict:
            return Filter_Dict[input_str]
    return -99


def recognize_Filter(input_str, special_file_name=''):
    Filter_Name = 'unknown_input_str_'+input_str # ''
    Filter_Wave = numpy.nan # um
    if type(input_str) is str:
        # 
        # Check if AB_25, mJy things
        if input_str.endswith('_AB_25'):
            input_str = input_str.replace('_AB_25', '')
        if input_str.endswith('_mJy'):
            input_str = input_str.replace('_mJy', '')
        # 
        # Match filters
        if input_str == 'FLUX_GALEX_NUV' or input_str == 'FLUXERR_GALEX_NUV': 
            Filter_Name = 'GALEX NUV'
            Filter_Wave = 2313.9 * 1e-4 # um, Laigle 2016 Table 1
        # 
        elif input_str.find('_U_KPNO')>=0: 
            Filter_Name = 'KPNO'
            Filter_Wave = 0.3593  # um, Skelton 2014ApJS..214...24S Table 6
        # 
        elif input_str.find('_G_Keck')>=0: 
            Filter_Name = 'Keck LRIS'
            Filter_Wave = 0.4751  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_R_Keck')>=0: 
            Filter_Name = 'Keck LRIS'
            Filter_Wave = 0.6819  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_Rs_Keck')>=0: 
            Filter_Name = 'Keck LRIS'
            Filter_Wave = 0.6819  # um, Skelton 2014ApJS..214...24S Table 6
        # 
        #Pattern_Subaru = re.compile("^([IN][AB])([0-9][0-9][0-9])[^0-9]*")
        #Matched_Subaru = Pattern_Subaru.match(input_str)
        #if Matched_Subaru: 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = float(Matched_Subaru.groups()[1]) * 1e-3 # um
        # 
        #elif input_str.startswith('IA427_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 4263.4e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA464_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 4635.1e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA484_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 4849.2e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA505_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 5062.5e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA527_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 5261.1e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA574_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 5764.8e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA624_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 6233.1e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA679_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 6781.1e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA709_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 7073.6e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA738_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 7361.6e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA767_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 7684.9e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('IA827_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 8244.5e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('NB711_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 7119.9e-4  # um, Laigle 2016 Table 1
        #elif input_str.startswith('NB816_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 8149.4e-4  # um, Laigle 2016 Table 1
        # 
        #elif input_str.startswith('B_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 4458.3 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('V_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 5477.8 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('r_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 6288.7 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('ip_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 7683.9 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('zpp_'): 
        #    Filter_Name = 'Subaru Suprime-Cam'
        #    Filter_Wave = 9105.7 * 1e-4 # um, Laigle 2016 Table 1
        # 
        elif input_str.find('_B_Subaru')>=0: 
            Filter_Name = 'Subaru Suprime-Cam'
            Filter_Wave = 0.4448  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_V_Subaru')>=0: 
            Filter_Name = 'Subaru Suprime-Cam'
            Filter_Wave = 0.5470  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_R_Subaru')>=0: 
            Filter_Name = 'Subaru Suprime-Cam'
            Filter_Wave = 0.6276  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_i_Subaru')>=0: 
            Filter_Name = 'Subaru Suprime-Cam'
            Filter_Wave = 0.7671  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_z_Subaru')>=0: 
            Filter_Name = 'Subaru Suprime-Cam'
            Filter_Wave = 0.9028  # um, Skelton 2014ApJS..214...24S Table 6
        # 
        elif input_str.find('_J_Subaru')>=0: 
            Filter_Name = 'Subaru MOIRCS'
            Filter_Wave = 1.2517  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_H_Subaru')>=0: 
            Filter_Name = 'Subaru MOIRCS'
            Filter_Wave = 1.6347  # um, Skelton 2014ApJS..214...24S Table 6
        elif input_str.find('_Ks_Subaru')>=0: 
            Filter_Name = 'Subaru MOIRCS'
            Filter_Wave = 2.1577  # um, Skelton 2014ApJS..214...24S Table 6
        # 
        #elif input_str.startswith('Y_'): 
        #    Filter_Name = 'VISTA VIRCAM'
        #    Filter_Wave = 10214.2 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('J_'): 
        #    Filter_Name = 'VISTA VIRCAM'
        #    Filter_Wave = 12534.6 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('H_'): 
        #    Filter_Name = 'VISTA VIRCAM'
        #    Filter_Wave = 16453.4 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('Ks_'): 
        #    Filter_Name = 'VISTA VIRCAM'
        #    Filter_Wave = 21539.9 * 1e-4 # um, Laigle 2016 Table 1
        # 
        #elif input_str.startswith('Hw_'): 
        #    Filter_Name = 'CFHT WIRCAM'
        #    Filter_Wave = 16311.4 * 1e-4 # um, Laigle 2016 Table 1
        #elif input_str.startswith('Ksw_'): 
        #    Filter_Name = 'CFHT WIRCAM'
        #    Filter_Wave = 21590.4 * 1e-4 # um, Laigle 2016 Table 1
        # 
        #elif input_str.startswith('u_'): 
        #    Filter_Name = 'CFHT MegaCam'
        #    Filter_Wave = 3823.3 * 1e-4 # um, Laigle 2016 Table 1
        # 
        elif input_str == 'f_u_3DHST':
            Filter_Name = 'KPNO 4m/Mosaic'
            Filter_Wave = 0.35929 # um, Skelton 2014 Table 6
        elif input_str == 'f_b_3DHST':
            Filter_Name = 'Subaru/Suprime-Cam'
            Filter_Wave = 0.44480 # um, Skelton 2014 Table 6
        elif input_str == 'f_v_3DHST':
            Filter_Name = 'Subaru/Suprime-Cam'
            Filter_Wave = 0.54702 # um, Skelton 2014 Table 6
        elif input_str == 'f_g_3DHST':
            Filter_Name = 'Keck/LRIS'
            Filter_Wave = 0.47508 # um, Skelton 2014 Table 6
        elif input_str == 'f_rs_3DHST':
            Filter_Name = 'Keck/LRIS'
            Filter_Wave = 0.68186 # um, Skelton 2014 Table 6
        elif input_str == 'f_r_3DHST':
            Filter_Name = 'Subaru/Suprime-Cam'
            Filter_Wave = 0.62755 # um, Skelton 2014 Table 6
        elif input_str == 'f_i_3DHST':
            Filter_Name = 'Subaru/Suprime-Cam'
            Filter_Wave = 0.76712 # um, Skelton 2014 Table 6
        elif input_str == 'f_z_3DHST':
            Filter_Name = 'Subaru/Suprime-Cam'
            Filter_Wave = 0.90282 # um, Skelton 2014 Table 6
        elif input_str == 'f_f435w_3DHST':
            Filter_Name = 'HST/ACS'
            Filter_Wave = 0.43179 # um, Skelton 2014 Table 6
        elif input_str == 'f_f606w_3DHST':
            Filter_Name = 'HST/ACS'
            Filter_Wave = 0.59194 # um, Skelton 2014 Table 6
        elif input_str == 'f_f775w_3DHST':
            Filter_Name = 'HST/ACS'
            Filter_Wave = 0.76933 # um, Skelton 2014 Table 6
        elif input_str == 'f_f850lp_3DHST':
            Filter_Name = 'HST/ACS'
            Filter_Wave = 0.90364 # um, Skelton 2014 Table 6
        elif input_str == 'f_f125w_3DHST':
            Filter_Name = 'HST/WFC3'
            Filter_Wave = 1.24710 # um, Skelton 2014 Table 6
        elif input_str == 'f_f140w_3DHST':
            Filter_Name = 'HST/WFC3'
            Filter_Wave = 1.39240 # um, Skelton 2014 Table 6
        elif input_str == 'f_f160w_3DHST':
            Filter_Name = 'HST/WFC3'
            Filter_Wave = 1.53960 # um, Skelton 2014 Table 6
        elif input_str == 'f_j_3DHST':
            Filter_Name = 'Subaru/MOIRCS'
            Filter_Wave = 1.25170 # um, Skelton 2014 Table 6
        elif input_str == 'f_h_3DHST':
            Filter_Name = 'Subaru/MOIRCS'
            Filter_Wave = 1.63470 # um, Skelton 2014 Table 6
        elif input_str == 'f_ks_3DHST':
            Filter_Name = 'Subaru/MOIRCS'
            Filter_Wave = 2.15770 # um, Skelton 2014 Table 6   # --- 20171025 for GOODSN 3D-HST catalog (Skelton et al. 2014)
        # 
        #elif input_str == 'f_irac1' or input_str == 'df_irac1' or input_str == 'e_irac1' or input_str == 'fch1' or input_str == 'dfch1' or input_str == '_fch1' or input_str == '_dfch1': 
        #    Filter_Name = 'Spitzer IRAC ch1'
        #    Filter_Wave = 35634.3 * 1e-4 # um
        #elif input_str == 'f_irac2' or input_str == 'df_irac2' or input_str == 'e_irac2' or input_str == 'fch2' or input_str == 'dfch2' or input_str == '_fch2' or input_str == '_dfch2': 
        #    Filter_Name = 'Spitzer IRAC ch2'
        #    Filter_Wave = 45110.1 * 1e-4 # um
        #elif input_str == 'f_irac3' or input_str == 'df_irac3' or input_str == 'e_irac3' or input_str == 'fch3' or input_str == 'dfch3' or input_str == '_fch3' or input_str == '_dfch3': 
        #    Filter_Name = 'Spitzer IRAC ch3'
        #    Filter_Wave = 57593.4 * 1e-4 # um
        #elif input_str == 'f_irac4' or input_str == 'df_irac4' or input_str == 'e_irac4' or input_str == 'fch4' or input_str == 'dfch4' or input_str == '_fch4' or input_str == '_dfch4': 
        #    Filter_Name = 'Spitzer IRAC ch4'
        #    Filter_Wave = 79594.9 * 1e-4 # um
        # 
        #elif input_str == 'SPLASH_1_FLUX' or input_str == 'SPLASH_1_FLUX_ERR' or input_str.startswith('SPLASH_1_FLUX_') or input_str.startswith('SPLASH_1_FLUX_ERR_'): 
        #    Filter_Name = 'Spitzer IRAC ch1'
        #    Filter_Wave = 35634.3 * 1e-4 # um
        #elif input_str == 'SPLASH_2_FLUX' or input_str == 'SPLASH_2_FLUX_ERR' or input_str.startswith('SPLASH_2_FLUX_') or input_str.startswith('SPLASH_2_FLUX_ERR_'): 
        #    Filter_Name = 'Spitzer IRAC ch2'
        #    Filter_Wave = 45110.1 * 1e-4 # um
        #elif input_str == 'SPLASH_3_FLUX' or input_str == 'SPLASH_3_FLUX_ERR' or input_str.startswith('SPLASH_3_FLUX_') or input_str.startswith('SPLASH_3_FLUX_ERR_'): 
        #    Filter_Name = 'Spitzer IRAC ch3'
        #    Filter_Wave = 57593.4 * 1e-4 # um
        #elif input_str == 'SPLASH_4_FLUX' or input_str == 'SPLASH_4_FLUX_ERR' or input_str.startswith('SPLASH_4_FLUX_') or input_str.startswith('SPLASH_4_FLUX_ERR_'): 
        #    Filter_Name = 'Spitzer IRAC ch4'
        #    Filter_Wave = 79594.9 * 1e-4 # um
        # 
        elif input_str == 'FLUX_IRAC1' or input_str == 'FLUXERR_IRAC1' or input_str.startswith('FLUX_IRAC1_') or input_str.startswith('FLUXERR_IRAC1_') or input_str=='fch1' or input_str=='dfch1': 
            Filter_Name = 'Spitzer IRAC ch1'
            Filter_Wave = 35634.3 * 1e-4 # um
        elif input_str == 'FLUX_IRAC2' or input_str == 'FLUXERR_IRAC2' or input_str.startswith('FLUX_IRAC2_') or input_str.startswith('FLUXERR_IRAC2_') or input_str=='fch2' or input_str=='dfch2': 
            Filter_Name = 'Spitzer IRAC ch2'
            Filter_Wave = 45110.1 * 1e-4 # um
        elif input_str == 'FLUX_IRAC3' or input_str == 'FLUXERR_IRAC3' or input_str.startswith('FLUX_IRAC3_') or input_str.startswith('FLUXERR_IRAC3_') or input_str=='fch3' or input_str=='dfch3': 
            Filter_Name = 'Spitzer IRAC ch3'
            Filter_Wave = 57593.4 * 1e-4 # um
        elif input_str == 'FLUX_IRAC4' or input_str == 'FLUXERR_IRAC4' or input_str.startswith('FLUX_IRAC4_') or input_str.startswith('FLUXERR_IRAC4_') or input_str=='fch4' or input_str=='dfch4': 
            Filter_Name = 'Spitzer IRAC ch4'
            Filter_Wave = 79594.9 * 1e-4 # um
        # 
        elif input_str == 'FLUX_MIPS24' or input_str == 'FLUXERR_MIPS24' or input_str == 'f24' or input_str == 'df24' or input_str == 'f_24' or input_str == 'df_24': 
            Filter_Name = 'Spitzer MIPS 24'
            Filter_Wave = 24.0 # um
        # 
        #elif input_str == 'FLUX_24' or input_str == 'FLUXERR_24' or input_str == 'f24' or input_str == 'df24' or input_str == 'f_24' or input_str == 'df_24': 
        #    Filter_Name = 'Spitzer MIPS 24'
        #    Filter_Wave = 24.0 # um
        # 
        #elif input_str == 'FLUX_16' or input_str == 'FLUXERR_16' or input_str == 'f16' or input_str == 'df16' or input_str == 'f_16' or input_str == 'df_16': 
        #    Filter_Name = 'Spitzer IRS PUI 16'
        #    Filter_Wave = 16.0 # um
        # 
        elif input_str == 'FLUX_K' or input_str == 'FLUXERR_K' or input_str == 'fK' or input_str == 'dfK' or input_str == 'f_K' or input_str == 'df_K': 
            Filter_Name = 'unknown K band'
            Filter_Wave = 2.15 # um
        # 
        #elif input_str.startswith('FLUX_K_') or input_str.startswith('FLUXERR_K_') or input_str.startswith('fK_') or input_str.startswith('dfK_') or input_str.startswith('f_K_') or input_str.startswith('df_K_'): 
        #    search_str = re.search(input_str,'.*K_([^_]*).*')
        #    if search_str:
        #        Filter_Name = search_str.group(1)+' K band'
        #    else:
        #        Filter_Name = 'unknown K band'
        #    Filter_Wave = 2.15 # um
        # 
        #elif input_str == 'FLUX_814W' or input_str == 'FLUXERR_814W' \
        #    or input_str.startswith('FLUX_814W_') or input_str.startswith('FLUXERR_814W_'): 
        #    Filter_Name = 'HST ACS F814W'
        #    Filter_Wave = 814.0e-3 # um
        # 
        # 
        if numpy.isnan(Filter_Wave):
            Pattern_FLUX_1 = re.compile("(FLUX_)([0-9Ee.+-]+)([^0-9Ee.+-]*.*)") # e.g., FLUX_20cm
            Pattern_FLUXERR_1 = re.compile("(FLUX[_]?ERR_)([0-9Ee.+-]+)([^0-9Ee.+-]*.*)")
            Pattern_FLUX_2 = re.compile("[^a-zA-Z]*(f[_]?)([0-9Ee.+-]+)([^0-9Ee.+-]*.*)") # e.g., _f1.4ghz
            Pattern_FLUXERR_2 = re.compile("[^a-zA-Z]*(df[_]?)([0-9Ee.+-]+)([^0-9Ee.+-]*.*)")
            Pattern_FLUX_3 = re.compile("(.*)(_FLUX)(_.*)") # e.g. SPLASH_1_FLUX_Laigle
            Pattern_FLUXERR_3 = re.compile("(.*)(_FLUX[_]?ERR)(_.*)")
            Pattern_FLUX_4 = re.compile("[_]?(f_)([^_]+)(.*)") # e.g., f_K_Jin
            Pattern_FLUXERR_4 = re.compile("[_]?(df_)([^_]+)(.*)") # 
            Matched_FLUX_1 = Pattern_FLUX_1.match(input_str)
            Matched_FLUXERR_1 = Pattern_FLUXERR_1.match(input_str)
            Matched_FLUX_2 = Pattern_FLUX_2.match(input_str)
            Matched_FLUXERR_2 = Pattern_FLUXERR_2.match(input_str)
            Matched_FLUX_3 = Pattern_FLUX_3.match(input_str)
            Matched_FLUXERR_3 = Pattern_FLUXERR_3.match(input_str)
            Matched_FLUX_4 = Pattern_FLUX_4.match(input_str)
            Matched_FLUXERR_4 = Pattern_FLUXERR_4.match(input_str)
            Matched = None
            if Matched is None:
                if Matched_FLUX_1:
                    Matched = Matched_FLUX_1
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUXERR_1:
                    Matched = Matched_FLUXERR_1
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUX_2:
                    Matched = Matched_FLUX_2
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUXERR_2:
                    Matched = Matched_FLUXERR_2
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUX_3:
                    Matched = Matched_FLUX_3
                    Matched_str_2 = Matched.group(1)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUXERR_3:
                    Matched = Matched_FLUXERR_3
                    Matched_str_2 = Matched.group(1)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUX_4:
                    Matched = Matched_FLUX_4
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched is None:
                if Matched_FLUXERR_4:
                    Matched = Matched_FLUXERR_4
                    Matched_str_2 = Matched.group(2)
                    Matched_str_3 = Matched.group(3)
            if Matched: 
                #print('Matched_str_2 '+Matched_str_2)
                #print('Matched_str_3 '+Matched_str_3)
                try:
                    Filter_Name = 'unknown'
                    Filter_Wave = float(Matched_str_2)
                    # if matched the pattern 'FLUX_wavelength'
                    # try to convert Filter_Wave unit
                    if Matched_str_3.lower() == 'cm' or Matched_str_3.lower().startswith('cm_'):
                        Filter_Wave = Filter_Wave * 1e4 # convert from cm to um
                        if Matched_str_2 == '20':
                            Filter_Name = 'VLA 1.4 GHz'
                        elif Matched_str_2 == '10':
                            Filter_Name = 'VLA 3 GHz'
                        Matched_str_3 = Matched_str_3[2:]
                    elif Matched_str_3.lower() == 'ghz' or Matched_str_3.lower().startswith('ghz_'):
                        Filter_Wave = 2.99792458e5 / Filter_Wave # convert from GHz to um
                        if Matched_str_2 == '1.4':
                            Filter_Name = 'VLA 1.4 GHz'
                        elif Matched_str_2 == '3':
                            Filter_Name = 'VLA 3 GHz'
                        Matched_str_3 = Matched_str_3[3:]
                    else:
                        if not Matched_str_3.lower().startswith('_') and not Matched_str_3=='':
                            Filter_Wave = -99
                            Filter_Name = 'unknown wavelength ' + Matched_str_2 # failed to determine a valid wavelength from the input_str
                    #elif Matched_str_3.upper() == 'W' or Matched_str_3.upper().startswith('W_'):
                    #    Filter_Wave = Filter_Wave / 1e4 # convert from AA to um, e.g. F814W
                    # try to guess Filter_Name
                    if Matched_str_3.upper().find('ALMA')>=0:
                        Filter_Name = 'ALMA'
                    elif Matched_str_3.upper().find('SCUBA2')>=0:
                        Filter_Name = 'JCMT SCUBA2'
                    elif Matched_str_3.upper().find('JCMT')>=0 and Matched_str_3.upper().find('AZTEC')>=0:
                        Filter_Name = 'JCMT AzTEC'
                    elif Matched_str_3.upper().find('MAMBO')>=0:
                        Filter_Name = 'IRAM 30m MAMBO'
                    #if Matched_str_2 == '814' and Matched_str_3.startswith('W'):
                    #    Filter_Name = 'HST F814W'
                    #    Matched_str_3 = Matched_str_3[1:]
                    if Matched_str_3 == '' or Matched_str_3.startswith('_'):
                        if Matched_str_2 =='16':
                            Filter_Name = 'Spitzer IRS PUI'
                        elif Matched_str_2 =='24':
                            Filter_Name = 'Spitzer MIPS'
                        elif Matched_str_2 =='70':
                            Filter_Name = 'Herschel PACS'
                        elif Matched_str_2 =='100':
                            Filter_Name = 'Herschel PACS'
                        elif Matched_str_2 =='160':
                            Filter_Name = 'Herschel PACS'
                        elif Matched_str_2 =='250':
                            Filter_Name = 'Herschel SPIRE'
                        elif Matched_str_2 =='350':
                            Filter_Name = 'Herschel SPIRE'
                        elif Matched_str_2 =='500':
                            Filter_Name = 'Herschel SPIRE'
                        elif Matched_str_2 =='850':
                            Filter_Name = 'JCMT SCUBA2'
                        elif Matched_str_2 =='1100':
                            Filter_Name = 'JCMT AzTEC'
                        elif Matched_str_2 =='1200':
                            Filter_Name = 'IRAM 30m MAMBO'
                        elif Matched_str_2 =='1200':
                            Filter_Name = 'IRAM 30m MAMBO'
                        elif Matched_str_2 =='123456':
                            Filter_Name = 'Test Filter Name'
                    Filter_Name = Filter_Name + Matched_str_3
                except:
                    # if matched the pattern 'FLUX_band_name'
                    #print('recognize_Filter_Instrument_by_Short_Name '+Matched_str_2)
                    Filter_Name = recognize_Filter_Instrument_by_Short_Name(Matched_str_2, Matched_str_3)
                    Filter_Wave = recognize_Filter_Wavelength_by_Short_Name(Matched_str_2)
                    Filter_Name = Filter_Name + Matched_str_3
    # 
    #if special_file_name.find('Laigle')>=0:
    #    Filter_Name = Filter_Name + ' (Laigle)'
    # 
    return Filter_Name, Filter_Wave









##########################################
#               MAIN PROGRAM             #
##########################################

if len(sys.argv) <= 1:
    
    print('Usage: michi2_extract_flux_from_data_table.py catalog_input.fits 23434')
    sys.exit()


# Read input args
DataFile = ''
SourceID_Inputs = []
MaxSNR = numpy.nan
CatID = numpy.nan
i = 0
while i <= (len(sys.argv)-1):
    if i >= 1:
        if not sys.argv[i].startswith('-'):
            if DataFile == '':
                DataFile = sys.argv[i]
            else:
                SourceID_Inputs.append(sys.argv[i])
        elif sys.argv[i].upper() == '-MAXSNR':
            i = i + 1
            if i <= (len(sys.argv)-1) and numpy.isnan(MaxSNR):
                MaxSNR = float(sys.argv[i])
                print('# Setting max SNR limit to %s'%(MaxSNR))
        elif sys.argv[i].upper() == '-CATID':
            i = i + 1
            if i <= (len(sys.argv)-1) and numpy.isnan(CatID):
                CatID = int(sys.argv[i])
                print('# Setting catalog ID to %s'%(CatID)) # if set, then we will append "_from_cat_%d" to the output file name.
    i = i + 1


# Read data file
if DataFile != '':
    DataFile = sys.argv[1]
    print('# Reading "%s"'%(DataFile))
    DataTable = CrabTable(DataFile, verbose=0)
    
    Col_Source  = recognize_Col_Source(DataTable.getColumnNames(), special_file_name=DataFile)
    Col_ID      = recognize_Col_ID(DataTable.getColumnNames(), special_file_name=DataFile)
    Col_FLUX    = recognize_Col_FLUX(DataTable.getColumnNames(), special_file_name=DataFile)
    Col_FLUXERR = recognize_Col_FLUXERR(DataTable.getColumnNames(), special_file_name=DataFile)
    
    # special treatment
    
    if 1 == 1:
        print('# Col_Source = %s'%Col_Source)
        print('# Col_ID = %s'%Col_ID)
        print('# Col_FLUX = %s'%Col_FLUX)
        print('# Col_FLUXERR = %s'%Col_FLUXERR)
    
    if Col_Source:
        if Col_ID:
            #<BUGGY># Col_Source = Col_Source.extend(Col_ID)
            Col_Source.extend(Col_ID)
    else:
        if Col_ID:
            Col_Source = Col_ID
    
    if Col_Source is None:
        print('******************************************************************************')
        print('Error! Could not determine Source or ID columns in the input catalog!')
        print('Column names: %s'%(DataTable.getColumnNames()))
        print('Col_Source = %s'%Col_Source)
        print('Col_ID = %s'%Col_ID)
        print('Col_FLUX = %s'%Col_FLUX)
        print('Col_FLUXERR = %s'%Col_FLUXERR)
        sys.exit()
    
    if len(Col_FLUX) != len(Col_FLUXERR):
        print('******************************************************************************')
        print('Error! FLUX columns and FLUXERR columns do not match in dimension! Please check the input catalog!')
        for k in range(max(len(Col_FLUX),len(Col_FLUXERR))):
            if k < len(Col_FLUX) and k < len(Col_FLUXERR):
                print('        %-30s %-30s'%(Col_FLUX[k], Col_FLUXERR[k]))
            elif k < len(Col_FLUX):
                print('        %-30s %-30s'%(Col_FLUX[k], ' '))
            elif k < len(Col_FLUXERR):
                print('        %-30s %-30s'%(' ', Col_FLUXERR[k]))
        sys.exit()
    
    SourceID_Matchs = [] # an array of dict
    
    if len(SourceID_Inputs) > 0:
        
        for SourceID_Input in SourceID_Inputs:
            print('# Finding source by the input name or id "%s"'%(SourceID_Input))
            # 
            # check the SourceID_Input type (dict or str)
            if SourceID_Input.startswith('{') and SourceID_Input.endswith('}'):
                #print(SourceID_Input) # something like {'ID_Laigle':12345}
                SourceID_Dict = json.loads(SourceID_Input.replace("'",'"')) # json only accepts double quotes
                #print(SourceID_Dict)
            else:
                SourceID_Dict = {}
                for icol in Col_Source:
                    SourceID_Dict[icol] = SourceID_Input
                #print(SourceID_Dict)
            # 
            # loop SOURCE Table Headers and match SourceID_Input
            SourceID_Match = []
            for icol in Col_Source:
                if icol in SourceID_Dict:
                    SourceID_Where = numpy.argwhere(DataTable.getColumn(icol).astype(str) == str(SourceID_Dict[icol])).T # do a transpose to numpy.argwhere(), see http://stackoverflow.com/questions/33747908/output-of-numpy-wherecondition-is-not-an-array-but-a-tuple-of-arrays-why
                    if len(SourceID_Where) > 0:
                        SourceID_Where = SourceID_Where[0]
                        if len(SourceID_Match) > 0:
                            SourceID_Match = numpy.intersect1d(SourceID_Match, SourceID_Where) # solve multiplicity <TODO>
                        else:
                            SourceID_Match = SourceID_Where
                    #print SourceID_Where
                    #print SourceID_Match
            # 
            # check whether we found any source according to the input SourceID_Input
            if len(SourceID_Match) == 0:
                print('***********')
                print('# Warning! Could not find source according to the input name or id "%s"!'%(SourceID_Input))
                print('***********')
                # do not append anything if the source was not found.
            else:
                SourceID_Dict['row'] = SourceID_Match[0]
                SourceID_Dict['source id input'] = SourceID_Input
                for icol in Col_Source:
                    SourceID_Dict[icol] = DataTable.getColumn(icol)[SourceID_Dict['row']]
                SourceID_Matchs.append(SourceID_Dict)
        
    else:
        
        # if no SourceID_Input is given by the user, we will output flux for each object
        for irow in range(DataTable.getRowNumber()):
            SourceID_Dict = {}
            SourceID_Dict['row'] = irow
            SourceID_Dict['source id input'] = 'at_row_%d'%(irow+1)
            for icol in Col_Source:
                SourceID_Dict[icol] = DataTable.getColumn(icol)[SourceID_Dict['row']]
            SourceID_Matchs.append(SourceID_Dict)
        
        print('# Getting all %d sources in the data table'%(len(SourceID_Matchs)))
    
    print('')
    
    # 
    # found Source matched by SourceID_Input
    # 
    for j in range(len(SourceID_Matchs)):
        #print("# -------------------------------------------------")
        print("# Matched source \"%s\"."%(SourceID_Matchs[j]))
        
        # prepare SED data structure
        SED = []
        
        # loop SOURCE Table Headers and print
        #for k in range(len(Col_Source)):
        #    if Col_Source[k] in SourceID_Dict:
        #        print('# Matched with column "%s" row %d "%s"'%(str(Col_Source[k]), SourceID_Matchs[j]['row'], DataTable.getColumn(str(Col_Source[k]))[SourceID_Matchs[j]['row']]))
        
        # loop SED Data Array and convert flux
        for k in range(len(Col_FLUX)):
            FilterHead = Col_FLUX[k]
            #print('Debug', 'recognize_Filter', Col_FLUX[k], 'special_file_name='+DataFile)
            FilterName, FilterWave = recognize_Filter(Col_FLUX[k], special_file_name=DataFile)
            FilterFlux = DataTable.getColumn(Col_FLUX[k])[SourceID_Matchs[j]['row']]
            FilterFluxErr = DataTable.getColumn(Col_FLUXERR[k])[SourceID_Matchs[j]['row']]
            FilterType = 'FLUX'
            FilterFluxUnit = 'mJy'
            FilterWaveUnit = 'um'
            # 
            TempColumn = DataTable.TableColumns[DataTable.getColumnIndex(Col_FLUX[k])]
            if type(TempColumn) is astropy.io.fits.column.Column:
                if type(TempColumn.unit) is str:
                    #print(TempColumn.unit)
                    if TempColumn.unit != '':
                        FilterFluxUnit = TempColumn.unit
            # 
            if FilterFluxUnit == 'uJy':
                FilterFlux = FilterFlux / 1e3
                FilterFluxErr = FilterFluxErr / 1e3
                FilterFluxUnit = 'mJy'
            
            # 
            #if FilterType == 'MAG AB':
            #    FilterFlux = math.pow(10, (float(FilterFlux)/(-2.5))) * 3630.7805 * 1e3 # AB magnitude to mJy, https://en.wikipedia.org/wiki/AB_magnitude
            #    FilterFluxUnit = 'mJy'
            #    FilterType = 'FLUX mJy'
            #elif FilterType == 'FLUX uJy':
            #    FilterFlux = FilterFlux * 1e-3 # mJy
            #    FilterFluxUnit = 'mJy'
            #    FilterType = 'FLUX mJy'
            #
            #elif FilterType == 'FLUX AB 25':
            #    FilterFlux = FilterFlux / 10**3.44 # mJy
            #    FilterFluxUnit = 'mJy'
            #    FilterType = 'FLUX mJy'
            #    # magAB = 25.0-2.5*log10(flux) = 8.90-2.5*log10(f_Jy) = 8.90+2.5*3-2.5*log10(f_mJy) = 16.4-2.5*log10(f_mJy)
            #    # so 8.60-2.5*log10(flux) = -2.5*log10(f_mJy)
            #    # so 3.44-log10(flux) = -log10(f_mJy)
            #    # so f_mJy = flux/10**3.44 = flux / 2754.228703
            # 
            # 
            SED_k = {}
            SED_k['Head'] = FilterHead
            SED_k['Filter'] = FilterName
            SED_k['Wave'] = FilterWave
            SED_k['WaveUnit'] = FilterWaveUnit
            SED_k['Flux'] = FilterFlux
            SED_k['FluxErr'] = FilterFluxErr
            SED_k['FluxUnit'] = FilterFluxUnit
            SED_k['Type'] = FilterType
            SED.append(SED_k)
            #print("# Getting Column %-20s Wave %-15.6e Flux %-15.6e FluxUnit %s"%(FilterHead, FilterWave, FilterFlux, FilterFluxUnit))
        
        # sort SED
        SED_unsorted = SED
        SED_sorted = sorted(SED, key=lambda k: float('-inf') if math.isnan(k['Wave']) else k['Wave']) # sort function breaks in the presence of nan, see http://stackoverflow.com/questions/4240050/python-sort-function-breaks-in-the-presence-of-nan
        SED = SED_sorted
        
        # loop SED (sorted) and output to file
        out_name = 'extracted_flux'
        out_name_for_obj = 'extracted_flux_for_obj_%s'%(re.sub(r'\W+', ' ', SourceID_Matchs[j]['source id input']).strip().replace(' ','_'))
        if not numpy.isnan(CatID):
            out_name_for_obj = out_name_for_obj + '_from_cat_%d'%(CatID)
        fout = out_name+'.txt'
        fout_obj = out_name_for_obj+'.txt'
        fout_info = out_name+'.info'
        fout_info_obj = out_name_for_obj+'.info'
        with open(fout_info,'w') as fp:
            fp.write('cat = "%s"  # the input catalog name\n'%(DataFile))
            fp.write('row = %d  # index starting from 0\n'%(SourceID_Matchs[j]['row']))
            for icol in Col_Source:
                fp.write('%s = %s\n'%(icol, SourceID_Matchs[j][icol]))
            fp.close()
        # 
        with open(fout,'w') as fp:
            for k in range(len(SED)):
                FilterName = str(SED[k]['Filter'])
                FilterWave = float(SED[k]['Wave'])
                FilterFlux = float(SED[k]['Flux'])
                FilterFErr = float(SED[k]['FluxErr'])
                FilterFluxUnit = str(SED[k]['FluxUnit'])
                # MaxSNR (20180111)
                if MaxSNR > 0:
                    if (FilterFErr>0) and (FilterFlux>MaxSNR*FilterFErr):
                        FilterFErr = FilterFlux/MaxSNR
                # print
                if k == 0:
                    print("# %-20s %-18s %-18s %-12s %-s"%('Wave', 'Flux', 'FluxErr', 'FluxUnit', 'FilterName'))
                    fp.write("# %-20s %-18s %-18s %-12s %-s\n"%('Wave', 'Flux', 'FluxErr', 'FluxUnit', 'FilterName'))
                #<20180110># if FilterWave > 0 and FilterFlux > 0 and FilterFErr > 0
                if FilterFlux > 0 and FilterFErr > 0:
                    #print("                 %-20s Wave %-15.6e Flux %-15.6e FluxError %-15.6e FluxUnit %s"%(FilterName, FilterWave, FilterFlux, FilterFErr, FilterFluxUnit))
                    print("  %-20.8g %-18.8g %-18.8g %-12s %-s"%(FilterWave, FilterFlux, FilterFErr, FilterFluxUnit, FilterName.replace(' ','_')))
                    fp.write("  %-20.8g %-18.8g %-18.8g %-12s %-s\n"%(FilterWave, FilterFlux, FilterFErr, FilterFluxUnit, FilterName.replace(' ','_')))
            fp.close()
        # 
        os.system('cp "%s" "%s"'%(fout, fout_obj))
        os.system('cp "%s" "%s"'%(fout_info, fout_info_obj))
        print('Output to "%s"!'%(fout))
        print('Output to "%s"!'%(fout_info))
        print('Output to "%s"!'%(fout_obj))
        print('Output to "%s"!'%(fout_info_obj))
        print('')
        # 
        #break












