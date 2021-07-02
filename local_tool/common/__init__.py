import os
import sys
pwd_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(pwd_path)
sys.path.append(parent_path)
packages_path = parent_path+'/packages'
sys.path.append(packages_path)
