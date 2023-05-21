# from esp32.udp_audio import Esp32AudioUDP
# from audio import AudioProcessing

# # esp32_audio = Esp32AudioUDP()
# # esp32_audio.begin()
# # data = esp32_audio.start_recording(5)
# # AudioProcessing.write_wav(data, 'raw.temp.mp3')
# # reduce_noise_data = AudioProcessing.reduce_noise(data)
# # AudioProcessing.write_wav(reduce_noise_data, 'raw.reduce-noise.temp.mp3')
# # chunks = AudioProcessing.split_audio(reduce_noise_data)
# # for i, chunk in enumerate(chunks):

# #   answer = input('Is correct?')

from audio.AudioLabeling import AudioLabeling

labeling = AudioLabeling(5)
labeling.begin('output_data')
