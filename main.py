import csv
import json
import os
import os.path
from pprint import pprint
from os import path

from kr_state_rename import kr_state_rename

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
input_directory_states = directory_input + '\\states'
directory_output = directory + '\\output\\'

states = []
supported_languages = []


def main(supported_languages=None, states=None):
    print('Start rename script')

    if not path.isfile(directory_output + 'states.json') and not path.isfile(directory_output + 'languages.json'):
        print('Loading in fresh states, victory points and languages')
        for state_filename in os.listdir(input_directory_states):
            absolute_file_path_state = os.path.join(input_directory_states, state_filename)
            states.append(kr_state_rename(absolute_file_path_state, directory_input, directory_output).main())

            # Add it to the support languages array to keep a dynamic language system
            if states[-1]['translation_names'] is not None:
                add_language(states[-1]['translation_names'], True)
            if states[-1]['vp_translation_names'] is not None:
                add_language(states[-1]['vp_translation_names'], False)

        supported_languages.sort(key=str.lower)
        # Make a save
        with open(directory_output + 'states.json', 'w') as file:
            json.dump(states, file)
        with open(directory_output + 'languages.json', 'w') as file:
            json.dump(supported_languages, file)
    else:
        print('Loading in cache files. Ya, for speed!')
        states_file = open(directory_output + 'states.json')
        states = json.load(states_file)
        states_file.close()

        languages_file = open(directory_output + 'languages.json')
        supported_languages = json.load(languages_file)
        languages_file.close()

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
    print('Start creating CSV')
    with open(directory_output + 'output.csv', 'w', newline='\n', encoding="utf-8") as c:
        writer = csv.writer(c)
        header = ['State ID', 'VP ID']

        for n in supported_languages:
            header.append(n)

        # Create the header
        writer.writerow(header)

    print('Finished CSV!')


if __name__ == "__main__":
    main()
