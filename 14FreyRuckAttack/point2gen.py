import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.point_generator import generate_point

k = sys.argv[1]
Q = generate_point(k)
print(Q)

