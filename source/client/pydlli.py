import runpy
import requests

import shutil
import os


def _decryption(input_file, output_file, key):
    with open(input_file, 'rb') as file_in:
        with open(output_file, 'wb') as file_out:
            while True:
                chunk = file_in.read(1024)
                if not chunk:
                    break

                encrypted_chunk = bytearray([byte ^ (key % 256) for byte in chunk])
                file_out.write(encrypted_chunk)


def get_public_key():
    key = requests.get('http://pandev.x10.mx/pydll/public_key').content
    return int(key, 16)


def makedir_if_not_exists(dir_path):
    if os.path.exists(dir_path):
        return True
    else:
        os.makedirs(dir_path)


def import_dll(file, temp_directory="temp/", temp_filename="library.example.content",
               use_a_class=None):  # Function to import python files as dll or other files

    makedir_if_not_exists(temp_directory)  # Make a temporary directory

    temp_file = temp_directory + temp_filename

    _decryption(file, temp_file, get_public_key())  # Decrypt DLL

    i = runpy.run_path(temp_file)

    if use_a_class is not None:  # If class is set, then you can use "." (Example: `libname.run_xy()`)
        return i[use_a_class]()
    else:  # If class is not set, then can only use "[]" (Example: `libname['run_xy']()`)
        return i
