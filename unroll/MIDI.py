import music21
from .KeyStrikes import KeyStrikes

def midi2keystrikes(filename,tracknum=0):
    """
    Reads a midifile (thanks to the package music21), returns a list
    of the keys hits:  [{'time':15, 'note':50} ,{... ]
    """
    
    mf = music21.midi.MidiFile()
    mf.open(filename)
    mf.read() 
    mf.close()
    events = mf.tracks[tracknum].events
    result = []
    t=0
    
    for e in events:
        
        if e.isDeltaTime and (e.time is not None):
            
            t += e.time
            
        elif ( e.isNoteOn and ( e.pitch is not None) and
              (e.velocity != 0) and (e.pitch > 11)):
                   
            result.append( {'time':t, 'note':e.pitch} )
            
    if (len(result) == 0) and (tracknum <5):
        # if it didn't work, scan another track.
        return midi2keystrikes(filename,tracknum+1)
        
    return KeyStrikes(result)
