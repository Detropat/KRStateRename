import os

from kr_state_rename import kr_state_rename

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
input_directory_states = directory_input + '\\states'
directory_output = directory + '\\output'


def main():
    print('Start rename script')
    for state_filename in os.listdir(input_directory_states):
        absolute_file_path_state = os.path.join(input_directory_states, state_filename)
        kr_state_rename(absolute_file_path_state, directory_input, directory_output).main()
    print('End of rename script')


if __name__ == "__main__":
    main()
