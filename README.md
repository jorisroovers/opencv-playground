# opencv-playground
Personal playground for opencv.

Each subdirectory contains some simple python code that I've been playing around with. The ```images``` directory

All scripts can be executed directly.

For example:
```
python circles/circles.py circles/coins.png
```

Code is usually poor quality as it's mostly meant as for learning purposes.

## Installation ##

You will need to install OpenCV:
On Mac:
```
brew tap homebrew/science
brew install opencv
```
Then modify your ```PYTHONPATH``` to include OpenCV:

```
export PYTHONPATH="$PYTHONPATH;/usr/local/Cellar/opencv/2.4.10/lib/python2.7/site-packages"
```

Finally, install all python requirements.txt:
```
pip install -r requirements.txt
```