from pydub import AudioSegment

pad_ms = 1000  # milliseconds of silence needed
silence = AudioSegment.silent(duration=pad_ms)
audio = AudioSegment.from_wav('thu4.wav')

padded = audio + silence  # Adding silence after the audio
padded.export('padded-file.wav', format='wav')