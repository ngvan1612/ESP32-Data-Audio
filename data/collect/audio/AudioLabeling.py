from ..esp32.udp_audio import Esp32AudioUDP
from .AudioProcessing import AudioProcessing
import json
import os

class AudioLabeling:
    
  def __init__(self, seconds) -> None:
    self.seconds = seconds
    self.esp32_audio = Esp32AudioUDP()
    self.esp32_audio.begin()
  
  def begin(self, output_dir):
    print("Ghi đầu ra:", self.seconds, "giây")
    label_name = input('Nhập tên nhãn').strip()

    if not label_name:
      print('Tên nhãn không được trống!')
      return
    
    out = os.path.join(output_dir, label_name)
    if os.path.exists(out):
      print('Nhãn đã tồn tại')
      return
    
    os.makedirs(out, exist_ok=True)

    data = self.esp32_audio.start_recording(self.seconds)
    AudioProcessing.write_wav(data, os.path.join(out, "audio.wav"))

    data = AudioProcessing.reduce_noise(data)
    AudioProcessing.write_wav(data, os.path.join(out, "audio.reduced-noise.wav"))

    chunks = AudioProcessing.split_audio(data)

    output_arr = []

    for i, chunks in enumerate(chunks):
      AudioProcessing.write_wav(data, os.path.join(out, f"audio.chunk.{i}.mp3"))

      while True:
        answer = input('Đúng không? [y/n]').strip().lower()
        if answer in ['y', 'n']:
          break

      if answer == 'y':
        output_arr.append({
          'chunk': i,
          'accepted': True
        })
      else:
        output_arr.append({
          'chunk': i,
          'accepted': False
        })
    
    with open(os.path.join(out, "audio.config.json"), 'w', encoding='utf-8') as f:
      json.dump(output_arr, f, indent=2)


