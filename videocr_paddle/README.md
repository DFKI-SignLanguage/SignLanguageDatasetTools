# Hardcoded subtitle extractor
A package, based on `PaddleOCR`, used to detect and recognise hardcoded(burned-in) subtitles from videos and save them to .srt files.
(Previous tested package, video OCR using `Tesseract`, showed worse result in speed and accuracy.)
- With multiprocessing tools, it took 18 minutes running on 52 short videos with a total duration of 1 hour.
- Worth a try if you have a video with hardcoded subtitles and it's not available to use so far.

## Description

Input:
videos with hardcoded subtitles
<p float="left">
	<img width="500" alt="output1" src="https://user-images.githubusercontent.com/45097812/217612460-d85d3bc0-b216-4159-b3b0-2e6553f0a921.png">
	<img width="500" alt="output3" src="https://user-images.githubusercontent.com/45097812/217612685-cfb95381-27dc-46e5-aaff-925402830012.png">
</p>
Output: text file in .srt format per video.
<p float="left">
	<img width="500" alt="output2" src="https://user-images.githubusercontent.com/45097812/217612666-0f59e8d0-8afe-4441-a9dc-d7439a52a514.png">
	<img width="500" alt="output4" src="https://user-images.githubusercontent.com/45097812/217612698-98bd12d9-287e-4d0e-ab86-0d04e1ced163.png">
</p>

Notes:
- Due to the issue locking in parallelised processing, progress bar looks quite ugly, but works ok.
<p float="left">
	<img width="500" alt="Screenshot 2023-02-08 at 19 25 50" src="https://user-images.githubusercontent.com/45097812/217619875-85735176-c719-4c72-b9b1-1ab00263e72b.png">
	
</p>

## Getting Started
Guide:
- First try to change only `DIR_PATH`, `VIDEO_TYPE`, `lang`, with other parameters fixed.

## Dependencies
- Python 3.7 or 3.8 (Other vestions not tested)
- paddlepaddle
- videocr
- tqdm
- parmap

## Installation
0. Prepare CLI on your environment (local, conda ..)
   
1. Setup PaddlePaddle (in case CPU)
```
pip install paddlepaddle==2.3.1 -i https://mirror.baidu.com/pypi/simple
```

2. (Optional) Setup PaddlePaddle-GPU (only in case GPU, recommended if you have a CUDA 9 or CUDA 10 GPU.)
```
pip install paddlepaddle-gpu==2.3.1.post112 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
```

3. Install parmap
```
pip install parmap
```
   
4. Setup videocr
```
pip install git+https://github.com/taekko/videocr_paddle.git
```

## Run on CLI
1.  Go to where `config.json` and `run.py` are located.
2. Fix .json configuration file (see appendix below)
3. Run `python3 run.py`

## Sample `config.json`
```
{	
	"DIR_PATH": "/Users/taekwon.rhee/Documents/Uni/Q&U project/script/slt/scraping/Maria Ortiz (temp)/lowcut/cropped/test2",
	"VIDEO_TYPE": ".mp4",

	"language_code": "es",
	"use_gpu": 0,

	"start_time": "00:00",
	"end_time": "",

	"confidence_threshold": 75,
	"similarity_threshold": 20,

	"use_fullframe": 1,
	"frames_to_skip": 5,

	"crop_x": 0,
	"crop_y": 0,
	"crop_width": 0,
	"crop_height": 0,

	"similar_image_threshold": 100,
	"similar_pixel_threshold": 25

}
```
The sample `DIR_PATH` looks like this:
<p float="left">
	<img width="500" alt="Screenshot 2023-02-08 at 19 45 46" src="https://user-images.githubusercontent.com/45097812/217623398-477b2fd4-38d6-43e1-a980-71885b733033.png">
</p>


## (Appendix_1) Parameters
- `DIR_PATH`
  Path where the target vidoes are located.
  
- `VIDEO_TYPE`
  The specified extension of the videos (e.g. .mp4)
  
- `lang`
  The language of the subtitles. (See below: Support languages and abbreviations)

- `conf_threshold`
  Confidence threshold for word predictions. Words with lower confidence than this value will be discarded. The default value `75` is fine for most cases. 

  Make it closer to 0 if you get too few words in each line, or make it closer to 100 if there are too many excess words in each line.

- `sim_threshold`
  Similarity threshold for subtitle lines. Subtitle lines with larger [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance) ratios than this threshold will be merged together. The default value `80` is fine for most cases.

  Make it closer to 0 if you get too many duplicated subtitle lines, or make it closer to 100 if you get too few subtitle lines.

- `time_start` and `time_end`
  Extract subtitles from only a clip of the video. The subtitle timestamps are still calculated according to the full video length.

- `use_fullframe`
  By default, the specified cropped area is used for OCR or if a crop is not specified, then the bottom third of the frame will be used. By setting this value to `True` the entire frame will be used.

- `crop_x`, `crop_y`, `crop_width`, `crop_height`
  Specifies the bounding area in pixels for the portion of the frame that will be used for OCR.

- `det_model_dir`
  the text detection inference model folder. There are two ways to transfer parameters, 1. None: Automatically download the built-in model to ~/.paddleocr/det; 2. The path of a specific inference model, the model and params files must be included in the model path.
  
  See PaddleOCR repo for list of prebuilt models: https://github.com/PaddlePaddle/PaddleOCR/.

- `rec_model_dir`
  the text recognition inference model folder. There are two ways to transfer parameters, 1. None: Automatically download the built-in model to ~/.paddleocr/rec; 2. The path of a specific inference model, the model and params files must be included in the model path.
  
  See PaddleOCR repo for list of prebuilt models: https://github.com/PaddlePaddle/PaddleOCR/.

- `use_gpu`
  Set to `True` if performing ocr with gpu (requires the `paddlepaddle-gpu` python package to be installed)

- `brightness_threshold`
  If set, pixels whose brightness are less than the threshold will be blackened out. Valid brightness values range from 0 (black) to 255 (white). This can help improve accuracy when performing OCR on videos with white subtitles.

- `similar_image_threshold`
  The number of non-similar pixels there can be before the program considers 2 consecutive frames to be different. If a frame is not different from the previous frame, then the OCR result from the previous frame will be used (which can save a lot of time depending on how fast each OCR inference takes).

- `similar_pixel_threshold`
  Brightness threshold from 0-255 used with the `similar_image_threshold` to determine if 2 consecutive frames are different. If the difference between 2 pixels exceeds the threshold, then they will be considered non-similar.

- `frames_to_skip`
  The number of frames to skip before sampling a frame for OCR. Keep in mind the fps of the input video before increasing.


## (Appendix_2) 5 Support languages and abbreviations

| Language  | Abbreviation | | Language  | Abbreviation |
| ---  | --- | --- | ---  | --- |
|Chinese & English|ch| |Arabic|ar|
|English|en| |Hindi|hi|
|French|fr| |Uyghur|ug|
|German|german| |Persian|fa|
|Japan|japan| |Urdu|ur|
|Korean|korean| | Serbian(latin) |rs_latin|
|Chinese Traditional |chinese_cht| |Occitan |oc|
| Italian |it| |Marathi|mr|
|Spanish |es| |Nepali|ne|
| Portuguese|pt| |Serbian(cyrillic)|rs_cyrillic|
|Russia|ru||Bulgarian |bg|
|Ukranian|uk| |Estonian |et|
|Belarusian|be| |Irish |ga|
|Telugu |te| |Croatian |hr|
|Saudi Arabia|sa| |Hungarian |hu|
|Tamil |ta| |Indonesian|id|
|Afrikaans |af| |Icelandic|is|
|Azerbaijani  |az||Kurdish|ku|
|Bosnian|bs| |Lithuanian |lt|
|Czech|cs| |Latvian |lv|
|Welsh |cy| |Maori|mi|
|Danish|da| |Malay|ms|
|Maltese |mt| |Adyghe |ady|
|Dutch |nl| |Kabardian |kbd|
|Norwegian |no| |Avar |ava|
|Polish |pl| |Dargwa |dar|
|Romanian |ro| |Ingush |inh|
|Slovak |sk| |Lak |lbe|
|Slovenian |sl| |Lezghian |lez|
|Albanian |sq| |Tabassaran |tab|
|Swedish |sv| |Bihari |bh|
|Swahili |sw| |Maithili |mai|
|Tagalog |tl| |Angika |ang|
|Turkish |tr| |Bhojpuri |bho|
|Uzbek |uz| |Magahi |mah|
|Vietnamese |vi| |Nagpur |sck|
|Mongolian |mn| |Newari |new|
|Abaza |abq| |Goan Konkani|gom|
- source: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/multi_languages_en.md#language_abbreviations




## References
- https://github.com/oliverfei/videocr-PaddleOCR
- https://github.com/PaddlePaddle/PaddleOCR


