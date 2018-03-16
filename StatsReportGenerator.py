import os
import datetime

class StatsReportGenerator:
    
    def __init__(self, report_file):
        self.min_value = float(0)
        self.max_value = float(0)
        self.mean = float(0)
        self.std = float(0)
        self.rms = float(0)
        self.report_file = open(report_file, 'a')
        self.report_file.write('________ Stats from overlapping strips generated at: ' + str(datetime.datetime.now()) + ' ________\n')
        self.i = 0

    def _xstr(self, s):
        if s is None:
            return 'NULL'
        else:
            return str(s)

    def _xfloat(self, f):
        if f is None:
            return float(0)
        else:
            return float(f)

    def deduceFromHistogram(self, histogram, diff_name):
        histogram_param = histogram[0]
        min_val = float("{0:.3f}".format(histogram_param.getMin()))
        max_val = float("{0:.3f}".format(histogram_param.getMax()))
        mean = float("{0:.3f}".format(histogram_param.getMean()))
        std = float("{0:.3f}".format(histogram_param.getStd()))
        rms = float("{0:.3f}".format(histogram_param.getRms()))

        self._addValuesAndWrite(diff_name, min_val, max_val, mean, std, rms)


    def _addValuesAndWrite(self, compared_strips_name, min_value = None, max_value = None, mean = None, std = None, rms = None):
        self.min_value += self._xfloat(min_value)
        self.max_value += self._xfloat(max_value)
        self.mean += self._xfloat(mean)
        self.std += self._xfloat(std)
        self.rms += self._xfloat(rms)
        self.report_file.write(compared_strips_name + '\t Min: ' + self._xstr(min_value) + '\t Max: ' + self._xstr(max_value) + '\t Mean: ' +  self._xstr(mean) + '\t Std: ' + self._xstr(std) + '\t RMS:' + self._xstr(rms) + '\n')
        self.i += 1

    def summarize(self):
        mean_mean = self.mean / self.i
        std_mean = self.std / self.i
        rms_mean = self.rms / self.i
        self.report_file.write('Mean values: \t Mean: ' + self._xstr(mean_mean) + '\t Std: ' + self._xstr(std_mean) + '\t RMS: ' + self._xstr(rms_mean) + '\n')
        self.report_file.close()