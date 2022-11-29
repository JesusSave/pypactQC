from pypactQC.util.decorators import freeze_it
from pypactQC.util.lines import first_occurrence
from pypactQC.util.jsonserializable import JSONSerializable
from pypactQC.output.nuclide import Nuclide
from pypactQC.output.nuclideUE import NuclideUE
from pypactQC.output.tags import NUCLIDES_HEADER
from pypactQC.output.tags import UNCERTAINTY_ESTIMATES
import pypactQC.util.propertyfinder as pf

NUCLIDES_IGNORES = ['\n', '|']


@freeze_it
class NuclidesUE(JSONSerializable):
    """
        The nuclides type from the output
    """
    def __init__(self):
        self.nuclidesUE = []

    def __len__(self):
        return len(self.nuclidesUE)

    def __getitem__(self, index):
        return self.nuclidesUE[index]

    def json_deserialize(self, j, objtype=object):
        super(NuclidesUE, self).json_deserialize(j)
        self.json_deserialize_list(j, 'nuclidesUE', NuclideUE)

    def fispact_deserialize(self, filerecord, interval):

        self.__init__()

        substring = filerecord[interval]

        starttag = '0   Nuclide     Atoms     E(Atoms)  Activity E(Activity)   Heat     E(Heat)  Dose Rate E(Dose Rate) Ingest   E(Ingest)   Inhale   E(Inhale)   % Error\n'
        endtag = '\n1'


        # The column headers line is after the main nuclide header
        def get_header(index):
            raw = substring[index].split('  ')
            header = list(filter(''.__ne__, raw))
            for ignore in NUCLIDES_IGNORES:
                if ignore in header:
                    header = list(filter(ignore.__ne__, header))
            return header

        # The nuclides list starts from the line prior to the total number
        # so we need the line number of this tag and count backwards
        i, line = first_occurrence(lines=substring, tag=starttag)

        # The end of Uncertainty Estimate of nuclides list
        js = []
        for j,ln in enumerate(substring[i:]):
            if ln.startswith("1"):
              js.append(j)
        if not js:
          js.append(len(substring)-i)
           
        '''
        print(f'------------ interval {interval}')
        if (interval>=98):
          print(f'== i {i} {js[0]} {line}, {len(substring)}')
          print(get_header(i+1))
          print(get_header(i+2))          
          print(get_header(i+js[0]-1))
        '''
        if i < 0:
            return

        header = get_header(i)
        if (len(header) < 13):
          header = ['Nuclide', 'Atoms', 'E(Atoms)', 'Activity', 'E(Activity)','Heat', 'E(Heat)', 'Dose Rate', 'E(Dose Rate)', 'Ingest', 'E(Ingest)','Inhale', 'E(Inhale)','% Error']

        for n in range(i+1, i+js[0]):
            #print(n,substring[n:])
            nuclide = NuclideUE()
            nuclide.fispact_deserialize(substring[n:],
                                        column_headers=header)
            self.nuclidesUE.append(nuclide)
