import os
import sys
import time
import shutil
import hashlib
import multiprocessing
from collections import Counter



def time_calc(seconds):
    suffix = ["Seconds", "Minutes", "Hours"]
    if seconds > 60:
        minutes = seconds / 60
        if minutes >= 60:
            return ("%s:%s:%s ") % (str(int(minutes / 60)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(seconds % 60)).zfill(2)) + suffix[2]
        else:
            return ("%s:%s ") % (str(int(minutes)).zfill(2), str(int(seconds % 60)).zfill(2)) + suffix[1]
    else:
        return ("%s ") % (str(int(seconds)).zfill(2)) + suffix[0]


def get_folder_size(folder):
    total_size = 0
    folder_files = os.listdir(folder)
    for i in folder_files:
        path = os.path.join(folder, i)
        file_size = os.path.getsize(path)
        total_size += file_size
    return total_size


def file_size_converter(byts):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if byts == 0:
        return '0 B'
    else:
        i = 0
        while byts >= 1000 and i < len(suffixes)-1:
            byts /= 1000
            i += 1
        size = ('%.2f' % byts).rstrip('0').rstrip('.')
        return '%s %s' % (size, suffixes[i])


def delete_the_Duplicate_files_folder():
    while True:
        should_i_delete = input('Do you want to delete the "' + str(Duplicate_files_folder) + '" folder?, (y/n): ')
        answer_as_string = str(should_i_delete)
        answer_in_lower_case = answer_as_string.lower()
        if answer_in_lower_case == 'y':
            shutil.rmtree(Duplicate_files_folder)
            print('"' + str(Duplicate_files_folder) + '" folder deleted.. ')
            break
        elif answer_in_lower_case == 'n':
            break
        else:
            print('Please answer with "y" or "n" only!')
            continue


def delete_the_Progress_log_folder():
    while True:
        should_i_delete = input('Do you want to delete the "' + str(Progress_log_for_duplicate_files_finder) + '" folder?, (y/n): ')
        answer_as_string = str(should_i_delete)
        answer_in_lower_case = answer_as_string.lower()
        if answer_in_lower_case == 'y':
            shutil.rmtree(Progress_log_for_duplicate_files_finder)
            print('"' + str(Progress_log_for_duplicate_files_finder) + '" folder deleted.. ')
            break
        elif answer_in_lower_case == 'n':
            break
        else:
            print('Please answer with "y" or "n" only!')
            continue


def sorting_function(tuple):
        return tuple[1]


def get_file_extension(file_name):
    extension = os.path.splitext(file_name)[1]
    if extension:
        return extension
    else:
        return 'empty'

def get_file_name_and_extension(file_name):
    return (file_name, get_file_extension(file_name))

def get_file_name_and_size(file_name):
    if os.path.isfile(file_name) and file_name != os.path.basename(__file__):
        return (file_name, os.path.getsize(file_name))


def Get_first_1024_bytes_hash(file_name):
    BLOCKSIZE = 1024
    hasher = hashlib.sha1()
    with open(file_name, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        hasher.update(buf)
    return (file_name, hasher.hexdigest())

def Get_entire_file_hash(file_name):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(file_name, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return (file_name, hasher.hexdigest())


def This_many_white_spaces(strng):
    return " " * int((len(Saving_progress_msg) - len(strng)) / 2)


def find_repetitive_sizes(lst):
    msg = '=== Looking for files with recurring sizes ==='
    print('\n' + This_many_white_spaces(msg) + msg)
    Counted_sizes = Counter([i[1] for i in lst])
    Counted_sizes_as_a_list = list(Counted_sizes.items())
    Counted_sizes_as_a_list.sort(reverse=True, key=sorting_function)
    eligible_sizes = [size for size, size_repetition_count in Counted_sizes_as_a_list if size_repetition_count > 1]
    eligible_sizes.sort()
    eligible_files_names = [i[0] for i in lst if i[1] in eligible_sizes]
    print(Saving_progress_msg)
    with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_sizes_lst.txt'), 'w') as f:
        for i in eligible_files_names:
            f.write(str(i) + '\n')
        f.write('This_lst_is_complete')
    print(Finished_saving_msg)
    return eligible_files_names


def find_repetitive_extensions(lst):
    msg = '=== Looking for files with recurring extensions === '
    print('\n' + This_many_white_spaces(msg) + msg)
    Counted_extensions = Counter([i[1] for i in lst])
    Counted_extensions_as_a_list = list(Counted_extensions.items())
    Counted_extensions_as_a_list.sort(reverse=True, key=sorting_function)
    eligible_extensions = [ext for ext, ext_repetition_count in Counted_extensions_as_a_list if ext_repetition_count > 1]
    eligible_extensions.sort()
    eligible_files_names = [i[0] for i in lst if i[1] in eligible_extensions]
    print(Saving_progress_msg)
    with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_extensions_lst.txt'), 'w') as f:
        for i in eligible_files_names:
            f.write(str(i) + '\n')
        f.write('This_lst_is_complete')
    print(Finished_saving_msg)
    return eligible_files_names


def find_repetitive_1024Bytes_hashes(lst):
    msg = '=== Looking for files with recurring 1024Byte hashes ==='
    print('\n' + This_many_white_spaces(msg) + msg)
    Counted_hashes = Counter([i[1] for i in lst])
    Counted_hashes_as_a_list = list(Counted_hashes.items())
    Counted_hashes_as_a_list.sort(reverse=True, key=sorting_function)
    eligible_hashes = [Hash for Hash, Hash_repetition_count in Counted_hashes_as_a_list if Hash_repetition_count > 1]
    eligible_hashes.sort()
    eligible_files_names = [i[0] for i in lst if i[1] in eligible_hashes]
    print(Saving_progress_msg)
    with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_1024Bytes_hashes.txt'), 'w') as f:
        for i in eligible_files_names:
            f.write(str(i) + '\n')
        f.write('This_lst_is_complete')
    print(Finished_saving_msg)
    return eligible_files_names


def byte_by_byte_comparison(lst):
    global Duplicates_counter
    if len(lst) > 1:
        print('\nStarting full hash comparison ...')
    Duplicate_files_names = []
    for i,x in enumerate(lst, start=1):
        if x[0] in Duplicate_files_names:
            continue
        else:
            if i == len(lst):
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'Unique_files_names.txt'), 'a') as f:
                    f.write(x[0] + '\n')
                break
            else:
                for y in lst[i:]:
                    if y[0] in Duplicate_files_names:
                        continue
                    else:
                        if x[1] == y[1]:
                            Duplicates_counter += 1
                            Duplicate_files_names.append(y[0])
                            Number_of_white_spaces = ' ' * int(30 - len('#' + str(Duplicates_counter)))
                            print('#' + str(Duplicates_counter) + Number_of_white_spaces + 'Moving "' + y[0] + '" into "' + Duplicate_files_folder + '" folder..')
                            shutil.move(y[0], Duplicate_files_folder)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'Unique_files_names.txt'), 'a') as f:
                    f.write(x[0] + '\n')





if __name__ == '__main__':


    Start_time = time.time()

    print('\nStarting program ...')

    Duplicate_files_folder = "Duplicate files"
    Progress_log_for_duplicate_files_finder = 'progress_log_for_duplicate_files_finder'
    Duplicates_counter = 0

    Saving_progress_msg = 'Saving progress.. it is recommended to wait for the "Finished saving" msg before you exit the program or this step will be lost ... '
    Finished_saving_msg = 'Finished saving ...'
    Loading_progress_msg = '\nLoading progress from last session.. please wait ...'

    if not os.path.isdir(Duplicate_files_folder):
        os.mkdir(Duplicate_files_folder)
    
    if not os.path.isdir(Progress_log_for_duplicate_files_finder):
            os.mkdir(Progress_log_for_duplicate_files_finder)

    Use_this_many_cores = multiprocessing.cpu_count() - 2
    
    chunk_size_for_map = 10


    if os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_files_names_and_full_hash_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_files_names_and_full_hash_lst.append(element)

            if os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'Unique_files_names.txt')):
                saved_unique_files_names_lst = []
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'Unique_files_names.txt'), 'r') as f:
                    for line in f.readlines():
                        if len(line) > 0:
                            saved_unique_files_names_lst.append(line.rstrip('\n'))
                saved_unique_files_names_lst.sort()
                whats_left_of_the_lst = [i for i in saved_files_names_and_full_hash_lst if os.path.isfile(i[0]) and i[0] not in saved_unique_files_names_lst]

                if len(whats_left_of_the_lst) > 0:
                    byte_by_byte_comparison(whats_left_of_the_lst)
            
            else:

                saved_files_names_and_full_hash_lst = []
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'r') as f:
                    for line in f.readlines()[:-1]:
                        if len(line) > 0:
                            element = tuple(line.rstrip('\n').rsplit(" ", 1))
                            saved_files_names_and_full_hash_lst.append(element)
                    whats_left_of_the_lst = [i for i in saved_files_names_and_full_hash_lst if os.path.isfile(i[0])]
        
                    byte_by_byte_comparison(whats_left_of_the_lst)

        else:

            print(Loading_progress_msg)
            saved_repetitive_1024Bytes_hashes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_1024Bytes_hashes.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_1024Bytes_hashes_lst.append(line.rstrip('\n'))

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, saved_repetitive_1024Bytes_hashes_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)



    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_1024Bytes_hashes.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_1024Bytes_hashes.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_repetitive_1024Bytes_hashes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_1024Bytes_hashes.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_1024Bytes_hashes_lst.append(line.rstrip('\n'))

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, saved_repetitive_1024Bytes_hashes_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)

        else:

            print(Loading_progress_msg)
            saved_files_names_and_first_1024_bytes_hash_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_files_names_and_first_1024_bytes_hash_lst.append(element)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(saved_files_names_and_first_1024_bytes_hash_lst)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)




    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_files_names_and_first_1024_bytes_hash_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_files_names_and_first_1024_bytes_hash_lst.append(element)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(saved_files_names_and_first_1024_bytes_hash_lst)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)
        
        else:

            print(Loading_progress_msg)
            saved_repetitive_extensions_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_extensions_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_extensions_lst.append(line.rstrip('\n'))
    
            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, saved_repetitive_extensions_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)



    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_extensions_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_extensions_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_repetitive_extensions_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_extensions_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_extensions_lst.append(line.rstrip('\n'))

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, saved_repetitive_extensions_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)
        
        else:

            print(Loading_progress_msg)
            saved_files_names_and_extensions_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_files_names_and_extensions_lst.append(element)

            repetitive_extensions = find_repetitive_extensions(saved_files_names_and_extensions_lst)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)




    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_files_names_and_extensions_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_files_names_and_extensions_lst.append(element)

            repetitive_extensions = find_repetitive_extensions(saved_files_names_and_extensions_lst)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)
        
        else:

            print(Loading_progress_msg)
            saved_repetitive_sizes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_sizes_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_sizes_lst.append(line.rstrip('\n'))

            msg = '=== Getting file extensions === '
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_extension, saved_repetitive_sizes_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_extensions = find_repetitive_extensions(res)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)
    


    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_sizes_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_sizes_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_repetitive_sizes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'repetitive_sizes_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        saved_repetitive_sizes_lst.append(line.rstrip('\n'))

            msg = '=== Getting file extensions === '
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_extension, saved_repetitive_sizes_lst, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_extensions = find_repetitive_extensions(res)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)
        
        else:

            print(Loading_progress_msg)
            saved_clean_names_and_sizes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_clean_names_and_sizes_lst.append(element)
            
            repetitive_sizes = find_repetitive_sizes(saved_clean_names_and_sizes_lst)

            msg = '=== Getting file extensions === '
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_extension, repetitive_sizes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_extensions = find_repetitive_extensions(res)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)



    elif os.path.isfile(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt')):

        with open(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt'), 'r') as f:
            last_line = f.readlines()[-1]

        if last_line == 'This_lst_is_complete':
            print(Loading_progress_msg)
            saved_clean_names_and_sizes_lst = []
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt'), 'r') as f:
                for line in f.readlines()[:-1]:
                    if len(line) > 0:
                        element = tuple(line.rstrip('\n').rsplit(" ", 1))
                        saved_clean_names_and_sizes_lst.append(element)
            
            repetitive_sizes = find_repetitive_sizes(saved_clean_names_and_sizes_lst)

            msg = '=== Getting file extensions === '
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_extension, repetitive_sizes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_extensions = find_repetitive_extensions(res)

            msg = '=== Getting first 1024byte file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

            msg = '=== Getting full file hashes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

            res.sort(key=sorting_function)

            print(Saving_progress_msg)
            with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                for i in res:
                    f.write(str(i[0]) + " " + str(i[1]) + '\n')
                f.write('This_lst_is_complete')
            print(Finished_saving_msg)

            byte_by_byte_comparison(res)

        else:

            Items_lst = os.listdir()

            msg = '=== Getting file sizes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_size, Items_lst, chunksize=chunk_size_for_map)
            
            res = [i for i in res if i != None]

            if len(res) < 1:
                print('\nNo files were found ...')

            else:

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_sizes = find_repetitive_sizes(res)

                msg = '=== Getting file extensions === '
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(get_file_name_and_extension, repetitive_sizes, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_extensions = find_repetitive_extensions(res)

                msg = '=== Getting first 1024byte file hashes ==='
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

                msg = '=== Getting full file hashes ==='
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                byte_by_byte_comparison(res)



    else:

        Items_lst = os.listdir()

        if len(Items_lst) > 1:
            
            msg = '=== Getting file sizes ==='
            print('\n' + This_many_white_spaces(msg) + msg)
            with multiprocessing.Pool(Use_this_many_cores) as pool:
                res = pool.map(get_file_name_and_size, Items_lst, chunksize=chunk_size_for_map)
            
            res = [i for i in res if i != None]

            if len(res) < 1:
                print('\nNo files were found ...')

            else:

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'clean_names_and_sizes_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_sizes = find_repetitive_sizes(res)

                msg = '=== Getting file extensions === '
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(get_file_name_and_extension, repetitive_sizes, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_extensions_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_extensions = find_repetitive_extensions(res)

                msg = '=== Getting first 1024byte file hashes ==='
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(Get_first_1024_bytes_hash, repetitive_extensions, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_first_1024_bytes_hash_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                repetitive_hashes = find_repetitive_1024Bytes_hashes(res)

                msg = '=== Getting full file hashes ==='
                print('\n' + This_many_white_spaces(msg) + msg)
                with multiprocessing.Pool(Use_this_many_cores) as pool:
                    res = pool.map(Get_entire_file_hash, repetitive_hashes, chunksize=chunk_size_for_map)

                res.sort(key=sorting_function)

                print(Saving_progress_msg)
                with open(os.path.join(Progress_log_for_duplicate_files_finder, 'files_names_and_full_hash_lst.txt'), 'w') as f:
                    for i in res:
                        f.write(str(i[0]) + " " + str(i[1]) + '\n')
                    f.write('This_lst_is_complete')
                print(Finished_saving_msg)

                byte_by_byte_comparison(res)


    End_time = time.time()
    Time_consumed = End_time - Start_time
    print('\nDone!')
    print('Finished in ' + str(time_calc(Time_consumed)) + '..')


    if Duplicates_counter > 0:
        print('Moved ' + str(Duplicates_counter) + ' files into "' + Duplicate_files_folder + '" folder..')
        print('"' + str(Duplicate_files_folder) + '" folder is ' + str(file_size_converter(get_folder_size(Duplicate_files_folder))) + ' in size ...')
        delete_the_Duplicate_files_folder()
        delete_the_Progress_log_folder()
        print('\nExiting program ...')
    else:
        print('No duplicate files were found..')
        print('"' + str(Duplicate_files_folder) + '" folder is ' + str(file_size_converter(get_folder_size(Duplicate_files_folder))) + ' in size ...')
        delete_the_Duplicate_files_folder()
        delete_the_Progress_log_folder()
        print('\nExiting program ...')
