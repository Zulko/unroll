import numpy as np
from .KeyStrikes import KeyStrikes



def fourier_transform(signal, period, tt):
    """
    See http://en.wikipedia.org/wiki/Fourier_transform
    How come Numpy and Scipy don't implement this ???
    """
    f = lambda func : (signal*func(2*np.pi*tt/period)).sum()
    return f(np.cos)+ 1j*f(np.sin)
    


def video2rollscan(videofile, focus, start=0, end=None, savefile=None):
    """
    
    Makes a scan of the roll from the video.
    Requires the pyton module MoviePy
    
    Parameters
    -----------
    
    video
        Any videofile that MoviePy (FFMPEG) can read.
        
    focus
        A function ( f(image)->rectangular image ). For instance
        if the line of interest is defined by y=15 and x=10...230
        
        >>> focus = lambda im : im[ [15], 10:230 ]
        
    start,end
        Where to start and stop, each one either in seconds, or in
        format `(minutes, seconds)`. By default `start=0` and `end`
        is the end of the video.
        
    savefile
        If provided, the scan image will be saved under this name.
    
    Returns
    --------
    
      A W*H*3 RGB picture of the piano roll made by stacking the focus
      lines of the different frames under one another.
    """
    
    from moviepy.editor import VideoFileClip
    
    if end is None:
        end = video.duration
        
    video = VideoFileClip(videofile, audio=False).subclip(start, end)
    
    tt = np.arange(0, video.duration, 1.0/video.fps)
    result = np.vstack( [ focus(video.get_frame(t)) for t in tt] )
    
    if savefile:
        import matplotlib.pyplot as plt
        plt.imsave(savefile)
        
    return result
    

def rollscan2keystrikes(roll_image, column_widths=[1.1,50, .01],
                        threshold_keypress=.8, report = False):
    """
    
    Converts an image of a roll into a KeysStrikes object.
    
    Parameters
    ------------
    
    roll_image
        A roll image obtained for instance with video2scan
    
    column_widths
        A triplet of the form [min, max, step] with min>1
        for the search of the column width (in pixels) in the roll.
    
    threshold_keypress
        Parameter in range 0-1. A pixel is considered
        a hole if its luminosity is < threshold_keypress*max_luminosity.
        If too small, notes strikes will be missed, if too high there
        will be false note strikes.
        
    report
        If provided, the spectrum used for column-width estimation
        is stored into a file.
    
    Returns
    --------
    
    keystrikes
        A KeyStrikes object (conversion of the roll image).
    
    """
    # get the profile of  min_luminosity( column of pixels)
    roll_greyscale = roll_image.mean(axis=2) # collapse RGB to grey
    luminosity_per_column = roll_greyscale.min(axis=0)
    
    
    # compute the spectrum of this profile
    n_lines, n_columns = roll_greyscale.shape
    tt = np.arange(n_columns) # 0,1,2,3,4... n_columns
    lum0 = luminosity_per_column - luminosity_per_column.mean()
    widths = np.arange(*column_widths)
    transform = [fourier_transform(lum0,w,tt) for w in widths]
    transform = np.array( transform )
    
    # the max of the spectrum indicates the width of a hole-column
    optimal_i = np.argmax(abs(transform))
    hole_width = widths[optimal_i]
    
    # the width + the offset enable to determine which columns of
    # pixels are in hole-columns
    offset = np.angle( transform[optimal_i] ) +hole_width/2
    keys_positions = np.arange(offset,n_columns,hole_width)
    keys_positions = np.round(keys_positions).astype(int)
    
    # only keep one column of pixel per hole-column in the image
    keys_greyscale = roll_greyscale[:, keys_positions]
    
    
    # threshold this reduced image into key-pressed/ key-released
    maxi = keys_greyscale.max()
    key_pressed = keys_greyscale < threshold_keypress*maxi
    
    # find the moments of the strikes
    key_changes =  np.diff(key_pressed.astype(int), axis=0)
    
    y, x = key_changes.shape
    keys_strikes = [{'time':i,'note':j} for i in range(y)
                                       for j in range(x)
                                       if key_changes[i,j]==1 ]
                
    if report:
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(1,2, figsize=(12,3.5))
        
        ax[0].plot(luminosity_per_column, c='k')
        ax[0].set_xlabel('column of pixels (x-index)')
        ax[0].set_ylabel('minimal luminosity')
        for p in keys_positions:
            ax[0].axvline(p,c='r')
        
        ax[1].plot(widths, abs(transform), c='k')
        ax[1].set_xlabel("Period (in number of pixels)");
        ax[1].set_ylabel("Spectrum value")
        ax[1].axvline(hole_width, lw=3, c='r')
        
        fig.tight_layout()
        fig.savefig('roll_luminosity_spectrum.jpeg')
    
    return KeyStrikes(keys_strikes)
    
    
    
    

