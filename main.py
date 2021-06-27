import os

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
directory_input_localisation = directory_input + '\\localisation'
directory_input_states = directory_input + '\\states'
directory_output = directory + '\\output'


def main():
    print('Starting loading in localisation files')

    for filename in os.listdir(directory_input_localisation):
        absolute_file_path = os.path.join(directory_input_localisation, filename)
        # Create a local object to be used later on, many, many times :-)
        create_localisation_object(absolute_file_path)


def create_localisation_object(filename):
    print('Parsing ' + filename)
    with open(filename, 'r', encoding='utf-8') as f:
        print('Starting')


if __name__ == "__main__":
    main()
