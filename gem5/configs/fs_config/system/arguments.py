import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu-type", default="atomic", help="atomic, simple or o3")
    parser.add_argument("--cpu-num", default=1, help="Number of cpus")

    parser.add_argument("--kernel", help="Path of the kernel")
    parser.add_argument("--image", help="Path of the image")

    return parser.parse_args()