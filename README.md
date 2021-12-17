# About

This is POC code of voice recognition by using MFCC + GMM and was inspried by https://github.com/MohamadMerchant/Voice-Authentication-and-Face-Recognition

# Data
Data is from: https://www.kaggle.com/nltkdata/timitcorpus and splitted into training data and testing data.
- Training data is in folder `voice_databse`, 9 file .wav each person
- Testing data is in folder `recognize`, 1 file .wav each person

# Run code
1. To register all from files in `./voice_databse`:
```bash
$ python register_all.py
```
2. To recognize from file:
```bash
$ python recognize.py $filename
```
For example
```bash
$ python recognize.py ./recognize/dr2-faem0/sa1.wav
```
3. To recognize all files in `./recognize` folder. 
```bash
$ python recognize_all.py > output.txt
```
The output will be written to output.txt

4. To test recognize unknown with mic
```bash
$ python recognize.py
```