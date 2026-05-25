import sys
import logging
import argparse
from commands import make, run


VERBOSE = 5
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs)

def main():
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.Logger.verbose = verbose
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['make', 'run'])
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--debug',   action='store_true')
    args = parser.parse_args()

    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = VERBOSE
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format="%(name)s: %(message)s")

    match args.command:
        case "make":
            make.execute()
        case "run":
            run.execute()

if __name__ == "__main__":
    main()