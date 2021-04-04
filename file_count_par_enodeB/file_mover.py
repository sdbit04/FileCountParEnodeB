import os
import shutil
import traceback
import time
import pathlib


class FileMover(object):

    daily_stat_directory = time.strftime("%d-%m-%Y", time.localtime())
    result_location = pathlib.Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), "ListOfFiles", daily_stat_directory))
    result_location.mkdir(parents=True, exist_ok=True)

    def __init__(self, current_input_directory_path, inside_files, out_dir_path):
        self.current_in_dir_path = current_input_directory_path
        self.out_dir_path = out_dir_path
        self.inside_files = inside_files
        self.current_base_dir_name = os.path.basename(self.current_in_dir_path)
        self.current_out_dir_path = os.path.join(self.out_dir_path, self.current_base_dir_name)

    def move_file(self, file_name):
        input_file_path = os.path.realpath(os.path.join(self.current_in_dir_path, file_name))
        out_file_path = os.path.realpath(os.path.join(self.current_out_dir_path, file_name))
        try:
            shutil.move(input_file_path, out_file_path)
        except FileNotFoundError:
            try:
                os.mkdir(self.current_out_dir_path)
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

    def move_files_under_a_dir(self):
        """This method will be called once we have got a directory-path and the list of its containing files,
        we can use os.walk() to get these input.
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
                for file_name in self.inside_files:
                    list_file.write(file_name + "\n")
                    try:
                        self.move_file(file_name)
                    except FileNotFoundError:
                        print("Got exception during moving file")
                        print(traceback.print_exc())

