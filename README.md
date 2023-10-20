# MIDI_match_and_segment
 Python code for finding matches between time_series (music symbolically represented, specifically), segmenting time series, and matching segments

## segmenter.py

The script segments time series data using dynamic time warping (DTW). It takes a list of matches as input, where each match is a tuple of two time series sequences. The output is a list of segmented matches, where each segmented match is a tuple of three elements: the segmented input sequence, the segmented output sequence, and the DTW distance between the two segmented sequences.

### The following is a step-by-step overview of what happens in the code:

The find_dtw_greedy() function finds the most similar subsegment of the reference sequence to the query sequence. It does this by iteratively extending the subsegment length and calculating the DTW distance between the subsegment and the query sequence. The function returns the most similar subsegment, the start and end indices of the subsegment, and the DTW distance.
The split_random() function randomly splits a list into chunks of a specified minimum and maximum size. It returns a list of chunks and a list of indices corresponding to the start of each chunk in the original list.
The segment_dtw() function segments the input and output time series sequences based on the DTW distance between the two sequences. It does this by:
Randomly splitting the input sequence into chunks.
Finding the most similar subsegment of the reference sequence to each chunk of the input sequence.
Segmenting the input and output sequences based on the start and end indices of the most similar subsegments.
The main function loads the list of matches from a file, segments the matches using the segment_dtw() function, and pickles the segmented matches to a file.
This code can be used to segment time series data for a variety of tasks, such as anomaly detection, pattern recognition, and data classification.
