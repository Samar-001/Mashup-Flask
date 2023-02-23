from flask import Flask, request,redirect,render_template,send_file
from pytube import YouTube
import pydub 
import urllib.request
import re
import os
import sys
import logging

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])

def index():
    delete_after_use = True                              
    if(request.method=='POST'):
        x = request.form['singer']
        n = int(request.form['song_count'])
        y = int(request.form['duration'])
        output_name = request.form['output']

        x = x.replace(' ','') + "songs"
        output_name = output_name + ".mp3"

        html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                                                        
        for i in range(n):
            yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
            mp4files = yt.streams.filter(only_audio=True).first().download(filename='audio_'+str(i)+'.mp3')

        if os.path.isfile(str(os.getcwd())+"\\audio_0.mp3"):
            try:
                fin_sound = pydub.AudioSegment.from_file(
                    str(os.getcwd())+"\\audio_0.mp3", format='mp3')[20000:(y*1000+20000)]
            except:
                fin_sound = pydub.AudioSegment.from_file(
                    str(os.getcwd())+"\\audio_0.mp3", format='mp4')[20000:(y*1000+20000)]
            for i in range(1, n):
                aud_file = str(os.getcwd())+"\\audio_"+str(i)+".mp3"
                fin_sound = fin_sound.append(pydub.AudioSegment.from_file(aud_file)[20000:(y*1000+20000)], crossfade=1000)
    
        try:
            fin_sound.export(output_name, format="mp3")
        except:
            sys.exit("Error while saving the file. Try a differrent file name.")
            
        if delete_after_use:
            for i in range(n):
                os.remove("audio_"+str(i)+".mp3")
        
        # if(send_file(path_or_file = str(os.getcwd())+"\\"+output_name, mimetype = "audio/mpeg", as_attachment=True)):
        #     os.remove(output_name)

        return redirect("/success")
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template("success.html")

if __name__=='__main__':
    app.run()