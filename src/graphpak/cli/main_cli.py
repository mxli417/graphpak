import typer
from typing_extensions import Annotated
import logging
from rich import print
from rich.prompt import Prompt, Confirm
from graphpak.kraken import KNGConstructor
from graphpak.visualizers.plotting import kng2plot
from graphpak.io.serialization.triplets import kng2csv
from graphpak.utils.misc.cli_banners import banner
from pathlib import Path

# run cli app
print(f"[green]{banner()}[green]")
app = typer.Typer(help="Awesome graphpak CLI!")


@app.command()
def krakenize(text: Annotated[str, typer.Option(help="The text you want to have processed")] = None):
    """Process the text coming from input-side in terminal into a graphpak kng-like structure, plot and store it.

    Args:
        text_input (Annotated[str, typer.Option, optional): The text you want to have processed. Defaults to None.
    """
    # TODO: (optional) push silent mode into cli options
    print(":high_voltage: [green] Welcome to graphpak - processing your request![/green] :high_voltage:")
    if text is not None and len(text) > 0:
        ger_kng = KNGConstructor(language="ger", ctype="rule-based")
        kng_triples = ger_kng(text)
        assert kng_triples is not None, f"Could not process your text into a valid output"
        assert all(
            [el.get("subject") is not None for el in kng_triples]
        ), f"Package-Error: subject must be part of every kng triple"
        assert all(
            [el.get("object") is not None for el in kng_triples]
        ), f"Package-Error: object must be part of every kng triple"
        assert all(
            [el.get("relation") is not None for el in kng_triples]
        ), f"Package-Error: relation must be part of every kng triple"
        # printouts
        print(f"We found the following triples: \n")
        for triple in kng_triples:
            print(f"\t {triple} \t")
        # ask if the user wants to store the graph plot
        get_plot = Confirm.ask(":open_book: Do you want to store a graph plot as *.png?")
        if get_plot:
            # ask for plot fpath
            fpath = Prompt.ask(":open_book: Please enter the plot output path+filename: ", default="kng_plt.png")
            kng2plot(
                kng_triples=kng_triples,
                fpath=Path(fpath),
                silent=False,
            )
        else:
            kng2plot(
                kng_triples=kng_triples,
                fpath=None,
                silent=False,
            )
        # ask if the user wants to store the graph data
        get_data = Confirm.ask(":open_book: Do you want to store the graph data as *.csv?")
        if get_data:
            # ask for plot fpath
            fpath = Prompt.ask(":open_book: Please enter the graph data dump path+filename: ", default="kng_dump.csv")
            kng2csv(
                kng_triples=kng_triples,
                fpath=Path(fpath),
                encoding="utf-8",
            )
        # goodbye
        print(":coffee: [green]Goodbye![/green] :coffee:")
    else:
        print(":collision: [bold red]Cannot process empty string![/bold red]:collision:")
