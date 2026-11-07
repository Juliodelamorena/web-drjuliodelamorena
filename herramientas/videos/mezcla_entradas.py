import subprocess, os
import entradas as E
SON = {
 "martes": [("beep.wav",0.45,0.8),("beep.wav",0.95,0.8),("riser.wav",0.4,0.7),("kick.wav",1.63,1),("kick.wav",2.13,1),("beep.wav",2.75,0.9),("beep.wav",2.95,0.9)],
 "miercoles": [("whoosh.wav",1.1,0.9),("whoosh.wav",1.6,0.9),("kick.wav",1.63,1),("kick.wav",2.13,1),("whoosh.wav",2.25,0.7),("clank.wav",2.75,1)],
 "jueves": [("riser.wav",0.1,0.6),("mito.wav",1.15,1.3),("kick.wav",1.48,1),("kick.wav",2.18,1),("ding.wav",2.75,0.8)],
 "viernes": [("flip.wav",0.05,0.9)]+[("click.wav",0.32+i*0.06,0.6) for i in range(14)]+[("kick.wav",1.63,0.7),("kick.wav",2.13,0.7),("kick.wav",2.72,1.0)],
 "sabado": [("riser.wav",0.2,0.9),("boom.wav",1.3,1.2),("kick.wav",1.83,0.9),("kick.wav",2.33,0.9)],
}
import sys
for nom, sons in [(k,v) for k,v in SON.items() if k in sys.argv[1:] or len(sys.argv)==1]:
    v = E.render(nom)
    args = ["ffmpeg","-v","error","-y","-i",v,"-i","../prp/musica_larga.wav"]
    for f,_,_ in sons: args += ["-i", f]
    fc = "[1]atrim=0:4.2,volume=0.18,afade=t=in:d=0.4,afade=t=out:st=3.7:d=0.5[m];"
    labs = ["[m]"]
    for i,(f,t,vol) in enumerate(sons):
        fc += f"[{i+2}]adelay={int(t*1000)}:all=1,volume={vol}[s{i}];"; labs.append(f"[s{i}]")
    fc += "".join(labs) + f"amix=inputs={len(labs)}:normalize=0,apad,atrim=0:4.2,alimiter=limit=0.9[a]"
    out = f"entrada-{nom}.mp4"
    subprocess.run(args+["-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out],check=True)
    print(out)
