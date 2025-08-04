import sounddevice as sd

print("Available Input Devices:")
for i, dev in enumerate(sd.query_devices()):
    if dev['max_input_channels'] > 0:
        print(f"[{i}] {dev['name']} — max channels: {dev['max_input_channels']} — default samplerate: {dev['default_samplerate']}")