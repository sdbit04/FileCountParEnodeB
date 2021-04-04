from threading import Thread
import os
import pdb
from file_count_par_enodeB.file_mover import FileMover
import traceback


class FileLister(object):

    def __init__(self, file_pattern, in_directory_path, out_dir_path):
        self.provided_f_pattern = file_pattern
        self.provided_in_dir_path = os.path.realpath(in_directory_path)
        self.provided_out_dir_path = os.path.realpath(out_dir_path)
        try:
            os.mkdir(self.provided_out_dir_path)
        except FileExistsError:
            print("Out directory already exist, so proceeding")

        """self.file_mover = FileMover(self.f_dir_path, self.f_out_path)

    def list_files(self):
        file_list = os.listdir(self.f_dir_path)
        # pdb.set_trace()
        try:
            os.mkdir(self.result_location)
        except FileExistsError:
            pass
        try:
            with open(os.path.join(self.result_location, os.path.basename(self.f_dir_path)), 'a') as list_file:
                for file_name in file_list:
                    list_file.write(file_name+"\n")
            self.file_mover.move_files(file_list)

        except FileNotFoundError:
            with open(os.path.join(self.result_location, os.path.basename(self.f_dir_path)), 'w') as list_file:
                for file_name in file_list:
                    list_file.write(file_name+"\n")
            self.file_mover.move_files(file_list)
        """

    def list_files_n_move_mlt(self):
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
                file_mover = FileMover(dir, inside_files, self.provided_out_dir_path)
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
    file_lister = FileLister('*', input_dir, output_dir)
    file_lister.list_files_n_move_mlt()

