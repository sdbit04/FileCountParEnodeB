import os
import pdb
from file_count_par_enodeB.file_mover import FileMover
import traceback


class FileLister(object):

    result_location = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ListOfFiles")

    def __init__(self, file_pattern, in_directory_path, out_dir_path):
        self.provided_f_pattern = file_pattern
        self.provided_in_dir_path = os.path.realpath(in_directory_path)
        self.provided_out_dir_path = os.path.realpath(out_dir_path)

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

    def list_files_n_move(self):
        for current_in_dir, dirs, files in os.walk(self.provided_in_dir_path):
            if len(files) > 0:
                current_base_dir = os.path.basename(current_in_dir)
                corresponding_out_dir = os.path.join(self.provided_out_dir_path, current_base_dir)
                try:
                    os.mkdir(os.path.realpath(self.provided_out_dir_path))
                except FileExistsError:
                    pass
                _file_mover = FileMover(current_in_dir, corresponding_out_dir)
                try:
                    os.mkdir(self.result_location)
                except FileExistsError:
                    pass

                try:
                    with open(os.path.join(self.result_location, current_base_dir), 'a') as list_file:
                        for file_name in files:
                            list_file.write(file_name + "\n")
                            try:
                                _file_mover.move_file(file_name)
                            except FileNotFoundError:
                                print("Got exception during moving file")
                                print(traceback.print_exc())
                except FileNotFoundError:
                    print("Got exception in append mode block")
                    with open(os.path.join(self.result_location, current_base_dir), 'w') as list_file:
                        for file_name in files:
                            list_file.write(file_name + "\n")
                            try:
                                _file_mover.move_file(file_name)
                            except FileNotFoundError:
                                print("Got exception during moving file")
                                print(traceback.print_exc())
            else:
                print("No file under directory {}".format(current_in_dir))

    def move_files_under_a_dir(self, current_in_dir,inside_files):
        current_base_dir = os.path.basename(current_in_dir)
        corresponding_out_dir = os.path.join(self.provided_out_dir_path, current_base_dir)
        try:
            os.mkdir(os.path.realpath(self.provided_out_dir_path))
        except FileExistsError:
            pass
        _file_mover = FileMover(current_in_dir, corresponding_out_dir)
        try:
            os.mkdir(self.result_location)
        except FileExistsError:
            pass

        try:
            with open(os.path.join(self.result_location, current_base_dir), 'a') as list_file:
                for file_name in inside_files:
                    list_file.write(file_name + "\n")
                    try:
                        _file_mover.move_file(file_name)
                    except FileNotFoundError:
                        print("Got exception during moving file")
                        print(traceback.print_exc())
        except FileNotFoundError:
            print("Got exception in append mode block")
            with open(os.path.join(self.result_location, current_base_dir), 'w') as list_file:
                for file_name in inside_files:
                    list_file.write(file_name + "\n")
                    try:
                        _file_mover.move_file(file_name)
                    except FileNotFoundError:
                        print("Got exception during moving file")
                        print(traceback.print_exc())

    def list_files_n_move_mlt(self):
        dir_vs_its_file_list = {}
        for current_in_dir, dirs, files in os.walk(self.provided_in_dir_path):
            if len(files) > 0:
                dir_vs_its_file_list[current_in_dir]=files
            else:
                print("No file under directory {}".format(current_in_dir))

        for dir, inside_files in dir_vs_its_file_list.items():
            #TODO create a thread for each directory. to run move_files_under_a_dir()
            pass

        #TODO once all threads are created run those threads


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir_path")
    parser.add_argument("output_dir_path")
    args = parser.parse_args()
    input_dir = args.input_dir_path
    output_dir = args.output_dir_path
    file_lister = FileLister('*', input_dir, output_dir)
    file_lister.list_files_n_move()

