from opals import Import, Grid, Diff, Histo, Types, Bounds, Overlap, ZColor
from StripsFabric import StripsFabric
from StatsReportGenerator import StatsReportGenerator
import os

class OverlappingStripsComparer:
    '''
    Class for comparing overlapping strips. 
    It is intended to use for strips comparation from one moment in time.
    Parameters:
    -----------
    StripsFabric: StripsFabric object
        get StripsFabric object necessary for further operations
    result_raster_folder: string
        folder name for resulting rasters and other elements (histo, reports)
    '''
    def __init__(self, StripsFabric, result_folder):
        self.stripsFabric = StripsFabric
        self.result_folder = os.path.join(self.stripsFabric.absolute_path, result_folder)
        if not os.path.exists(self.result_folder):
                os.makedirs(self.result_folder)

        self.report = StatsReportGenerator(os.path.join(self.result_folder, 'overlapping_stats.txt'))
    '''
    Create overlap file for given strips. Useful for further comparisons.
    '''
    def _createOverlap(self):
        strips_list = self.stripsFabric.getStripsPlusCorrectedFromFile()
        bounds_list = list()
        for base_strip in strips_list:

            imp = Import.Import()
            imp.inFile = base_strip + '.las'
            imp.outFile = base_strip + '.odm'
            imp.run()

            bound = Bounds.Bounds()
            bound.inFile = imp.outFile
            bound.outFile = base_strip + '_bounds.shp'
            bound.run()

            grid = Grid.Grid()
            grid.inFile = imp.outFile
            grid.outFile = base_strip + '_z.tif'
            grid.interpolation = Types.GridInterpolator.movingPlanes
            grid.gridSize = 0.5
            grid.run()

            bounds_list.append(bound.outFile)

        overlap = Overlap.Overlap()
        overlap.inFile = bounds_list
        overlap.outFile = os.path.join(self.result_folder, 'overlap.txt')
        overlap.run()
    '''
    Compare strips
    '''
    def compare(self):
        self._createOverlap()
        overlap_file = open(os.path.join(self.result_folder, 'overlap.txt'), 'r')

        for line in overlap_file:
            splitted_line = line.split('|')
            strip1 = splitted_line[0].strip().split('_bounds')[0] + '_z.tif'
            strip2 = splitted_line[1].strip().split('_bounds')[0] + '_z.tif'

            diff_name = os.path.splitext(os.path.basename(strip1))[0] + '-' + os.path.splitext(os.path.basename(strip2))[0]
            diff_rasters_folder = os.path.join(self.result_folder, 'diff_rasters')
            if not os.path.exists(diff_rasters_folder):
                os.makedirs(diff_rasters_folder)
            diff_raster_file = os.path.join(diff_rasters_folder, diff_name + '.tif')

            diff = Diff.Diff()
            diff.inFile = [strip1, strip2]
            diff.outFile = diff_raster_file
            diff.run()

            zco = ZColor.ZColor()
            zco.inFile = diff_raster_file
            zco.outFile = os.path.join(diff_rasters_folder, diff_name + '_coloured.tif')
            zco.palFile = r'$OPALS_ROOT\addons\pal\differencePal.xml'
            zco.zRange = [-0.5,0.5]
            zco.run()

            hist = Histo.Histo()
            hist.inFile = diff_raster_file
            hist.plotFile = os.path.join(diff_rasters_folder, diff_name + '_histo.svg')
            hist.binWidth = 0.02
            hist.sampleRange = [-0.5, 0.5]
            hist.run()

            histogram_param = hist.histogram[0]
            min_val = float("{0:.3f}".format(histogram_param.getMin()))
            max_val = float("{0:.3f}".format(histogram_param.getMax()))
            mean = float("{0:.3f}".format(histogram_param.getMean()))
            std = float("{0:.3f}".format(histogram_param.getStd()))
            rms = float("{0:.3f}".format(histogram_param.getRms()))

            self.report.addValuesAndWrite(diff_name, min_val, max_val, mean, std, rms)
            
        self.report.summarize()


                