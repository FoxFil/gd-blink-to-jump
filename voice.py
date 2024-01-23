import sounddevice as sd
import keyboard
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

threshold_db = 6

key_to_hold = "w"

fs = 44100
duration = 100000

# Initialize a list to store decibel levels
decibel_levels = []

# Set up the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.axhline(y=threshold_db, color='r', linestyle='--', label='Threshold')

ax.set_ylim(0, 100)
ax.set_xlim(0, 50)  # Show only the last 50 decibel levels
ax.set_xlabel('Time')
ax.set_ylabel('Decibel Level')
ax.legend()

def callback(indata, frames, time_given, status):
    db = 20 * indata.max()
    decibel_levels.append(db)

    print('your decebeel level:', db)

    if db > threshold_db:
        keyboard.press(key_to_hold)
    else:
        keyboard.release(key_to_hold)

def update(frame):
    line.set_data(range(len(decibel_levels[-50:])), decibel_levels[-50:])
    ax.set_xlim(0, 50)  # Show only the last 50 decibel levels
    return line,

while 1:
    with sd.InputStream(callback=callback, channels=1, samplerate=fs):
        ani = FuncAnimation(fig, update, blit=True)
        plt.show()
