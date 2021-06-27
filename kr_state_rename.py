from pprint import pprint

from ClauseWizard import cwparse


class kr_state_rename:
    # Constructor
    def __init__(self, file, input_directory, output_directory):
        self.file = file
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.input_directory_localisation = self.input_directory + '\\localisation'
        self.input_directory_states = self.input_directory + '\\states'
        self.localisation_files = []
        self.state = {'vp_translation_names': [], 'provinces': [], 'vp_default_names': []}

    # Start the main script
    def main(self):
        print('Loading in state files')

        self.parse_state_file()

        # Continue on to find everything in the KR_00_Map_States_Native_l_english and
        # KR_00_Map_Victory_Points_Native_l_english files
        self.find_in_state_file()
        self.find_in_vp_file()
        pprint(self.state)
        # exit(0)

    # Search in the VP file
    def find_in_vp_file(self):
        with open(self.input_directory_localisation + '\\KR_00_Map_Victory_Points_Native_l_english.yml', 'r',
                  encoding="utf-8") as stream:
            for line in stream:
                for province in self.state['provinces']:
                    new_prov = str(province)
                    if ('endo_vp_' + new_prov + ':0') in line:
                        default_name = line.split(':0')
                        default_name = str(default_name[1].strip())
                        default_name = default_name.replace('"', '')
                        default_array = [new_prov, default_name]
                        self.state['vp_default_names'].append(default_array)
                    elif ('endo_vp_' + new_prov + '_') in line:
                        # Example endo_vp_3838_italian:0 "Ajaccio"
                        # Split it first by the underscore
                        line_string = line.split('_')
                        if line_string[3] is not None:
                            language = line_string[3].split(':0')
                            # By default it can look ugly, do some fixing. Ie. ['italian', ' "Corsica"\n']
                            formatted_name = str(language[1].strip())
                            formatted_name = formatted_name.replace('"', '')
                            vp = [new_prov, str(language[0]).lower(), formatted_name]
                            self.state['vp_translation_names'].append(vp)
                            pprint(self.state)
                            # exit(0)

    # Search in the state file
    def find_in_state_file(self):
        with open(self.input_directory_localisation + '\\KR_00_Map_States_Native_l_english.yml', 'r',
                  encoding="utf-8") as stream:
            for line in stream:
                # This is a search for the first default state name
                if ('endo_state_' + self.state['id'] + ':0') in line:
                    default_name = line.split(':0')
                    default_name = str(default_name[1].strip())
                    default_name = default_name.replace('"', '')
                    self.state['state_default_name'] = default_name
                elif ('endo_state_' + self.state['id'] + '_') in line:
                    # Example: endo_state_1_italian:0 "Corsica"
                    # Split it first by the underscore
                    line_string = line.split('_')
                    if line_string[3] is not None:
                        language = line_string[3].split(':0')
                        # By default it can look ugly, do some fixing. Ie. ['italian', ' "Corsica"\n']
                        formatted_name = str(language[1].strip())
                        formatted_name = formatted_name.replace('"', '')
                        new_state = [str(language[0]).lower(), formatted_name]
                        self.state['translation_names'] = new_state

    # Parsing a state file
    def parse_state_file(self):
        print('Handling file: ' + self.file)
        with open(self.file, 'r', encoding='latin-1') as f:
            self.state['raw_decode'] = cwparse(f.read(), False)
            for k, v in self.state['raw_decode']:
                for state_array, s in v:
                    if 'id' == state_array:
                        self.state['id'] = str(s[0])
                    if 'history' == state_array:
                        for victory_point, vp in s:
                            if 'victory_points' == victory_point:
                                # The first element is the state ID
                                # The second one is the VP value itself
                                self.state['provinces'].append(vp[0][0])
