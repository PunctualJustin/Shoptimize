# Shoptimize

Optmize shopping carts accross a number of stores.

Currently a CLI that produce a report to identify the selections from stores and their associated costs.

## Usage

There are 2 driver files; `src/main.py`, and `src/make_basket/main.py`

The 2 drivers serve to perform the main optimization function, and manage stores and items, respectively.

The basket of items and their associated stores are stored in `./inputs/items.json`

### Add items

To make add items and stores, run:

```
$ python ./src/make_basket/main.py
```

and follow the instructions

If you prefer, you can edit the `items.json` file direction, in the `inputs` directory.

### Optimize

To find out what stores you will get the best value for which items, run:


```
$ python ./src/main.py
```

## Future Improvements:
- A unified driver to run both the `make_basket` script and `optimize` scripts
- Load and store `items` file to a custom path
- `items` constructor to remove the need to start with a seed file.
- A GUI to make input simpler
