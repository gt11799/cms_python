import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
from tools.kefu_performance import kefuPerformanceEffective

def temp_fix_missing_data():
    kefuPerformanceEffective(day = -10)
    kefuPerformanceEffective(day = -11)
    kefuPerformanceEffective(day = -12)
    kefuPerformanceEffective(day = -13)
    kefuPerformanceEffective(day = -14)

if __name__ == '__main__':
	temp_fix_missing_data()