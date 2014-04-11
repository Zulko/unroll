Unroll
=======

Unroll is a Python module for the transcription of piano rolls to sheet music. It will very soon also be a command line tool.
It can transcribe from a MIDI file or from a video of a piano roll. It finds
the notes, the tempo, roughly separates the hands, and writes the result
in a Lilypond_ file.

See this blog post for a more thorough presentation of the objectives and the method.

Use
-----

Unroll can be called from Python or from a terminal.

To transcribe a MIDI file (terminal, coming soon) ::

    >>> unroll tiger_rag.mid quarter=1.1,10,0.02 score.ly

To transcribe a MIDI file (Python) ::
    
    from unroll import midi2keystrikes
    
    keystrikes = midi2keystrikes('tiger_rag.mid')
    
    keystrikes.transcribe('score.ly',
                          quarter_duration = [1.1,10,0.02])

To transcribe a video (terminal, coming soon) ::

    >>> unroll limehouse_nights.mp4 focus=156,58,156,478
               transpose=26 quarter=1.1,10,0.02 score.ly

To transcribe a video (Python) ::
    
    from unroll import video2scan, rollscan2keystrikes
    
    scan = video2rollscan(videofile = "limehouse_nights.mp4",
                          focus = lambda im : im[[156],58:478])
                      
    keystrikes = rollscan2keystrikes(scan)
    keystrikes = ks.transposed(26) # transpose notes +26 tones
    keystrikes.transcribe('score.ly',
                          quarter_duration = [1.1,10,0.02])
    

The output is a Lylipond file (``score.ly``) that you will need to edit to correct the mistakes (it can take a few hours with a good editor like Frescobaldi_), 
and then compile to beautiful sheet music  like this one.
    

Installation
--------------

First method: get the source (on Github_ or PyPI_), unzip it into a directory, and in a terminal type: ::
    
    (sudo) python setup.py install
    


Second method: with a pip command. ::
    
    (sudo) pip install unroll
    


Contribute
-----------

Unroll is a free open-source software originally written by Zulko_ and released under the MIT licence.
Everyone is welcome to contribute and give feedback on Github_.

Reference Manual
------------------

.. autoclass:: unroll.KeyStrikes
   :members:

Video
''''''


.. autofunction:: unroll.video2rollscan

.. autofunction:: unroll.rollscan2keystrikes


MIDI
'''''

.. autofunction:: unroll.midi2keystrikes

.. raw:: html

        <a href="https://github.com/Zulko/unroll">
        <img style="position: absolute; top: 0; right: 0; border: 0;"
        src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"
        alt="Fork me on GitHub"></a>


.. _Lilypond: http://www.lilypond.org
.. _Frescobaldi: http://frescobaldi.org/
.. _Zulko: https://github.com/Zulko/
.. _Github: https://github.com/Zulko/unroll
.. _PYPI: https://pypi.python.org/pypi/unroll
