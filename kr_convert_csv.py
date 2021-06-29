import csv
import json
import os

from py import path
from tqdm import tqdm


class kr_convert_csv:
    directory = None
    directory_output = None
    directory_input = None
    directory_renames = None
    directory_renames_cache = None
    files = []
    definitions = None
    continents = None

    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.directory_output = self.directory + '\\output\\'
        self.directory_input = self.directory + '\\input\\'
        self.directory_renames = self.directory + '\\renames\\'
        self.directory_renames_cache = self.directory + '\\renames\\cache\\'
        self.continents = ['ocean', 'europe', 'north_america', 'south_america', 'australia', 'africa', 'asia',
                           'middle_east',
                           'india', 'central_america']

    # Load in the definitions
    def load_definitions(self):
        print('Loading in definitions')
        with open(self.directory_input + 'definition.csv', newline='') as f:
            reader = csv.reader(f)
            self.definitions = list(reader)

    def main(self):
        print('Starting converting')
        print('Loading in supported languages')
        supported_languages = json.load(open(self.directory_output + 'languages.json', encoding='utf-8'))
        self.load_definitions()

        with open(self.directory_output + 'output.csv', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            if not path.isfile(self.directory_renames_cache + 'provinces.json'):
                # First retrieve all continents
                main_bar = tqdm(reader)
                state_check = False
                for (index, row) in enumerate(reader):
                    main_bar.set_description("Processing CSV rows %s" % index)
                    # Header, skip it
                    if 0 == index:
                        continue

                    # This is a state, so skip it for now
                    if not row[1]:
                        state_check = True
                        continue

                    for (i, d) in enumerate(self.definitions):
                        formatted_line = d[0].split(';')
                        # No match between the definition and province ID
                        if formatted_line[0] != row[1]:
                            continue

                        selected_continent = self.continents[int(formatted_line[7])]
                        # print(selected_continent)


convert = kr_convert_csv()
convert.main()
