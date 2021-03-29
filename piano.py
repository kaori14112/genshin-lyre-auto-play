import time
import win32api
import win32con

from midi.midifiles.midifiles import MidiFile

letter = {'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90}
mapping = {'48': 'z', '50': 'x', '52': 'c', '53': 'v', '55': 'b', '57': 'n', '59': 'm', '60': 'a', '62': 's', '64': 'd', '65': 'f', '67': 'g', '69': 'h', '71': 'j', '72': 'q', '74': 'w', '76': 'e', '77': 'r', '79': 't', '81': 'y', '83': 'u'}

def dinput():
	a = {}
	count = 36
	while count <= 84:
		a[str(count)] = int(input())
		count += 1
	return a

def find(arr, time):
	result = []
	for i in arr:
		if i["time"] == time:
			result.append(i["note"])
	return result

def press(note):#48 83
	if note in mapping.keys():
		win32api.keybd_event(letter[mapping[note]], 0, 0, 0)
		#print("Press: ", letter[mapping[note]])
	return

def unpress(note):#48 83
	if note in mapping.keys():
		win32api.keybd_event(letter[mapping[note]], 0, win32con.KEYEVENTF_KEYUP, 0)
	return

def make_map():
	s = "zxcvbnmasdfghjqwertyu"
	for i, k in enumerate(mapping.keys()):
		mapping[k] = s[i]
	print(mapping)

midi_file = input("Midi file name (without suffix): ")
midi_object = MidiFile("./songs/" + midi_file + ".mid")
try:
	midi_object = MidiFile("./songs/" + midi_file + ".mid")
except:
	print("The file is damaged or does not exist. ")
	quit()
tick_accuracy = 0
print("Try to calculate the playback speed... ")
try:
	bpm = 60000000 / midi_object.tracks[1][0].tempo
	tick_accuracy = bpm / 20
	print("The calculation is successful. ")
except:
	tick_accuracy = int(input("The calculation failed, please check whether the file is complete, or manually enter the playback speed: (7)"))
type = ['note_on','note_off']
tracks = []
end_track = []
print("Start reading the audio track. ")
for i,track in enumerate(midi_object.tracks):
	print(f'track{i}')
	last_time = 0
	last_on = 0
	for msg in track:
		info = msg.dict()
		info['pertime'] = info['time']
		info['time'] += last_time
		last_time = info['time']
		if (info['type'] in type):
			del info['channel']
			del info['velocity']
			info['time'] = round(info['time'] / tick_accuracy)
			if info['type'] == 'note_on':
				del info['type']
				del info['pertime']
				last_on = info['time']
				tracks.append(info)
			else:
				del info['type']
				del info['pertime']
				last_on = info['time']
				end_track.append(info)
mmax = 0
for i in end_track:
	mmax = max(mmax, i['time'] + 1)
start = {}
print("Start converting the score... ")
for i in range(mmax):
	start[str(i)] = find(tracks, i)
stime = int(input("Wait time (seconds): "))
print("Play will be start in " + str(stime) + " seconds, please be prepared. ")
time.sleep(stime)
for i in range(mmax):
	if i != 0:
		for note in start[str(i - 1)]:
			unpress(str(note))
	for note in start[str(i)]:
		press(str(note))
	time.sleep(0.025)
print("The playback ends. ")