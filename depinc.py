import argparse
from commands import make, run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="depinc")
    subparsers = parser.add_subparsers(dest="command")

    # make command
    make_parser = subparsers.add_parser("make", help="Artefacts generator")
    make_parser.add_argument("type", choices=["adapter"])
    make_parser.add_argument("--ent", action="store_true")
    make_parser.add_argument("--out", action="store_true")
    make_parser.add_argument("-d", "--dir", default="generated")
    make_parser.add_argument("--force", action="store_true")
    make_parser.add_argument("--register", action="store_true")
    make_parser.add_argument("name")

    # run command
    run_parser = subparsers.add_parser("run", help="Ejecuta el adaptador configurado")
    run_parser.add_argument("--adapter", choices=["http", "cli"], default="http")

    args = parser.parse_args()

    match args.command:
        case "make":
            make.execute(args)
        case "run":
            run.execute()
        case _:
            parser.print_help()