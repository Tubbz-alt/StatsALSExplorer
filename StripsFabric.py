
import os

class StripsFabric:
    '''
    Class for producing strips from given strips names.
    Initialize paths to strips.
    Parameters:
    -----------
    absolute_path: os.path
        Path to file with strips or raster files that OPALS is able to utilize
    strips_filename: string
        Name of file that consists of strips names
    corrected_ending: string
        Ending for corrected strips. Default is "_corrected"
    '''
    def __init__(self, absolute_path, strips_filename, corrected_ending = '_corrected'):
        self.absolute_path = absolute_path
        self.strips_filename = strips_filename
        self.inFile = open(os.path.join(self.absolute_path, self.strips_filename), 'r')
        self.corrected_ending = corrected_ending
    '''
    Returns:
    -----------
    strips_list from strips file
    '''
    def getStripsFromFile(self):
        self.strips_list = list()
        for strip in self.inFile:
            base_strip = os.path.join(self.absolute_path, strip.strip())
            self.strips_list.append(base_strip)
        return self.strips_list
    '''
    Returns:
    -----------
    strips_list from strips file with corrected strips. 
    Make sure that files with given corrected_ending exists. Look at __init__ description
    '''
    def getStripsPlusCorrectedFromFile(self):
        self.strips_list = list()
        for strip in self.inFile:
            base_strip = os.path.join(self.absolute_path, strip.strip())
            corrected_strip = os.path.join(self.absolute_path, strip.strip()) + self.corrected_ending
            self.strips_list.append(base_strip)
            self.strips_list.append(corrected_strip)
        return self.strips_list