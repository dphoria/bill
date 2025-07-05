import click
from images import load_image
from receipts import get_items
from csv import DictWriter


@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.argument("csv", type=click.Path(exists=False))
def write_csv(image, csv):
    items = get_items(load_image(image))

    with open(csv, "w", newline="") as csv_file:
        field_names = ["name", "price"]
        writer = DictWriter(csv_file, fieldnames=field_names, extrasaction="ignore")

        for item in items.items:
            writer.writerow({"name": item.name, "price": item.price})
            click.echo(f"{item.name}, {item.price}")

        csv_file.write("\n")

        subtotal = items.get_sum()
        writer.writerow({"name": "Subtotal", "price": subtotal})
        click.echo(f"Subtotal, {subtotal}")
        tax = subtotal * 0.1035
        writer.writerow({"name": "Tax", "price": tax})
        click.echo(f"tax, {tax}")


if __name__ == "__main__":
    write_csv()
