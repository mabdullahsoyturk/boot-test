import errno
import os
import sys
import time

import m5
import m5.ticks
from m5.objects import *

from system import *
import argparse

if __name__ == "__m5_main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-listeners", default=False, action="store_true", help="Listeners disabled by default")
    parser.add_argument("--cpu-type", default="atomic", help="atomic, simple or o3")
    parser.add_argument("--cpu-num", default=1, help="Number of cpus")

    parser.add_argument("--kernel", help="Path of the kernel")
    parser.add_argument("--image", help="Path of the image")

    args = parser.parse_args()

    kernel = args.kernel
    image = args.image
    cpu_type = args.cpu_type
    num_cpus = args.cpu_num

    # create the system we are going to simulate
    system = MySystem(kernel, image, cpu_type, num_cpus, opts)

    # set up the root SimObject and start the simulation
    root = Root(full_system = True, system = system)

    # Required for long-running jobs
    if not args.allow_listeners:
        m5.disableAllListeners()

    m5.instantiate()

    print("Running the simulation")
    exit_event = m5.simulate()

    if exit_event.getCause() != "m5_exit instruction encountered":
        print("Failed to exit correctly")
        exit(1)
    else:
        print("Success!")
        exit(0)
