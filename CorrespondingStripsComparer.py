
from opals import Import, Grid, Diff, Histo, Types, ZColor
from StripsFabric import StripsFabric
from StatsReportGenerator import StatsReportGenerator
import os

class CorrespondingStripsComparer:
    '''
    Class for comparing corresponding strips. For example one can compare strips from two periods:
    one before correction and after correction. 
    For this purpose strips in strips definition file should have same name with additional ending (e.g. '_corrected').
    Ending for corrected strips is set in StripsFabric object.
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

        self.report = StatsReportGenerator(os.path.join(self.result_folder, 'corresponding_strips_stats.txt'))
    '''
    Run strips comparation.
    '''
    def compare(self):
        strips_list = self.stripsFabric.getStripsPlusCorrectedFromFile()

        base_strips_list = strips_list[::2]
        corrected_strips_list = strips_list[1::2]
        #now every strip has corresponding corrected strip in corrected_strips_list 
        #like element 0 in corrected_strip_list is corrected strip of element 0 in base_strips_list

        i = 0
        for base_strip in base_strips_list:
            corrected_strip = corrected_strips_list[i]
            i += 1

            diff_name = os.path.splitext(os.path.basename(base_strip))[0] + '-' + os.path.splitext(os.path.basename(corrected_strip))[0]
            diff_rasters_folder = os.path.join(self.result_folder, 'diff_corresponding_rasters')
            if not os.path.exists(diff_rasters_folder):
                os.makedirs(diff_rasters_folder)
            diff_raster_file = os.path.join(diff_rasters_folder, diff_name + '.tif')

            imp = Import.Import()
            imp.inFile = base_strip + '.las'
            imp.outFile = base_strip + '.odm'
            imp.run()

            imp_corr = Import.Import()
            imp_corr.inFile = corrected_strip + '.las'
            imp_corr.outFile = corrected_strip + '.odm'
            imp_corr.run()

            grid = Grid.Grid()
            grid.inFile = imp.outFile
            grid.outFile = base_strip + '_z.tif'
            grid.interpolation = Types.GridInterpolator.movingPlanes
            grid.gridSize = 0.5
            grid.run()

            grid_corr = Grid.Grid()
            grid_corr.inFile = imp_corr.outFile
            grid_corr.outFile = corrected_strip + '_z.tif'
            grid_corr.interpolation = Types.GridInterpolator.movingPlanes
            grid_corr.gridSize = 0.5
            grid_corr.run()

            diff = Diff.Diff()
            diff.inFile = [base_strip + '_z.tif', corrected_strip + '_z.tif']
            diff.outFile = diff_raster_file
            diff.run()

            zco = ZColor.ZColor()
            zco.inFile = diff_raster_file
            zco.outFile = os.path.join(diff_rasters_folder, diff_name + '_coloured.tif')
            zco.palFile = r'$OPALS_ROOT\addons\pal\differencePal.xml'
            zco.zRange = [-0.5,0.5]
            zco.run()

            histo = Histo.Histo()
            histo.inFile = diff_raster_file
            histo.plotFile = os.path.join(diff_rasters_folder, diff_name + '_histo.svg')
            histo.binWidth = 0.02
            histo.sampleRange = [-0.5, 0.5]
            histo.run()

            self.report.deduceFromHistogram(histo.histogram, diff_name)

        self.report.summarize()