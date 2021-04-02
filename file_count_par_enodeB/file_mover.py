import os
import shutil


class FileMover(object):

    def __init__(self, input_directory_path, out_dir_path):
        self.in_dir_path = input_directory_path
        self.out_dir_path = out_dir_path
    """
    def move_files(self, file_list):
        for file_name in file_list:
            input_file_path = os.path.join(self.in_dir_path, file_name)
            out_file_path = os.path.join(self.out_dir_path, file_name)
            try:
                shutil.move(input_file_path, out_file_path)
            except FileNotFoundError:
                os.mkdir(self.out_dir_path)
                shutil.move(input_file_path, out_file_path)
    """

    def move_file(self, file_name):
        input_file_path = os.path.realpath(os.path.join(self.in_dir_path, file_name))
        out_file_path = os.path.realpath(os.path.join(self.out_dir_path, file_name))
        try:
            shutil.move(input_file_path, out_file_path)
        except FileNotFoundError:
            try:
                os.mkdir(self.out_dir_path)
            except FileExistsError:
                print("Out directory is there, File was not available to move to out directory")
                pass
            else:
                print("Out directory created, retrying to move the file to out directory")
                try:
                    shutil.move(input_file_path, out_file_path)
                except FileNotFoundError:
                    # By the time I made the out dir, the file from input may get deleted, so this excpt may happen
                    print("Out directory is there, File was not available to move to out directory")
                    pass


