import re
import openpyxl


def search_enodeb_n_count(stats_file, enode_pattern, enodeb_count_dict):
    search_pattern = enode_pattern
    search_pattern_ob = re.compile(search_pattern, re.IGNORECASE)
    try:
        with open(stats_file, 'r') as stat_file:
            for line in stat_file.readlines():
                try:
                    match = search_pattern_ob.search(line).group(1)
                except AttributeError:
                    # pdb.set_trace()
                    # Ignoring end of file blank lines
                    pass
                else:
                    try:
                        old_count = enodeb_count_dict[match]
                    except KeyError:
                        enodeb_count_dict[match] = 1
                    else:
                        current_count = old_count+1
                        enodeb_count_dict[match] = current_count
    except (FileNotFoundError, IsADirectoryError):
        print("Stat file {} was not readable")
    finally:
        return enodeb_count_dict


def write_to_report(enodeb_count_dict_sum: dict, report_file_path):
    w_book = openpyxl.Workbook()
    w_sheet = w_book.active
    w_sheet.cell(1,1,"E_NodeB_Name")
    w_sheet.cell(1,2,"Files_count")
    current_row = 2
    for enodeB, count in enodeb_count_dict_sum.items():
        w_sheet.cell(current_row, 1, enodeB)
        w_sheet.cell(current_row, 2, count)
        current_row +=1
    w_book.save(report_file_path)


def move_and_read_stat_files(stat_files_directory):
    pass



if __name__ == "__main__":
    stat_file_path = r"D:\D_drive_BACKUP\MENTOR\TurkTel\LTE_HUAWEI\Analysis\Antalya\files_not_veing_collected_1.txt"
    report_file_path = r"D:\D_drive_BACKUP\MENTOR\TurkTel\LTE_HUAWEI\Analysis\Antalya\report.xlsx"
    EnodeB_pattern = "_*(L[0-9A-Za-z]+)_"
    global_enodeb_count_dict = {}
    global_enodeb_count_dict = search_enodeb_n_count(stat_file_path, EnodeB_pattern, global_enodeb_count_dict)
    print(global_enodeb_count_dict)
    write_to_report(global_enodeb_count_dict, report_file_path)
