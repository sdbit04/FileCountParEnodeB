from file_count_par_enodeB.file_mover import FileMover
import os
import time
import pathlib


def move_files_under_a_dir_mt(current_in_dir_path, current_base_dir_name, inside_files, current_out_dir_path, result_location):
    """This method will be called once we have got a directory-path and the list of its containing files,
    we can use os.walk() to get these input.
    It takes following arguments from its object:
    self.current_in_dir_path
    self.inside_files
    self.current_out_dir_path
    """

    try:
        with open(os.path.join(result_location, current_base_dir_name), 'a') as list_file:
            for file_name in inside_files:
                list_file.write(file_name + "\n")
                # try:
                #     self.move_file(file_name)
                # except FileNotFoundError:
                #     #TODO need to improve this block
                #     print("Got exception during moving file")
                #     print(traceback.print_exc())

    except FileNotFoundError:
        print("Got exception in append mode block")
        with open(os.path.join(result_location, current_base_dir_name), 'w') as list_file:
            for file_name in inside_files:
                list_file.write(file_name + "\n")
                # try:
                #     self.move_file(file_name)
                # except FileNotFoundError:
                #     print("Got exception during moving file")
                #     print(traceback.print_exc())

    file_count_in_current_dir = len(inside_files)
    max_single_file_mover_thread = 10
    if file_count_in_current_dir < (max_single_file_mover_thread *30):
        number_of_mover = file_count_in_current_dir // 10

        pass

    else:
        number_of_mover = file_count_in_current_dir










