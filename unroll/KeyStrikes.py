import numpy as np
import music21
from .lilypond import LILY_TEMPLATE


class KeyStrikes:

    def __init__(self, keystrikes):
        """
        KeyStrikes are objects containing a series of note (or keys)
        and the time at which they are striken.
        These objects can be analyzed to find the duration of the
        quarter, split into two KeyStrikes objects (to separate the
        hands), quantized, and converted into a Lilypond score.
        
        Methods midi2keystrikes and rollscan2keystrikes return such
        objects, from roll images and midi files respectively.
        """

        keystrikes = sorted(keystrikes, key=lambda e: e['time'])
        self.keystrikes = keystrikes
        self.times = np.array([e['time'] for e in keystrikes])

    def transposed(self, tones):
        """
        Returns a new Keystrike object in which the notes n have
        been replaced by n+tone
        """
        new_notes = [{'time': e['time'], 'note':e['note'] + tones}
                     for e in self.keystrikes]
        return KeyStrikes(new_notes)

    def _filter(self, fl):
        """
        Returns a Keystrike object with only the notes such
        that ``fl(note)==True``, where ``note = {'note: x, 'time': y'}``
        """
        return KeyStrikes(filter(fl,  self.keystrikes))

    def separate_hands(self, note=60):
        """
        Separates the hands by giving all the notes under `note` to
        the left hand. Returns 2 Keystrikes objects (left, right).
        """
        left = self._filter(lambda e: e['note'] < note)
        right = self._filter(lambda e: e['note'] >= note)
        return left, right

    def _spectrum(self, T):
        """
        Return the "Fourier Transform" evaluated in T of the hit-time
        of the notes. If it is high, T is a period of the hits.
        """
        a = np.sin(2 * np.pi * self.times / T).sum()
        b = np.cos(2 * np.pi * self.times / T).sum()
        return a ** 2 + b ** 2

    def find_quarter_duration(self, durations, report=False):
        """
        Finds the quarter duration by computing the spectrum with
        different period durations and keeping the optimal duration.
        If report is True, a image of the specturm is saved.
        """

        spectrum = map(self._spectrum, durations)
        optimal_i = np.argmax(spectrum)
        optimal_duration = durations[optimal_i]

        if report:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1)
            ax.plot(durations, spectrum)
            ax.axvline(optimal_duration, ls=':', color='r')
            ax.set_xlabel('Quarter duration')
            ax.set_ylabel('Spectrum Value')
            fig.tight_layout()
            fig.savefig("keystrikes_spectrum.jpeg")

        return optimal_duration

    def _to_music21stream(self):
        """
        Transforms the KeyStrikes object into a ``music21`` stream
        object (first step towards its conversion to Lilypond format)
        """

        stream = music21.stream.Stream()
        for strike in self.keystrikes:
            if (len(strike['note'])) == 1:
                to_append = music21.note.Note(strike['note'][0])
            else:
                to_append = music21.chord.Chord(strike['note'])
            to_append.duration.quarterLength = strike['duration']
            stream.append(to_append)

        return stream

    def to_lilystring(self):
        """
        Converts the Keystrikes object to lilypond format using music21
        """
        stream = self._to_music21stream()
        converter = music21.lily.translate.LilypondConverter()
        converter = converter.lyPrefixCompositeMusicFromStream(stream)

        return converter.stringOutput()

    def quantized(self, quarter_duration):
        """
        Returns a new KeyStrikes object obtained by quantizing the
        notes (regroups chords and corrects durations to the nearest
        eighth).
        """

        # the result is initialized with one 'empty' note.
        result = [{'note': [], 'time':0, 'duration':None}]

        for strike in self.keystrikes:

            # time elapsed since last strike
            delay = strike['time'] - result[-1]['time']
            # the next line quantizes that time in eights.
            delay_q = 0.5 * int((4.0 * delay / quarter_duration + 1) / 2)
            delay_q = min(delay_q, 12)

            if (delay_q == 0):  # put note in previous chord
                if strike['note'] not in result[-1]['note']:
                    result[-1]['note'].append(strike['note'])

            else:  # this is a 'new' note/chord
                result[-1]['duration'] = delay_q
                result.append({'note': [strike['note']],
                               'duration': None,
                               'time': strike['time']})

        result[-1]['duration'] = 4  # give a duration to the last note

        if result[0]['note'] == []:
            result.pop(0)  # first note will surely be empty

        return KeyStrikes(result)
        
        
    def transcribe(self, filename, quarter_durations,
                   hands_separation=60, report=False):
        """
        Transcribes the KeyStrike Object into piano sheet music.
        First it finds the tempo, then separates the hands, quantizes
        each hand and converts each to lilypond format.
        Finally it writes everything into a nive lilypond template,
        which can then be compiled with ``lilypond myfile.ly``
        
        quarter_durations must be of the form [min, max, step],
        with min>1. For instance [2, 40, .1]. Then the duration will be
        chosen among 2, 2.1, 2.2 ... 40
        """

        if hasattr(quarter_duration, '__iter__'):
            durations = np.arange(*quarter_duration)
            quarter_duration = self.find_quarter_duration(durations)

        left_hand, right_hand = self.separate_hands()

        left_hand_quantized = left_hand.quantized(quarter_duration)
        right_hand_quantized = right_hand.quantized(quarter_duration)

        left_hand_lily = left_hand_quantized.to_lilystring()
        right_hand_lily = right_hand_quantized.to_lilystring()

        score = LILY_TEMPLATE
        score = score.replace('$CONTENT_RIGHT_HAND', right_hand_lily)
        score = score.replace('$CONTENT_LEFT_HAND', left_hand_lily)

        with open(filename, "w+") as f:
            f.write(score)
