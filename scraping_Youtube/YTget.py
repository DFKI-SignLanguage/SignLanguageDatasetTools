# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:56:15 2022

@author: Fabian Deckert
"""

from pytube import YouTube, Playlist
import sv
import os, shutil
import datetime, time


def geturl(cp, a):
    
    if(cp == 'c'):
        c = Playlist(a)
        c_t = c.owner
        return c,c_t 
    else:
        p = Playlist(a)
        p_t = p.title
        return p,p_t
    
def createnewtitle(direc,name):
    if( os.path.exists(os.path.join(direc,name+".mp4")) == True):
        for i in range(6000):
            if( os.path.exists(os.path.join(direc,name+"_"+str(i)+".mp4")) == False): 
                return name+"_"+str(i)
    else:
        return name
            
        

def createdata(C_ID, Lang, dia, gran, a, lang_code, cp):
    
    p,p_t = geturl(cp, a)
    
    if(os.path.exists(p_t) == False):
        os.mkdir(p_t)
    else:
        shutil.rmtree(p_t)
        os.mkdir(p_t)
    
    os.mkdir(os.path.join(p_t , "captions"))
    os.mkdir(os.path.join(p_t , "videos"))
    os.mkdir(os.path.join(p_t , "videos_uncropped"))
    os.mkdir(os.path.join(p_t , "other"))
    
    for url in p.video_urls:
        try:
            yt = YouTube(url)
        except:
            print(f'\nVideo {url} is unavaialable, skipping.')
        else:
            print(f'\nDownloading video: {url}')
            
            #create variable for the title, which can used as filename
            titel = yt.title.replace("|", "").replace("\\", "") \
                        .replace("/", "").replace("\"", "").replace("?", "") \
                        .replace("*", "").replace(":", "").replace(">", "").replace("<", "")
            
            titel = createnewtitle(p_t,titel)
            #download the video
            try:
                stream = yt.streams.get_highest_resolution()
                yt.streams.get_highest_resolution().download(os.path.join(p_t , "videos_uncropped"),titel+".mp4")
            except:
                print(f'\nDownloading {url} is unavaialable, skipping.')
             
            #download captions
            l = ""
            lang_code = lang_code_s
            while(l == ""):
                if(lang_code == "" or len(yt.captions) == 0):
                    break
                elif(len(yt.captions) == 1):
                    lang_code = list(yt.captions.lang_code_index.keys())[0]
                    l = yt.captions[lang_code].xml_captions
                    d = open(os.path.join(p_t, "captions", titel+"_"+lang_code+".xml"), "x", encoding="utf-8")
                    d.write(l)
                    d.close
                else:
                    try:
                        l = yt.captions[lang_code].xml_captions
                        d = open(os.path.join(p_t, "captions", titel+"_"+lang_code+".xml"), "x", encoding="utf-8")
                        d.write(l)
                        d.close
                    except:
                        print("\n"+str(yt.captions))
                        lang_code = input("\nType in the language code for the captions or press enter: ")
                        

            # append Channel Id -> not codable
            data.append(C_ID)
            
            # append Language -> not codable
            data.append(Lang)
            
            # append Channel Dialect -> not codable
            data.append(dia)
            
            # append Channel Video Name
            data.append(str(titel))
            
            # append Part of Series -> not codable
            data.append("tbd")
            
            # append Url
            data.append(str(url))
            
            # append Release Date
            data.append(str(YouTube(url).publish_date.strftime("%Y/%m/%d")))
            
            # append Resolution
            data.append(str(stream.resolution))
            
            # append Cropped -> not codable
            data.append("tbd")
            
            # append Video Length
            i = 0
            while(i < 3):
                try:
                    t = YouTube(url).length
                    t_form = str(time.strftime("%H:%M:%S", time.gmtime(t)))
                    i = 3
                except Exception:
                    t_form = "tbd"
                i = i+1    
            data.append(t_form)
            
            # append FPS
            data.append(str(stream.fps))
            
            # append Number of Frames
            if(t_form != "tbd"):
                data.append(str(stream.fps*t))
            else:
                data.append("tbd")
            
            # append SL Subtitles Available -> not codable
            data.append("tbd")
            
            # append Audio Transcript Available -> not codable
            data.append("tbd")
            
            # append Granularity -> not codable
            data.append(gran)
            
            # append Number of sentences -> estimated
            if(l == ""):
                data.append("tbd")
            else:
                data.append(str(l.count(".<")+l.count("?<")+l.count("!<")+l.count(". ")+l.count("? ")+l.count("! ")))
             
            # append Date of Acquisition
            data.append(str(datetime.datetime.now().strftime("%Y/%m/%d")))
            
            # append File size
            data.append(str(stream.filesize_mb)+" MB")
            
            # append Video Path
            data.append(Lang+"\\"+p_t+"\\"+"videos_uncropped\\"+titel+".mp4")
    
    
    
    # write csv-file
    sv.writecsv( "new.csv", "|", titles, data)
    print("\nwrote csv-file")
    



titles = ["Channel Id",	"Language",	"Dialect","Video Name","Part of Series","Url","Release Date","Resolution","Cropped","Video Length","FPS","Number of Frames","SL Subtitles Available","Audio Transcript Available","Granularity","Number of Sentences","Date of Acquisition","File Size","Video Path"]
data = []


C_ID = input("\nType in the Channel ID from the GoogleSheet: ")
Lang = input("\nType in the sign language (SIL-code): ")
dia = input("\nType in the sign language dialect: ")
gran = input("\nType in the granularity (Sentences, Words or Phrases): ")

lang_code_s = input("\nType in the standard language code for the captions or press enter: ")

# for a whole channel use a playlist of all videos by pressing "alle wiedergeben" on YouTube
a = input("\nType in the Youtube playlist url: ")
cp = input("\nType in c for a playlist of a Channel or p for a normal playlist: ")

createdata(C_ID, Lang, dia, gran, a, lang_code_s, cp)