import csv
import json
import os
import os.path
from os import path

from natsort import os_sorted

from kr_state_rename import kr_state_rename

directory = os.path.dirname(os.path.abspath(__file__))
directory_input = directory + '\\input'
input_directory_states = directory_input + '\\states'
directory_output = directory + '\\output\\'

states = []
supported_languages = []


def main():
    print('Start rename script')

    if not path.isfile(directory_output + 'states.json') and not path.isfile(directory_output + 'languages.json'):
        print('Loading in fresh states, victory points and languages')
        files = os.listdir(input_directory_states)
        files = os_sorted(files)
        for state_filename in files:
            absolute_file_path_state = os.path.join(input_directory_states, state_filename)
            states.append(kr_state_rename(absolute_file_path_state, directory_input, directory_output).main())

            # Add it to the support languages array to keep a dynamic language system
            if states[-1]['translation_names'] is not None:
                add_language(states[-1]['translation_names'], True)
            if states[-1]['vp_translation_names'] is not None:
                add_language(states[-1]['vp_translation_names'], False)

        supported_languages.sort(key=str.lower)
        # Make a save
        with open(directory_output + 'states.json', 'w', encoding='utf-8') as file:
            json.dump(states, file, ensure_ascii=False)
        with open(directory_output + 'languages.json', 'w', encoding='utf-8') as file:
            json.dump(supported_languages, file, ensure_ascii=False)
    else:
        print('Loading in cache files. Ya, for speed!')

    states_array = json.load(open(directory_output + 'states.json', encoding='utf-8'))
    supported_languages_array = json.load(open(directory_output + 'languages.json', encoding='utf-8'))

    create_csv(states_array, supported_languages_array)
    print('End of rename script')


def add_language(language, state=True):
    if state is False:
        for v in language:
            if v[1] not in supported_languages:
                supported_languages.append(v[1])
    else:
        if language[1] not in supported_languages:
            supported_languages.append(language[1])


def create_csv(states_array=None, supported_languages_array=None):
    print('Start creating CSV')
    with open(directory_output + 'output.csv', 'w', newline='\n', encoding="utf-8") as c:
        writer = csv.writer(c)
        header = ['State ID', 'VP ID', 'State name']

        for n in supported_languages_array:
            header.append(n)

        # Create the header
        writer.writerow(header)

        for s in states_array:

            # Write the default state
            main_row = [s['id'], '', s['state_default_name']]
            # pprint(s)
            for n in supported_languages_array:
                write_value = None
                if s['translation_names'] is not None and n == s['translation_names'][1]:
                    write_value = s['translation_names'][2]

                main_row.append(write_value)

            writer.writerow(main_row)

            # Write the first province
            for vp in s['vp_default_names']:
                vp_province = ['', vp[0], vp[1]]
                for n in supported_languages_array:
                    write_value = None
                    for vp_trans in s['vp_translation_names']:
                        if vp_trans[0] == vp[0] and n == vp_trans[1]:
                            write_value = vp_trans[2]
                    vp_province.append(write_value)
                writer.writerow(vp_province)
            # exit(0)

    print('Finished CSV!')


if __name__ == "__main__":
    main()
