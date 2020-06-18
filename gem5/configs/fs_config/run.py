import os

import m5
import m5.ticks
from m5.objects import *
from system.arguments import get_arguments

from system import *
import argparse

if __name__ == "__m5_main__":
    args = get_arguments()
    
    kernel, image, cpu_type, num_cpus = args.kernel, args.image, args.cpu_type, args.cpu_num
    system = MySystem(kernel, image, cpu_type, num_cpus)
    root = Root(full_system = True, system = system)

    m5.instantiate()

    print("Running the simulation")
    exit_event = m5.simulate()

    if exit_event.getCause() != "m5_exit instruction encountered":
        print("Failed to exit correctly")
        exit(1)
    else:
        print("Success!")
        exit(0)