
LILY_TEMPLATE = r"""
\version "2.12.0"

\header {
 title = "" 
 subtitle = "" 
 composer = "" 
 arranger = ""
 source = ""
 style = ""
 copyright = "Creative commons"
}


upper = \new Voice \with {
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver" } {
    
  \time 4/4
  
  $CONTENT_RIGHT_HAND
}


lower =  \new Voice \with {
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver" } {
    
  \clef bass
  \time 4/4
  
  $CONTENT_LEFT_HAND
}

\score {
  \new PianoStaff <<
    \set PianoStaff.instrumentName = #"Piano  "
    
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout{}
  \midi{}
}
"""

