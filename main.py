import csv
import os
from pprint import pprint

from kr_state_rename import kr_state_rename

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
input_directory_states = directory_input + '\\states'
directory_output = directory + '\\output\\'

states = []
supported_languages = []


def main():
    print('Start rename script')
    print('Creating basic CSV file')

    for state_filename in os.listdir(input_directory_states):
        absolute_file_path_state = os.path.join(input_directory_states, state_filename)
        states.append(kr_state_rename(absolute_file_path_state, directory_input, directory_output).main())

        # Add it to the support languages array to keep a dynamic language system
        if states[-1]['translation_names'] is not None:
            add_language(states[-1]['translation_names'], True)
        if states[-1]['vp_translation_names'] is not None:
            add_language(states[-1]['vp_translation_names'], False)

    supported_languages.sort(key=str.lower)
    create_csv()
    print('End of rename script')


def add_language(language, state=True):
    if state is False:
        for v in language:
            if v[1] not in supported_languages:
                supported_languages.append(v[1])
    else:
        if language[1] not in supported_languages:
            supported_languages.append(language[1])


def create_csv():
    with open(directory_output + 'output.csv', 'w', newline='\n', encoding="utf-8") as c:
        writer = csv.writer(c)
        header = ['State ID', 'VP ID']

        for n in supported_languages:
            header.append(n)

        # Create the header
        writer.writerow(header)


if __name__ == "__main__":
    main()
