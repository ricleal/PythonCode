#!/usr/bin/env python3

import argparse
import os
from shutil import copyfile

import h5py
import numpy as np

FIELD = 'entry/instrument/instrument_xml/data'
args = None


def parse_arguments():
    '''
    Parse command line arguments
    '''

    global args
    parser = argparse.ArgumentParser(
        description='Replace field content in HDF')
    parser.add_argument('-i', '--input_files',
                        help='Input Nexus files to replace. Use comma separated list for multiple files.', required=True)
    parser.add_argument(
        '-x', '--xml_file', help='Input IDF XML file to replace the content', required=True)
    parser.add_argument('-s', '--suffix', help='Backup suffix',
                        required=False, default="orig")
    parser.add_argument('-o', '--overwrite',  action='store_true', help='Overwrite existing backup file',
                        required=False, default=False)
    args = parser.parse_args()


def backup(filename):
    '''
    Backups the original file if it doest not exist. Add as suffix the args.suffix
    If the file exist. overwrites it if args.overwrite is set to true
    '''

    dest_filename = filename + "." + args.suffix
    if not os.path.exists(dest_filename) or args.overwrite:
        copyfile(filename, dest_filename)
        return True
    else:
        print('The file you trying to backup already exists: {}.'
              ' Use the option -o/--overwrite.'.format(dest_filename))


def file_to_string(filename):
    ''' Opens a filename, and returns its contents as a string
    return None if the file does not exist'''

    if not os.path.exists(filename):
        print("The file {} does not exist.".format(filename))
        return None
    with open(filename, 'r') as my_file:
        data = my_file.read()
    return data


def replace_field_with_content(filename, content):
    ''' In the HDF file replaces the contents of FIELD with content '''
    with h5py.File(filename, 'r+') as f:
        del f[FIELD]
        f[FIELD] = np.string_(content)


def main():
    ''' main function.  Split the file names
    '''
    parse_arguments()
    for filename in [f.strip() for f in args.input_files.split(',')]:
        print('* Processing file {}.'.format(filename))
        backup_succeed = backup(filename)
        if backup_succeed:
            content = file_to_string(args.xml_file)
            if content:
                print("Replacing the contents of {} with the contents of {}.".format(
                    FIELD, args.xml_file))
                replace_field_with_content(filename, content)


if __name__ == "__main__":
    main()
