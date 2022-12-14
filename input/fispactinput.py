import os
from pypactQC.input.fluxesfile import FluxesFile
from pypactQC.input.filesfile import FilesFile
from pypactQC.input.inputdata import InputData
from pypactQC.util.decorators import freeze_it
from pypactQC.util.jsonserializable import JSONSerializable


@freeze_it
class FispactInput(JSONSerializable):
    """
        Full FISPACT-II super input class
        that contains everything needed to run FISPACT-II.
        
        Contains the input data (input file), flux data (fluxes file) and
        nuclear data and file information (files file).
        
        This is then JSON serializable which can be used for a RESTful API.
    """
    def __init__(self, runname="run", fluxname="flux", nuclear_data_base=os.sep):
        self.input = InputData(name=runname)
        self.flux  = FluxesFile(name=fluxname)
        self.files = FilesFile(base_dir=nuclear_data_base)
