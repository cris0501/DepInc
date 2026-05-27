import sys
import logging
import argparse
from commands import make, run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['make', 'run'])
    parser.add_argument('--debug',   action='store_true')
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO

    logging.basicConfig(level=level, format="[%(name)s] %(message)s")

    match args.command:
        case "make":
            make.execute()
        case "run":
            run.execute()

if __name__ == "__main__":
    main()