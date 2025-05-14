import sys
from commands import make, run

def main():
    if len(sys.argv) < 2:
        print("Uso: python depinc.py [make|run]")
        return

    command = sys.argv[1].lower()

    match command:
        case "make":
            make.execute()
        case "run":
            run.execute()
        case _:
            print(f"Comando desconocido: {command}")
            print("Comandos disponibles: make, run")

if __name__ == "__main__":
    main()