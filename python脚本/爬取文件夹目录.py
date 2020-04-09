#coding=utf-8
import os

def all_path(dirname):
    filelistlog = dirname + "\\filelistlog.txt"  # 保存文件路径
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if True:  # 保存全部文件名。
                try:
                    with open(filelistlog, 'a+') as fo:
                        fo.writelines(apath)
                        fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


if __name__ == '__main__':
    dirpath = "E:\phpStudy\PHPTutorial\WWW\phpcms"  # 指定根目录
    all_path(dirpath)
