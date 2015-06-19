# intensity
Measure and display intensity functions for different orders of SIM calibration
data.


#Requirements

The current code requires numpy, Mrc, wx and matplotlib

#Todo

Lots of interface cleanups, maybe a bit more error checking etc...



# Instructions on how to use this code from Oxford V2 OMX system.

WARNING: The graph colours quoted here are not those from this CODE!

Focusing the grating for SI work.

Current practice is to focus the grating optimally for the SI OTF
config which is actually, rather strangely, 45deg position which is
never used for imaging. Imaging uses -20, 40 and 100 deg. The focusing
is done in the green channel (488 excitation, 510 or so
emission). Plan in March 2013 is to focus it for beads embedded 3um
into a set prolong gold substrate, using immersion oil 1.514 as a
typical centre of a real biological sample.

Convention is moving the grating away from microscope is +ve.


Example of the Intensity app output from OMX v2 software showing
alignment of the red, green and blue curves.

1. Focus the spots roughly by eye in the BFP using the viewing tool. This
can be checked more accurately by lookingnat the spot size on the
ceiling. The far field spot size should be minimised.

2. Mount objective, find a single bead and do an Intensity stack, 5um at
50nm spacing SI, SI-PSF (ie 1 angle)128x128 pixels.

3. Run Intensity from MainApp on the desktop, select the file enter
centre point (can be found by examining data in softworx DMS.(y-axis
is flipped, you must use (128-y) as the Y position).

4. The output graph needs to have the blue peaak lining up with a
single red peak and one of the peaks in the gereen line.

5. Moving the grating away from the microscope moves the blue peak to
the left. To move the blue peak much requires moving quite a long
way. March 2013 I moved the grating about 20X 400 um, or about 8 mm to
get the blue line properly peaking with the other two.

6. If your red peak is split then move a little bit, say 100 um.

7. After they all line up reasonably move to the next stage.

Now you have got the focus roughly right, now you need to get the
exact focus you require. You need to start moving the chuck back and
forward about 100 um (I use single postit notes). After each move take
a proper OTF file, 8 um, 125 nm spacing, at 256x256 pixels.

1. Upload to OMXsi and use the softworx OTF creation tool to convert it
into an OTF. Deselect LeaveKz and bead correction, we can worry about
those later.

2. Open the created OTF in Priism (called something like
19Mar_525_02.otf). Don't try and save this too deep in your directory
structure as the otf creation tool has a path limit of 80 characters,
so will fail if you do this.

3. Set the scale to -0.1 0.1 1 (ie -0.1 to 0.1 with a gamma of 1).
open the attributes dialouge and display the phase info.

4. Scroll to the second slice a examine that.

5. You want the left and right lobes to both be around zero. If you are
near they will both have gray, black and white regions. The black and
white regions should be roughly equal.

6. If they are not, move the chuck in one direction, repeat the OTF and
see if it got better, if it got better repeat until it starts to get
worse. If it got worse, go in the other direction and repeat..