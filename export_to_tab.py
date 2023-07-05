import logging
from music21 import note, chord, stream, instrument, tablature
from tab_utils import note_name_to_guitar_tab

# Configuration
logging.basicConfig(level=logging.INFO)


def map_to_guitar_tab(chord_sequence):
    """
    Maps a list of chords to guitar tablature and
    exports the tablature to an XML file in MusicXML format.
    """

    # Create a TabStaff and specify instrument as guitar
    guitar_staff = stream.Stream()
    guitar_staff.insert(0, instrument.AcousticGuitar())

    # Iterate through the chords
    for ch in chord_sequence:
        # Ensure that the object is a Chord
        if isinstance(ch, chord.Chord):
            for n in ch.notes:
                # Convert each note to guitar tablature
                # Convert the note name to sharp notation if it is in flat notation
                note_name = n.name
                if '-' in note_name:
                    note_name = n.pitch.getEnharmonic().name

                # Convert the note to guitar tablature
                note_name_with_octave = note_name + str(n.octave)
                # Use the new function note_name_to_guitar_tab
                tab_positions = note_name_to_guitar_tab(note_name_with_octave)

                # For each tab position, create a TablatureNote and add it to the guitar_staff
                for string, fret in tab_positions:
                    single_note = note.Note(note_name)

                    # Create a new TablatureNote and set its properties
                    tab_note = tablature.TablatureNote()
                    tab_note.fret = fret
                    tab_note.string = string
                    tab_note.linkedNote = single_note

                    # Add the TablatureNote to the guitar_staff
                    guitar_staff.append(tab_note)

    # Returning the complete staff
    return guitar_staff
