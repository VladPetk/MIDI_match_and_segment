import pickle
from fastdtw import fastdtw
from parallelbar import progress_map

import argparse
import os

def find_segment_dtw(query, reference, step=250):
    query_segment = np.array(query)
    long_time_series = np.array(reference)

    # Initialize variables to store the best match
    best_distance = float('inf')
    best_start_index = None

    # Iterate through all possible subsegments of the longer time series
    for i in range(0, len(long_time_series) - len(query_segment) + 1, step):
        subsegment = long_time_series[i:i+len(query_segment)]
        distance, _ = fastdtw(query_segment, subsegment)

        # Check if this subsegment is the best match so far
        if distance < best_distance:
            best_distance = distance
            best_start_index = i

    # Extract the most similar segment
    most_similar_segment = long_time_series[best_start_index:best_start_index+len(query_segment)]
    similarity_score = 1 / (1 + best_distance)

    return most_similar_segment, best_start_index, similarity_score

def dtw_over_list(midi_in, midi_list, reduction=10, chunk_len=500):
    
    all_res = []

    min_len = int((chunk_len/reduction)*0.9)
    stepper = int(chunk_len/reduction)
    
    query = reduce_list_mode(midi_in[:chunk_len], reduction)
    results = []

    for j, midi in enumerate(midi_list):
        if len(midi) < 1000:
            continue
        reference = reduce_list_mode(midi, reduction)
        seg, idx, score = find_segment_dtw(query, reference, step=stepper)
        if len(seg) < min_len:
            continue
        r_idx = idx*reduction
        results.append([midi[r_idx:r_idx+(len(seg)*reduction)], score])
        print(f"Processing: {round((j/len(midis_in))*100, 2)} ----------------", end="\r", flush=True)
            
    return [midi_in[:chunk_len], max(results, key = lambda x: x[1])]

if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--name_in", type=str, help="Specify the name in variable")
    parser.add_argument("--name_out", type=str, help="Specify the name out variable")
    args = parser.parse_args()

    bad_paths = []
    for path, subdirs, files in os.walk("D:/musicai_old/classical_midis/"):
        for name in files:
            bad_paths.append(os.path.join(path, name))

    good_paths = []
    for path, subdirs, files in os.walk("D:/musicai_old/maestro/"):
        for name in files:
            good_paths.append(os.path.join(path, name))

    res = progress_map(chordify_midi, good_paths, process_timeout=50, n_cpu=6)
    pickle.dump(res, open(f"{args.name_out}.p", "wb"))
    
    