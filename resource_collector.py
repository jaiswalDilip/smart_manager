import psutil
import argparse
import os
from time import gmtime, strftime


def main():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-t", "--totalDurationtimeInSecs", dest="totalDurationtimeInSecs", type=int,
                        default=10, help="Total Duration of script to run")
    parser.add_argument("-i", "--intervalInSecs", dest="intervalInSecs",
                        type=int, default=10, help="interval between 2 runs of data collection")
    parser.add_argument("-n", "--numberOfIterations", dest="numberOfIterations",
                        type=int, default=0, help="No. of iterations")
    parser.add_argument("-o", "--outputFile", dest="outputFile",
                        type=str, default="data.csv", help="Default o/p file")
    parser.add_argument("-d", "--debug", action="store_true", default=False)

    # Read arguments from command line
    args = parser.parse_args()
    if not args.numberOfIterations:
        total_iterations = int(args.totalDurationtimeInSecs) // int(args.intervalInSecs)
    else:
        total_iterations = args.numberOfIterations
        args.totalDurationtimeInSecs = args.intervalInSecs * total_iterations
    print("totalDurationtimeInSecs: %s \nintervalInSecs: %s \ntotal_iterations: %s" % (
        args.totalDurationtimeInSecs, args.intervalInSecs, total_iterations))
    with open(args.outputFile, "w") as fh:
        fh.write("timestamp,RAM_Usage_In_Percentage,CPU_Usage_In_Percentage,DISK_Usage_In_Percantage\n")
        for _ in range(total_iterations):
            ts = strftime("%a %d %b %Y %H:%M:%S +0000", gmtime())
            msg = "%s,%s,%s,%s" % (ts, psutil.virtual_memory()[2], psutil.cpu_percent(args.intervalInSecs),
                                     psutil.disk_usage(r"/").percent)
            fh.write("%s\n" % msg)
            if args.debug:
                print(msg)
    print("Output @ %s" % os.path.join(os.getcwd(), args.outputFile))


if __name__ == "__main__":
    main()


"""
Usage
python3 resource_collector.py -t 30 -i 10 --debug
"""