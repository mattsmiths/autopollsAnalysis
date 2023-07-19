# autopollsAnalysis
Basic analysis for output of autopolls

This script will take the raw output from Autopolls systems and generate:
1. Videos detections above a set threshold of confidence (0.5 by default)
2. CSVs with detection data (datetime, etc.) for detections above a set confidence
3. Figures of detections over time

This code is being actively developed and looking for feedback for analysis that would be helpful to include.

You can run the file using terminal on linux or mac with an example below. The input is the directory path to call the python script itself, then a flag "-d" followed by the directory path to the data you would like to run the script over.
If you add a "-v" at the end, it'll generate a video with bounding boxes for images / detections above 0.5 confidence. You can modify the confidence threshold with a "-t" flag followed by whatever value you'd like.
After running in terminal, there should be texting describing where the data is being saved.
```
python ~/Downloads/apProcess.py -d '~/AutoPolls2/AP_20220803/AP12/' -v
```
