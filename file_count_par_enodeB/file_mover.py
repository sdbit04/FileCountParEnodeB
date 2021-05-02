import os
import shutil
import traceback
import time
import pathlib


class FileMover(object):

    def __init__(self, current_input_directory_path, current_base_dir_name, inside_files, out_dir_path, result_locatoin, log_path):
        self.current_in_dir_path = current_input_directory_path
        self.out_dir_path = out_dir_path
        self.inside_files = inside_files
        self.current_base_dir_name = current_base_dir_name
        self.current_out_dir_path = os.path.join(self.out_dir_path, self.current_base_dir_name)
        self.result_location = result_locatoin
        self.log_path = log_path
        try:
            os.mkdir(self.current_out_dir_path)
        except FileExistsError:
            with open(self.log_path, 'a') as log_file:
                print("current_out directory {} is there".format(current_base_dir_name), file=log_file)

    def move_file(self, file_name):
        input_file_path = os.path.realpath(os.path.join(self.current_in_dir_path, file_name))
        out_file_path = os.path.realpath(os.path.join(self.current_out_dir_path, file_name))
        try:
            shutil.move(input_file_path, out_file_path)
        except FileNotFoundError:
            with open(self.log_path, 'a') as log_file:
                print("Out directory is there, File was not available to move to out directory", file=log_file)
            # By the time I made the out dir, the file from input may get deleted, so this excpt may happen
            pass

    def move_files_under_a_dir(self):
        """This method will be called once we have got a directory-path and the list of its containing files,
        we can use os.walk() to get these input.
        It takes following arguments from its object:
        self.current_in_dir_path
        self.inside_files
        self.current_out_dir_path
        """
        # corresponding_out_dir = os.path.join(self.out_dir_path, current_base_dir)
        try:
            os.mkdir(os.path.realpath(self.out_dir_path))
        except FileExistsError:
            pass
        try:
            os.mkdir(self.result_location)
        except FileExistsError:
            pass

        try:
            with open(os.path.join(self.result_location, self.current_base_dir_name), 'a') as list_file:
                print("Moving and listing files of {} directory ".format(self.current_base_dir_name))
                for file_name in self.inside_files:
                    list_file.write(file_name + "\n")
                    try:
                        self.move_file(file_name)
                    except FileNotFoundError:
                        #TODO need to improve this block
                        print("Got exception during moving file")
                        print(traceback.print_exc())

        except FileNotFoundError:
            print("Got exception in append mode block")
            with open(os.path.join(self.result_location, self.current_base_dir_name), 'w') as list_file:
                print("Moving and listing files of {} directory ".format(self.current_base_dir_name))
                for file_name in self.inside_files:
                    list_file.write(file_name + "\n")
                    try:
                        self.move_file(file_name)
                    except FileNotFoundError:
                        print("Got exception during moving file")
                        print(traceback.print_exc())
