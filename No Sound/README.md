# wb_mapper
A program to search the War Brokers server list for servers that match a specified number of players, game mode, map, or region. No sound notification feature for less python modules.

Browser Version [here](https://github.com/paperblock01/War-Brokers-Mapper-for-Browser).

# Requirements
`python3`

Python Modules: `requests`, `time`, `getopt`, `sys`

`python3 -m pip install requests time getopt sys`

# Install

To Download:

* Click the file.

* Press the download button on the right that says "Download raw file"

### Windows:

Install `python3` for windows: [here](https://www.python.org/downloads/windows/)

Download the `wb_mapper.py` file

Open `cmd.exe`

`cd` to the folder you downloaded it to

Execute `python3 wb_mapper.py`

### Linux and Mac:

Download the `wb_mapper.py` file

Open the terminal

`cd` to the directory you downloaded it to

Execute `python3 wb_mapper.py`

### ChromeOS:

Browser Version [here](https://github.com/paperblock01/War-Brokers-Mapper-for-Browser).

# Usage
### NOTE: Servers with no human players are NOT detected

Running with no arguments will scan every server in the Classic game mode

To stop the program, press `CTRL` + `C` or `Command` + `C` if you are on a Mac

```
-h, --help              Display this help message

-f, --forever           Include this argument and the program will map servers until
                        the user stops it manually.

-g, --game=             Specify the game. Default is classic.

    classic
    4v4

-p, --players=          Specify the players in the server. The sign is the first
                        character and the number of players follows. The number of
                        players cannot equal Zero.

    -p [sign][number]

    [sign]
    L : Less than or equal to
    G : greater than or equal to

    -p L10
    -p G4

-m, --mode=             Specify a mode. Write ONLY the shorthand. If spaces are
                        included, put in quotes. The default is all modes. Works
                        only when classic is selected.

-a, --map=              Specify a map. If spaces are included, put in quotes.
                        The default is all maps.

-r, --region=           Specify a region. If spaces are included, put in quotes.
                        Only regions in the chosen game are accepted.
```

Example:

`python3 wb_mapper.py -f`

`python3 wb_mapper.py -g 4v4` `python3 wb_mapper.py --game=4v4`

`python3 wb_mapper.py -p G8` `python3 wb_mapper.py --players=L8`

* Mode, Map, and Region data is case insensitive as long as there is a comma:

`python3 wb_mapper.py -m "g g,Ml, B    D"` `python3 wb_mapper.py -m GG,ml,bd` `python3 wb_mapper.py --mode="gg, ml, bd"`

`python3 wb_mapper.py -a "Frontier, TRIBUTE"` `python3 wb_mapper.py -a Frontier,Tribute` `python3 wb_mapper.py --map="Frontier, Tribute"`

`python3 wb_mapper.py -r "europe, usa, usa_west, asia"` `python3 wb_mapper.py -r Europe,USA,USA_west,asia` `python3 wb_mapper.py --region=EUrope`

