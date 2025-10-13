import os

source_path = os.getcwd() ###[1]


o = ["/temp.txt","/TEMP.txt"]
pointless_file = source_path + o[0]
new_file = source_path + o[1]
os.rename(pointless_file, new_file) ###[2]


'''
[1] - geeksforgeeks <https://www.geeksforgeeks.org/python/get-current-directory-python/> Accessed on 10/10/2025
[2] - w3schools <https://www.w3schools.com/python/ref_os_rename.asp> Accessed on 10/10/2025
'''