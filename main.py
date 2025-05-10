from infrastructure.container import Container
from adapters.ent.cli_adapter import CLIAdapter

if __name__ == "__main__":
    container = Container()
    cli = CLIAdapter(container.flight_service)
    cli.run()