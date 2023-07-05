import logging
import pandas as pd
import librosa
import numpy as np
from music21 import *
from export_to_tab import map_to_guitar_tab
import logging


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

y, sr = librosa.load('audiofile.mp3')

# Step 1: Read Spectrogram Data from CSV
logging.info("Reading spectrogram data from CSV")
try:
    data = pd.read_csv('spectrogram.csv')
    logging.info("Spectrogram data successfully read from CSV")
except Exception as e:
    logging.error("Error reading spectrogram data from CSV: %s", str(e))

# Assuming data is an array representing the spectrogram
# Convert pandas DataFrame to numpy array for librosa processing
spectrogram_data = data.to_numpy()

# Inspect the data (it should be 2D array)
if len(spectrogram_data.shape) != 2:
    logging.error("Data loaded does not have the shape of a spectrogram")
    exit()

# Check for NaN or infinite values and replace them with zeros
if not np.all(np.isfinite(spectrogram_data)):
    logging.warning(
        "Spectrogram data contains NaN or infinite values. Replacing with zeros.")
    spectrogram_data = np.nan_to_num(spectrogram_data)

# Convert to magnitude spectrogram if data is complex
if np.iscomplexobj(spectrogram_data):
    logging.info("Converting complex spectrogram to magnitude spectrogram")
    spectrogram_data = np.abs(spectrogram_data)


# Step 2: Preprocessing Spectrogram Data

# Harmonic-Percussive Source Separation
try:
    logging.info("Applying Harmonic-Percussive Source Separation...")
    harmonic, percussive = librosa.effects.hpss(spectrogram_data)
    logging.info("Harmonic-Percussive Source Separation applied successfully")
except Exception as e:
    logging.error(f"Error applying Harmonic-Percussive Source Separation: {e}")

# Noise Reduction using Median Filtering
try:
    logging.info("Applying Noise Reduction...")
    noise_reduced_spectrogram = librosa.decompose.nn_filter(
        harmonic, aggregate=np.median, metric='cosine')
    logging.info("Noise Reduction applied successfully")
except Exception as e:
    logging.error(f"Error applying Noise Reduction: {e}")

# Step 4: Extract Chords
logging.info("Extracting chords from audio file")
try:
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

    # Define pitch class names
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E',
                     'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Detect chords from chromagram
    chord_sequence = []
    for time_slice in chromagram.T:
        # Convert chroma vector to music21 chord object
        chroma_vector = [int(round(x * 100)) for x in time_slice]
        pitches = []
        for pitch_class, intensity in enumerate(chroma_vector):
            # Assuming that if intensity is above a threshold, the pitch is present in the chord
            if intensity > 30:
                pitches.append(pitch_class)
        # Create a Chord object and append it to the sequence
        ch = chord.Chord(pitches)
        chord_sequence.append(ch)

    logging.info("Chords extracted successfully")
except Exception as e:
    logging.error("Error extracting chords: %s", str(e))
    logging.error("Skipping remaining steps due to error")
    exit()

# Step 5: Mapping Chords to Guitar Tablature
guitar_staff = map_to_guitar_tab(chord_sequence)

logging.info("Mapping chords to guitar tablature")

# Step 6: Create MusicXML file
logging.info("Creating MusicXML file")
try:
    # Creating a complete music score with the guitar_staff
    music_score = stream.Score()
    music_score.insert(0, guitar_staff)

    # Exporting the score to MusicXML format
    music_score.write('musicxml', fp='output.xml')
    logging.info("MusicXML file created successfully")
except Exception as e:
    logging.error("Error creating MusicXML file: %s", str(e))

logging.info("Script completed")
