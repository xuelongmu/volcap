import glob, os
from pathlib import Path
# for file in os.listdir("../mvrig3"):
#     if file.endswith(".raw"):
#         print("1")
#         print(os.path.join("../mvrig3", file))

# usage: file, path = splitPath(s)
# def splitPath(s):
#     f = os.path.basename(s)
#     p = s[:-(len(f))-1]
#     return f, p

# os.chdir("../mvrig3/16375702")
# for filename in glob.glob("*.raw"):
for file in Path('../mvrig3/').glob('**/*.raw'): # /media/xuelong/xue-intel-2/Colmap_Projects/samsung_volcap
    filepath = str(file)
    # print(str(filename))
    filepath_list = str(filepath).split('/') #[0:-1]
    print(filepath_list)
    filename = filepath_list[3].split('.')[0]
    print(filename)
    dirname = filepath_list[2]
    print(dirname)
    # file, path = splitPath(filename)
    # print('{} {}'.format(file, path))
