from pypactQC.util.decorators import freeze_it
from pypactQC.util.numerical import is_float, get_float
from pypactQC.util.jsonserializable import JSONSerializable
from pypactQC.library.nuclidelib import get_zai

NUCLIDE_IGNORES = ['\n', '|', '>', '&', '?', '#']


@freeze_it
class NuclideUE(JSONSerializable):
    """
        The nuclide type from the output
    """
    def __init__(self):
        self.nuclide = ""
        self.atoms = 0.0
        self.atoms_Error = 0.0
        self.activity = 0.0
        self.activity_Error = 0.0
        self.heat = 0.0
        self.heat_Error = 0.0
        self.dose = 0.0
        self.dose_Error = 0.0
        self.ingestion = 0.0
        self.ingestion_Error = 0.0
        self.inhalation = 0.0
        self.inhalation_Error = 0.0
        self.error = 0.0

    @property
    def name(self):
        return f"{self.nuclide}" 

    @property
    def zai(self):
        return get_zai(self.name) 

    def fispact_deserialize(self, linedump, column_headers):

        self.__init__()

        # takes the first line of the dump and
        # strip of the markers and ignores
        line = linedump[0]
        for i in NUCLIDE_IGNORES:
            line = line.replace(i, '')
	
        # turn the line into a list
        #strings = line.split()
        # leave one space
        # nuclide name need to be stripped seperately
        # remove extra space
        first = ' '.join(line[0:12].split()) 
        # remove left and right space
        #first = ''.join(line[0:12].rstrip().lstrip())
        strings = line[12:].split('  ')
        # add the nuclide name back to the list
        strings[:0] = [f'{first}']

        # Remove the 0 entry so that the entries now match with the header
        #strings.pop(0)
        
        #print(f'{column_headers}')
        #print(f'{strings}')
        #print(f'len  {len(column_headers)}')
        #print(f'len  {len(strings)}')
        
        self.nuclide = strings[0]
       
        assert(len(column_headers) == len(strings))

        def get_entry(header_name):
            column_index = index_containing_substring(column_headers, header_name)
            if column_index != -1:
                item = strings[column_index]
                if is_float(item):
                    return get_float(item)

            return 0.0

        self.atoms = get_entry('Atoms')
        self.atoms_Error = get_entry('E(Atoms)')
        self.activity = get_entry('Activity')
        self.activity_Error = get_entry('E(Activity)')
        self.heat = get_entry('Heat')
        self.heat_Error = get_entry('E(Heat)')
        self.dose = get_entry('Dose Rate')
        self.dose_Error = get_entry('E(Dose Rate)')
        self.ingestion = get_entry('Ingest')
        self.ingestion_Error = get_entry('E(Ingest)')
        self.inhalation = get_entry('Inhale')
        self.inhalation_Error = get_entry('E(Inhale)')
        self.error = get_entry('% Error')



def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1
