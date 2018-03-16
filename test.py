from CorrespondingStripsComparer import CorrespondingStripsComparer
from OverlappingStripsComparer import OverlappingStripsComparer
from StripsFabric import StripsFabric
import os

script_dir = os.path.dirname(__file__)
strips_folder = "ground_buildings"
absolute_path = os.path.join(script_dir,strips_folder)

stripsFabric = StripsFabric(absolute_path,"strips.txt")
#correspondingStripsComparer = CorrespondingStripsComparer(stripsFabric, "test_result")
#correspondingStripsComparer.compare()

overlappingStripsComparer = OverlappingStripsComparer(stripsFabric, "overlapping_test_result")
overlappingStripsComparer.compare()