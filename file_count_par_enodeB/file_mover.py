import os
import shutil


class FileMover(object):

    def __init__(self, input_directory_path, out_dir_path):
        self.in_dir_path = input_directory_path
        self.out_dir_path = out_dir_path

    def move_files(self, file_list):
        for file_name in file_list:
            input_file_path = os.path.join(self.in_dir_path, file_name)
            out_file_path = os.path.join(self.out_dir_path, file_name)
            try:
                shutil.move(input_file_path, out_file_path)
            except FileNotFoundError:
                os.mkdir(self.out_dir_path)
                shutil.move(input_file_path, out_file_path)

