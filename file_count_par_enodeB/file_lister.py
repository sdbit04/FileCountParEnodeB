from threading import Thread
import os
import pdb
from file_count_par_enodeB.file_mover import FileMover
import traceback
import time
import pathlib


class FileLister(object):

    def __init__(self, file_pattern, in_directory_path, out_dir_path, current_dir, date_dir):
        self.provided_f_pattern = file_pattern
        self.provided_in_dir_path = os.path.realpath(in_directory_path)
        self.provided_out_dir_path = os.path.realpath(out_dir_path)
        self.daily_stat_directory = date_dir
        self.current_dir = current_dir


        self.result_location = pathlib.Path(
            os.path.join(self.current_dir, "ListOfFiles", self.daily_stat_directory))
        self.result_location.mkdir(parents=True, exist_ok=True)
        self.log_dir = pathlib.Path(self.current_dir, 'Logs')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, "{}.log".format(self.daily_stat_directory))
        try:
            with open(self.log_path, 'a') as log_file:
                print("Start generation of stat files for, Daily directory {}".format(self.daily_stat_directory), file=log_file)
        except FileNotFoundError:
            with open(self.log_path, 'w') as log_file:
                print("Start generation of stat files for, Daily directory {}".format(self.daily_stat_directory), file=log_file)
        try:
            os.mkdir(self.provided_out_dir_path)
        except FileExistsError:
            with open(self.log_path, 'a') as log_file:
                print("Out directory already exist, so proceeding", file=log_file)

    def list_files_n_move_mlt(self):
        dir_vs_its_file_list = {}
        for current_in_dir, dirs, files in os.walk(self.provided_in_dir_path):
            if len(files) > 0:
                dir_vs_its_file_list[current_in_dir] = files
            else:
                print("No file under directory {}".format(current_in_dir))

        thread_count = 0
        thread_list = []
        try:
            for dir, inside_files in dir_vs_its_file_list.items():
                #TODO create a thread for each directory. to run move_files_under_a_dir()
                current_base_dir_name = os.path.basename(dir)
                thread_count += 1
                # One file mover object for each directory
                file_mover = FileMover(dir, current_base_dir_name, inside_files, self.provided_out_dir_path, self.result_location, self.log_path)
                thread_list.insert(thread_count, Thread(target=file_mover.move_files_under_a_dir, name=current_base_dir_name))

            for thread in thread_list:
                with open(self.log_path, 'a') as log_file:
                    print("Starting thread for {}".format(thread.getName()), file=log_file)
                thread.start()

            for thread in thread_list:
                thread.join()
        except Exception:
            with open(self.log_path, 'a') as log_file:
                print("Exception caught in high level inside any thread", file=log_file)
        else:
            print("Process of stat generation and file moving is done")

    def list_files_n_move_mlt_mlt(self):
        """NOt yet in use
        """
        dir_vs_its_file_list = {}
        for current_in_dir, dirs, files in os.walk(self.provided_in_dir_path):
            if len(files) > 0:
                dir_vs_its_file_list[current_in_dir]=files
            else:
                print("No file under directory {}".format(current_in_dir))

        thread_count = 0
        thread_list = []
        try:
            for dir, inside_files in dir_vs_its_file_list.items():
                #TODO create a thread for each directory. to run move_files_under_a_dir()
                thread_count += 1
                # One file mover object for each directory
                file_mover = FileMover(dir, inside_files, self.provided_out_dir_path, self.result_location)
                thread_list.insert(thread_count, Thread(target=file_mover.move_files_under_a_dir))

            for thread in thread_list:
                print("Starting thread {}".format(thread.getName()))
                thread.start()

            for thread in thread_list:
                thread.join()
        except Exception:
            print("Exception caught in high level inside any thread")
        else:
            print("Process of stat generation and file moving is done")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir_path")
    parser.add_argument("output_dir_path")
    args = parser.parse_args()
    input_dir = args.input_dir_path
    output_dir = args.output_dir_path
    current_directory = os.path.dirname(os.path.dirname(__file__))
    daily_stat_directory = time.strftime("%d-%m-%Y", time.localtime())
    file_lister = FileLister('*', input_dir, output_dir, current_directory,daily_stat_directory)
    file_lister.list_files_n_move_mlt()
