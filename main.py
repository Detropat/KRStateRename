import os

from kr_state_rename import kr_state_rename

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
directory_output = directory + '\\output'


def main():
    print('Start rename script')
    kr_state_rename(directory_input, directory_output).main()
    print('End of rename script')


if __name__ == "__main__":
    main()
