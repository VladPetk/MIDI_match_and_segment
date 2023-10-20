# MIDI_match_and_segment
 Python code for finding matches between time_series (music symbolically represented, specifically), segmenting time series, and matching segments

## segmenter.py

The script segments time series data using dynamic time warping (DTW). It takes a list of matches as input, where each match is a tuple of two time series sequences. The output is a list of segmented matches, where each segmented match is a tuple of three elements: the segmented input sequence, the segmented output sequence, and the DTW distance between the two segmented sequences.

### The following is a step-by-step overview of what happens in the code:

The `find_dtw_greedy()` function finds the most similar subsegment of the reference sequence to the query sequence. It does this by iteratively extending the subsegment length and calculating the DTW distance between the subsegment and the query sequence. The function returns the most similar subsegment, the start and end indices of the subsegment, and the DTW distance.

The `split_random()` function randomly splits a list into chunks of a specified minimum and maximum size. It returns a list of chunks and a list of indices corresponding to the start of each chunk in the original list.

The `segment_dtw()` function segments the input and output time series sequences based on the DTW distance between the two sequences. It does this by:

* Randomly splitting the input sequence into chunks.
* Finding the most similar subsegment of the reference sequence to each chunk of the input sequence.
* Segmenting the input and output sequences based on the start and end indices of the most similar subsegments.

The main function loads the list of matches from a file, segments the matches using the segment_dtw() function, and pickles the segmented matches to a file.

This code can be used to segment time series data for a variety of tasks, such as anomaly detection, pattern recognition, and data classification.

## harmonize.py


The code chordifies MIDI files using the Dechorder library. It takes two lists of MIDI file paths as input, one for the "good" MIDI files and one for the "bad" MIDI files. The output is two pickle files, one containing the chordified good MIDI files and the other containing the chordified bad MIDI files.

The code works by first loading the list of good and bad MIDI file paths. Then, it uses the `chordify_midi()` function to chordify each MIDI file. The `chordify_midi()` function works by first loading the MIDI file and then using the Dechorder library to extract the chords from the MIDI file. Once the chords have been extracted, the function converts the chords to a list of chord names.

Once all of the MIDI files have been chordified, the code pickles the chordified MIDI files to two separate pickle files. This allows the chordified MIDI files to be loaded and used later.

Here is a step-by-step overview of what happens in the code:

* The main function loads the lists of good and bad MIDI file paths.
* For each good MIDI file, the main function calls the `chordify_midi()` function to chordify the MIDI file.
* The main function pickles the chordified good MIDI files to a pickle file.
* The main function repeats steps 2 and 3 for the bad MIDI files.

## score_sim_harm.ipynb

The notebook matches MIDI files based on the modified (weighted) Jaccard similarity of their chord progressions. It takes two lists of MIDI file paths as input, one for the "good" MIDI files and one for the "bad" MIDI files. The output is a list of matches, where each match is a tuple of five elements:

* The path to the good MIDI file
* The path to the bad MIDI file
* The modified Jaccard similarity of the two chord progressions
* The index of the good MIDI file in the input list
* The index of the bad MIDI file in the input list
* 
The code works by first calculating the modified Jaccard similarity of the chord progressions of each pair of good and bad MIDI files. The modified Jaccard similarity is a measure of similarity between two sets that takes into account the size of the sets. It is calculated by dividing the number of elements that are common to both sets by the total number of elements in both sets.

Once the modified Jaccard similarity has been calculated for each pair of good and bad MIDI files, the code selects the pair with the highest modified Jaccard similarity as the best match. The code then outputs a list of all the best matches.

The code also includes a function to calculate the cosine similarity between two lists of pitches. This function can be used to filter out matches where the melodies of the two MIDI files are very different.
