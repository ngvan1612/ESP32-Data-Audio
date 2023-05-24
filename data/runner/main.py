import tensorflow as tf
from tensorflow.keras.saving import load_model
import tensorflow_io as tfio
import socket
import io
from pydub import AudioSegment
import numpy as np
from pydub.silence import split_on_silence
import noisereduce as nr

labels = {
    'silent': 0,
    'tien': 1,
    'lui': 2,
    'trai': 3,
    'phai': 4
}

reverse_labels = {
    labels[x]: x for x in labels
}

model = load_model('audio-model.h5')
model.summary()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 1234))

seconds = 100

wav_test = []
while len(wav_test) < seconds * 16000 * 2:
  message, _ = server_socket.recvfrom(1000)
  data = list(message)
  assert len(data) == 1000
  wav_test.extend(data)

  if len(wav_test) == 16000 * 2 * 5:
    s = io.BytesIO(bytes(wav_test))
    buffer = AudioSegment.from_raw(s, sample_width=2, frame_rate=16000, channels=1)
    buffer = np.array(buffer.get_array_of_samples())
    buffer = nr.reduce_noise(y=buffer, sr=16000)
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

    print(len(chunks))
    if len(chunks) == 1 and np.array(chunks[0].get_array_of_samples()).shape[0] == 16000:
      # nothing
      print('not found')
      pass
    else:
      for i, chunk in enumerate(chunks):
        df = np.array(chunk.get_array_of_samples())
        tensor = tf.cast(df, tf.float32) / 32768.0
        spectrogram = tfio.audio.spectrogram(tensor, nfft=512, window=512, stride=256)
        mel_spectrogram = tfio.audio.melscale(spectrogram, rate=16000, mels=128, fmin=32, fmax=8000)
        arr_df = np.array([mel_spectrogram.numpy()])
        pred = model.predict(arr_df, verbose=None)[0]
        pos = np.argmax(pred)
        print(i, 'predict', reverse_labels[pos], 'with acc=', int(pred[pos] * 100 * 100) / 100, '%')
    wav_test = []
