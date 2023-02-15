## Python-Script for downloading videos and subtitles and scraping data of them

### necessary python packages: 
- os 
- shutil 
- pytube
- datetime
- time

---

### How to use it:
- download the python-scripts, the necessary python packages and python

- start YTget.py or YTgetc.py, if you dont want videos without subtitles, in a Code-Editor <br>
                        or <br>
    type "python YTget.py" or "python YTgetc.py" in the console, where the Python-Scripts are saved

- follow the instructions of the Script

- Go to the GoogleDoc of your group and import the produced new.csv into the selected cell

- delete the imported header

---

### Updates before git:


-> 22.12.2022: added videopath, downloading captions and number of sentences, estimated by the captions

-> 02.01.2023: to scrape a whole channel, create a playlist of all videos of the channel by pressing "Play all" on the overview of the Home of the channel

-> 04.01.2023: adding caption language code to caption filenames, skipping downloading captions from videos without captions and automatically downloading captions, if only one language is available; changing title, if the title repeats
