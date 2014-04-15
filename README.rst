Unroll
=======

Unroll is a Python module to ease transcription of piano rolls to sheet music.
It transcribes either a MIDI file or a video of a piano roll. It finds
the notes, the tempo, roughly separates the hands, and writes the result
in a Lilypond file. In particular

You can use it like this: ::
    
    # TO TRANSCRIBE FROM A VIDEO
    
    from unroll import video2scan, rollscan2keystrikes
    focus = lambda im : im[[156],58:478]
    scan = video2scan(videofile = "limehouse_nights.mp4", focus = focus)
    keystrikes = rollscan2keystrikes(scan)
    keystrikes = ks.transposed(26)
    keystrikes.transcribe('score.ly', quarter_durations = [2,10,0.02])
    
    # TO TRANSCRIBE FROM A MIDI FILE
    
    from unroll import midi2keystrikes
    keystrikes = midi2keystrikes('tiger_rag.mid')
    ks.transcribe('score.ly', quarter_durations = [50,100,0.02])


Then you must edit ``score.ly`` to correct the mistakes and when you are done you compile it with
::
    
    lilypond score.ly
    
    
Installation
--------------

Unroll can be installed by unzipping the source code in one directory and using this command:
::
    
    (sudo) python setup.py install

You can also install it directly from the Python Package Index (PYPI_) with this command:
::
        
    (sudo) pip install unroll


Contribute
-----------
Unroll is an open-source software originally written by Zulko_ and released under the MIT licence.
The project is hosted on Github_ and everyone is welcome to contribute ! Please give feedback if you are using it and encounter difficulties.


.. _PYPI: https://pypi.python.org/pypi/unroll
.. _Github: https://github.com/Zulko/Unroll
.. _Zulko : https://github.com/Zulko
