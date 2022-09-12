from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import get_array_type
import matplotlib.pyplot as plt
import numpy as np
import scipy
import array
from collections import Counter
from pydub.utils import get_array_type
from Levenshtein import distance
import constants

def getSong():
    AudioSegment.converter = '/opt/homebrew/Cellar/ffmpeg/5.1/bin/ffmpeg'
    song = AudioSegment.from_wav("redemption_song.wav")
    return song    
    
# array of times in song when note starts
def findNoteStartTimes(volume, segment_ms):
    MIN_VOLUME = -33
    MIN_EDGE_HEIGHT = 5 # this is 5 hz increase from one sample to next
    MIN_MS_BETWEEN = 100 # 100 milliseconds
    start_times = []
    for i in range(1, len(volume)):
        if ((volume[i] > MIN_VOLUME) and (volume[i] - volume[i-1] > MIN_EDGE_HEIGHT)):
            time = i * segment_ms
            if (len(start_times) == 0 or (time - start_times[-1] >= MIN_MS_BETWEEN)):
                time = round(time/1000, 2) # convert to milliseconds
                start_times.append(time)
    return start_times

def get_frequencySpectrum(sample, max_frequency=800):
    """
    Derive frequency spectrum of a pydub.AudioSample
    Returns an array of frequencies and an array of how prevalent that frequency is in the sample
    """
    # convert pydub.AudioSample to raw audio data
    bit_depth = sample.sample_width * 8
    array_type = get_array_type(bit_depth)
    raw_audio_data = array.array(array_type, sample._data)
    n = len(raw_audio_data)
    print(n)



def main():
    song = getSong()
    twenty_seconds = 20 * 1000
    song = song[:twenty_seconds]
    # Filter out low frequencies to reduce noise
    updated_song = song.high_pass_filter(80)

    # Size of segments to break song into for volume calculations
    SEGMENT_MS = 50

    #dBFS is decibels relative to maximum possible loudness
    volume = [segment.dBFS for segment in song[::SEGMENT_MS]]
    volume_new = [segment.dBFS for segment in updated_song[::SEGMENT_MS]]

    # loading song as AudioSegment. Then broke into segments using slicing and called dBFS function on each segment to 
    # get its volume over time. Create Plot with Matplotlib
    x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
    
    # plt.plot(x_axis, volume)
    plt.plot(x_axis, volume_new)
    plt.xticks(np.arange(0, 10, 2.0))

    print(f"Predicted: {constants.predictedStartTimes}")
    actualStartTimes = findNoteStartTimes(volume_new, SEGMENT_MS)
    print(f"Actual: {actualStartTimes}")
    for s in constants.predictedStartTimes:
        plt.axvline(x=s, color='r', linewidth=1.0, linestyle="-")
    plt.show()

    get_frequencySpectrum()


if __name__ == "__main__":
    main()