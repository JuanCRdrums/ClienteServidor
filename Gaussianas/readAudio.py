import wave

file = wave.open("Synth Loop.wav",'rb')
nframes = file.getnframes()
frames = file.readframes(nframes)
print(frames[9150037])
