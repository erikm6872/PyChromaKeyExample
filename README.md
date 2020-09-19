# PyChromaKey Example
Example project for [PyChromaKey](https://pypi.org/project/PyChromaKey/). Both the library and this project are heavily 
based on [this article](https://medium.com/fnplus/blue-or-green-screen-effect-with-open-cv-chroma-keying-94d4a6ab2743)
by Teja Kummarikuntla.

## Prerequisites
* opencv-python
* numpy
* pillow
* pyscreenshot
* pychromakey

## Usage
`$ python3 main.py`

Modify `constants.py` to change defaults.

## Limitations
Tested only on Windows 10. AFAIK it should work fine on Linux/OSX, but you may need to change the webcam initialization.
