"""Console script for isigraph."""
import sys
import click

from isigraph.isigraph import store


@click.command()
@click.argument('files', type=click.Path(exists=True, dir_okay=False), nargs=-1)
def main(files: list):
    """isigraph

    Load your isi files in your neo4j database.
    """
    store(files)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
