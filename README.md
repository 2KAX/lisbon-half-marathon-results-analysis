# Lisbon half marathon results analysis 🏁

This projects aim to explore the results of the 2025 Half Marathon of Lisbon. So far it can only compute the number of runners per country.

## Requirements

Python (with json, requests and tabulate dependencies)

## Compute the number of runners per country

In order to compute the number of runners per country use the following command :

```shell
python3.10 main.py
```

You should get a result that looks like this (only the top 10 is featured here).

```
Country code      Runner count
--------------  --------------
PT                        3849
GB                        2486
DE                        2012
ES                        1426
FR                        1228
IT                         835
DK                         711
IE                         569
BR                         524
NL                         467
```