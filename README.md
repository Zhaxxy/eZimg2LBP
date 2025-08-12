# eZimg2LBP
Windows only tool to convert images to sticker mod files for Craftworld Toolkit

![eZimg2LBP.png](https://github.com/Zhaxxy/eZimg2LBP/blob/main/eZimg2LBP.png)

# requirements
Make sure you are using python3.11 on Windows
<br>
<br>
Make sure to pip install the requirements
```
pip install -r requirements.txt
```

# usage
## gui
run the `gui.py` file be either double clicking, or
```
python gui.py
```

## cli
```
usage: Windows only tool to convert images to sticker mod files for Craftworld Toolkit [-h] [-d DESCRIPTION]
                                                                                       [-u USERNAME] [-s] -i IMAGES
                                                                                       [IMAGES ...]
                                                                                       output_mod

positional arguments:
  output_mod            output of finished mod file, eg out.mod

options:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        optional description of the stickers
  -u USERNAME, --username USERNAME
                        optional set username of the stickers
  -s, --show-extensions
                        do you want the stickers to include the extensions? eg my_image.png instead of my_image
  -i IMAGES [IMAGES ...], --images IMAGES [IMAGES ...]
                        images to convert to a craftworld toolkit mod file

```
