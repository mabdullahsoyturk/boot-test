import errno
import os
import sys
import time

import m5
import m5.ticks
from m5.objects import *

sys.path.append('gem5/configs/common/') # For the next line...
import SimpleOpts

from system import *

SimpleOpts.set_usage("usage: %prog [options] kernel disk cpu_type mem_sys num_cpus boot_type")

SimpleOpts.add_option("--allow_listeners", default=False, action="store_true", help="Listeners disabled by default")

if __name__ == "__m5_main__":
    (opts, args) = SimpleOpts.parse_args()

    if len(args) != 6:
        SimpleOpts.print_help()
        m5.fatal("Bad arguments")

    kernel, disk, cpu_type, mem_sys, num_cpus, boot_type = args
    num_cpus = int(num_cpus)

    # create the system we are going to simulate
    if mem_sys == "classic":
        system = MySystem(kernel, disk, cpu_type, num_cpus, opts)
    elif mem_sys == "ruby":
        system = MyRubySystem(kernel, disk, cpu_type, num_cpus, opts)
    else:
        m5.fatal("Bad option for mem_sys, should be 'ruby' or 'classic'")

    # set up the root SimObject and start the simulation
    root = Root(full_system = True, system = system)

    # Required for long-running jobs
    if not opts.allow_listeners:
        m5.disableAllListeners()

    # instantiate all of the objects we've created above
    m5.instantiate()

    print("Running the simulation")
    exit_event = m5.simulate()

    if exit_event.getCause() != "m5_exit instruction encountered":
        print("Failed to exit correctly")
        exit(1)
    else:
        print("Success!")
        exit(0)
