import os
import re
import pdb
from file_count_par_enodeB.file_mover import FileMover


class FileLister(object):

    result_location = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ListOfFiles")

    def __init__(self, file_pattern, in_directory_path, out_dir_path):
        self.f_pattern = file_pattern
        self.f_dir_path = os.path.realpath(in_directory_path)
        self.f_out_path = os.path.realpath(out_dir_path)
        self.file_mover = FileMover(self.f_dir_path, self.f_out_path)

    def list_files(self):
        file_list = os.listdir(self.f_dir_path)
        pdb.set_trace()
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


if __name__ == "__main__":
    file_lister = FileLister('*', "D:\D_drive_BACKUP\MENTOR\yubaraj\Rename_sig\input", "D:\D_drive_BACKUP\MENTOR\yubaraj\Rename_sig\out")
    file_lister.list_files()



