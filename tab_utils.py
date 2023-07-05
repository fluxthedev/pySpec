# This dictionary maps note names to their positions on a standard-tuned guitar's fretboard.
NOTE_TO_TAB_POSITIONS = {
    'E2': [(6, 0)],
    'F2': [(6, 1)],
    'F#2': [(6, 2)],
    'G2': [(6, 3)],
    'G#2': [(6, 4)],
    'A2': [(6, 5), (5, 0)],
    'A#2': [(6, 6), (5, 1)],
    'B2': [(6, 7), (5, 2)],
    # ... continue for all notes including octaves ...
}

# Array representing the standard tuning of a guitar
# E2 (low E string) is note 40, A2 is 45, D3 is 50, G3 is 55, B3 is 59, E4 (high E string) is 64
standard_tuning = [40, 45, 50, 55, 59, 64]

# Array representing the note names
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_to_tab(note_name):
    """Convert a note name to guitar tablature positions."""
    return NOTE_TO_TAB_POSITIONS.get(note_name, [])


def chord_to_tab(chord):
    """Convert a chord (list of note names) to guitar tablature positions."""
    positions = []
    for note in chord:
        positions.extend(note_to_tab(note))
    return positions


def note_name_to_guitar_tab(note_name_with_octave):
    """
    Convert note name with octave to guitar tab positions (string, fret).

    :param note_name_with_octave: the note name with octave, e.g., 'C4'
    :return: a list of (string, fret) positions where this note can be played
    """
    return NOTE_TO_TAB_POSITIONS.get(note_name_with_octave, [])


def guitar_tab_to_note(string, fret):
    """
    Convert guitar tab (string, fret) to note name.

    :param string: the guitar string number (1-6)
    :param fret: the fret number (0-24)
    :return: the note name corresponding to the string and fret
    """
    # Convert string to integer if it is not already
    string = int(string)
    # Convert string number to MIDI note
    # Subtract 1 from the string because the array is 0-indexed
    midi_note = standard_tuning[string - 1] + fret

    # Convert MIDI note to note name
    # Subtract the MIDI number for C0 from the MIDI note to get the number of semitones
    # above C0, then take modulo 12 to get the index in the note_names array
    note_name_index = (midi_note - 12) % 12
    note_name = note_names[note_name_index]

    # Convert the MIDI note to octave by subtracting 12 from the MIDI note
    # and dividing by 12, then adding 1 (as the MIDI specification treats C0 as note 12)
    octave = (midi_note - 12) // 12 + 1

    return note_name + str(octave), string, fret
