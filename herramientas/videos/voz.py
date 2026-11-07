import json, urllib.request, subprocess, os
KEY=open('../dub/.key').read().strip(); V="FMUNJCsKXSdEGNKTCd7w"
F=["Lo que casi nadie te cuenta sobre la tendinitis.",
"En un tendón que lleva meses doliendo, casi nunca hay inflamación. Lo que hay es un tendón degenerado, que ha perdido calidad.",
"En mil novecientos noventa y nueve, el British Medical Journal ya pidió dejar de llamarla tendinitis.",
"Por eso los antiinflamatorios no la curan: alivian el dolor, pero el tendón sigue igual.",
"Lo que de verdad lo recupera es cargarlo de forma progresiva, con ejercicio bien dosificado.",
"El nombre sigue porque es fácil de decir… y de recetar."]
t=0.0; marks=[]
lst=open('list.txt','w')
for i,x in enumerate(F):
    mp=f"f{i}.mp3"
    if not os.path.exists(mp):
        body=json.dumps({"text":x,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.5,"similarity_boost":0.85}}).encode()
        r=urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":KEY,"Content-Type":"application/json"}))
        open(mp,'wb').write(r.read())
    w=f"f{i}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",mp,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.35","-ar","44100","-ac","1",w],check=True)
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",w],capture_output=True,text=True).stdout)
    marks.append([t,t+d-0.35,x]); t+=d; lst.write(f"file '{w}'\n")
lst.close()
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-i","list.txt","-c","copy","voz.wav"],check=True)
json.dump(marks,open('marks.json','w'),ensure_ascii=False); print(marks, t)
