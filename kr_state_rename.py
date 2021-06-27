import os
from pprint import pprint

from ClauseWizard import cwparse


class kr_state_rename:
    # Constructor
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.input_directory_localisation = self.input_directory + '\\localisation'
        self.input_directory_states = self.input_directory + '\\states'
        self.localisation_files = []
        self.state = {}
        self.state_id = None
        self.state_provinces = []
        self.state_default_name = None

    # Start the main script
    def main(self):
        print('Loading in state files')
        for state_filename in os.listdir(self.input_directory_states):
            absolute_file_path_state = os.path.join(self.input_directory_states, state_filename)
            self.parse_state_file(absolute_file_path_state)

            # Continue on to find everything in the KR_00_Map_States_Native_l_english and KR_00_Map_Victory_Points_Native_l_english files
            self.find_in_state_file()
            exit(0)

        print('Starting loading in localisation files')
        for filename in os.listdir(self.input_directory_localisation):
            absolute_file_path = os.path.join(self.input_directory_localisation, filename)
            self.create_localisation_object(absolute_file_path)

    def find_in_state_file(self):
        with open(self.input_directory_localisation + '\\KR_00_Map_States_Native_l_english.yml', 'r',
                  encoding="utf-8") as stream:
            for line in stream:
                if ('endo_state_' + self.state_id + ':0') in line:
                    self.state_default_name = line.split(':0')
                    print(self.state_default_name)

    # Parsing a state file
    def parse_state_file(self, filename):
        print('Handling file: ' + filename)
        with open(filename, 'r', encoding='latin-1') as f:
            self.state = cwparse(f.read(), False)
            for k, v in self.state:
                for state_array, s in v:
                    if 'id' == state_array:
                        self.state_id = str(s[0])
                    if 'history' == state_array:
                        for victory_point, vp in s:
                            if 'victory_points' == victory_point:
                                # The first element is the state ID
                                # The second one is the VP value itself
                                self.state_provinces.append(vp[0][0])

        pprint(self.state_provinces)

    # Create a local object to be used later on, many, many times :-)
    def create_localisation_object(self, filename):
        print('Parsing ' + filename)
