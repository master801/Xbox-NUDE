# Xbox-NUDE

N.U.D.E.@ Natural Ultimate Digital Experiment<br/>
![](https://upload.wikimedia.org/wikipedia/en/d/d3/N.U.D.E.%40Natural_Ultimate_Digital_Experiment_Coverart.png)

---
Unpacker and packer for `.tfs` files found in the Xbox game

## Usage
- `--extract` - Extract tfs file(s)
- `--create` - Create tfs file(s)
- `--input` - Input file or directory
- `--output` - Output directory or file

### Examples:

Extract tfs files in directory:
```
python main.py --extract --input=TFS --output=EXTRACTED
```
---

Create tfs from extracted:
```batch
python main.py --create --input=EXTRACTED --output=CREATED
```

Extract `SCENARIO.tfs`
```
python main.py --extract --input=SCENARIO.tfs --output=SCENARIO
```

Create `SCENARIO.tfs`
```batch
python main.py --create --input=SCENARIO --output=SCENARIO.tfs
```

## Requirements
* [Python 3.11.0](https://www.python.org/downloads/release/python-3110/)
* [kaitaistruct 0.10](https://pypi.org/project/kaitaistruct/0.10/)

---

## Built with:
 - [Kaitai Struct](https://kaitai.io/)
 - [PyCharm](https://www.jetbrains.com/pycharm/) 2023.1.1 RC (Community Edition)

## Thanks to:
 - [Wikipedia](https://en.wikipedia.org/wiki/N.U.D.E.@_Natural_Ultimate_Digital_Experiment) for the cover art
