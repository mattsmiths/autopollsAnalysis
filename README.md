# autopollsAnalysis
Basic analysis for output of autopolls

This script will take the raw output from Autopolls systems and generate:
1. Videos detections above a set threshold of confidence (0.5 by default)
2. CSVs with detection data (datetime, etc.) for detections above a set confidence
3. Figures of detections over time

This code is being actively developed and looking for feedback for analysis that would be helpful to include.

You can run the file using terminal on linux or mac with an example below. The input is the directory path to call the python script itself, then a flag "-d" followed by the directory path to the data you would like to run the script over.
Additional flags and functions:
  * -d : directory path to the storage location of the data to be processed, please use full directory paths at this time
  * -t : the threshold for a detection to be included in output (0.45 by default)
  * -v : generate a video with bounding boxes for images / detections, default is detections above 0.5 confidence.
  * -f : makes histograms of detections across time (per day)
After running in terminal, there should be texting describing where the data is being saved.
```
python /home/User/Downloads/apProcess.py -d '/Untitled/AutoPolls2/AP_20220803/AP12/' -v -t 0.6
```
The above command will look through the provided directory path to find subdirectories that include the detection JSON files, it will then create an output folder structure and begin to populate with CSVs of detections above a 0.6 confidence. Lastly, another output folder will be generated that contains videos of detections above 0.6 with bounding boxes overlayed.


The detectionRate.py script can take the output of the apProcess script and generate CSVs per camera per day at a given threshold. By default, rates starting at 5am to midnight are generated, independent of when the system is turned on. The threshold for inclusion and bin size can be modified as following:

* -d : full directory path to the newly generated CSVs from the APprocess script
* -b : the bin size for detection rate in seconds (300 by default)
* -t : threshold for including detection (0.45 by default)

```
python /home/User/Downloads/detectionRate.py -d '/home/User/Downloads/APprocess/APcsv/' -b 600 -t 0.6
```
The above command will create a new folder with CSVs of detection rate per camera per day with a rate calculate across 10 minute intervals of detections above 0.6.
