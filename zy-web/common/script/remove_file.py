import os

FILE_DIR = '/usr/xiaowan/www/jsp_download'


def remove_file():
    file_list = os.listdir(FILE_DIR)
    for file in file_list:
        filepath = os.path.join(FILE_DIR, file)
        if os.path.isfile(filepath):
            os.remove(filepath)
    print "success"


if __name__ == '__main__':
    remove_file()
