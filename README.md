# Shoptimize

Optmize shopping carts accross a number of stores.

Currently a CLI with a rough report.

## Usage

There are 2 driver files; `src/main.py`, and `src/make_basket/main.py`

The 2 drivers serve to perform the main optimization function, and manage stores and items, respectively.

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
