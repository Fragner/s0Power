#checkinput arguments
import argparse


parser = argparse.ArgumentParser(description='only -v or --verbose supported')
parser.add_argument("-v", '--verbose', type=int, nargs='?', help='with 1 or none debug is active, with 0 = debug isn\'t active ', default=0)
parser.add_argument("-f", '--force', type=float, nargs='?', help='force actual produce power', default=None)
inputArgs = parser.parse_args()