import socket
from pydub import AudioSegment
import io
import numpy as np

class Esp32AudioUDP:
    
    def __init__(self) -> None:
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def begin(self):
      self.server_socket.bind(('', 1234))

    def start_recording(self, seconds: int):
      wav_test = []
      while len(wav_test) < seconds * 16000 * 2:
        if len(wav_test) % 16000 == 0:
          print('Reading... ', len(wav_test))
        message, _ = self.server_socket.recvfrom(1000)
        data = list(message)
        assert len(data) == 1000
        wav_test.extend(data)
      
      s = io.BytesIO(bytes(wav_test))
      buffer = AudioSegment.from_raw(s, sample_width=2, frame_rate=16000, channels=1)
      return np.array(buffer.get_array_of_samples())
