import noisereduce as nr
import scipy.io.wavfile
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

class AudioProcessing:
    
    def __init__(self) -> None:
      pass

    @staticmethod
    def reduce_noise(buffer):
      temp = nr.reduce_noise(y=buffer, sr=16000)
      temp = temp / max(np.max(temp), abs(np.min(temp))) * 32767
      return np.array(temp, dtype=np.int16)
    
    @staticmethod
    def write_wav(buffer, output_file_name: str):
      scipy.io.wavfile.write(output_file_name, 16000, buffer)
    

    @staticmethod
    def split_audio(buffer: np.ndarray, reduced_noise=True):
      if not reduced_noise:
        buffer = reduced_noise(buffer)

      audio_segment = AudioSegment(
        buffer.tobytes(),
        frame_rate=16000,
        sample_width=2,
        channels=1
      )

      chunks = split_on_silence(
        audio_segment,
        min_silence_len=200,
        silence_thresh=-50,
        keep_silence=200
      )

      return chunks
