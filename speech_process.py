import sys
import os
from moviepy.editor import VideoFileClip
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
# 1. 将文件夹中的所有mp4文件转成wav文件

target_folder = 'Onmoji'
def get_files(path, file_list, end_with):
    for file in os.listdir(path):
        fs = os.path.join(path, file)
        if os.path.isfile(fs) and fs.endswith(end_with):
            file_list.append(fs)
        elif os.path.isdir(fs):
            get_files(fs, file_list, end_with)

mp4_files = []
get_files(target_folder, mp4_files, end_with=".mp4")

for mp4_file in mp4_files:
    mp4_path = os.path.join('', mp4_file)
    audio_clip = VideoFileClip(mp4_path)
    audio_clip.audio.write_audiofile(mp4_path.replace('.mp4', '.wav'))

print("Convert Complete!")

audio_type = 'wav'
# 2. 把所有的wav文件根据静默切断
wav_files = []
get_files(target_folder, wav_files, ".wav")
for wav_file in wav_files:
    sound = AudioSegment.from_wav(wav_file)
    print("开始分割")
    chunks = split_on_silence(sound,min_silence_len=300,silence_thresh=-70)
    filepath = os.path.split(wav_file)[0]
    print(filepath)
    chunks_path = filepath + '/chunks/'
    if not os.path.exists(chunks_path):os.mkdir(chunks_path)
    # 保存所有分段
    print('开始保存')
    for i in range(len(chunks)):
        new = chunks[i]
        save_name = chunks_path+'%04d.%s'%(i, audio_type)
        new.export(save_name, format=audio_type)
        print('%04d'%i,len(new))
    print('保存完毕')


