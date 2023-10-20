from parallelbar import progress_map
import pickle

import argparse
import os
from fastdtw import fastdtw
import random
import numpy as np


def find_dtw_greedy(query, reference):

  # Define your time series data
  x = np.array(query, dtype=float)
  y = np.array(reference, dtype=float)

  # Set initial best match and distance
  best_match = None
  best_distance = float('inf')
  start_id = int()
  end_id = int()

  # Define the initial subsegment length
  subsegment_length = len(x)

  for i in range(len(y) - subsegment_length + 1):
      subsegment = y[i:i+subsegment_length]
      distance, _ = fastdtw(x, subsegment)

      if distance < best_distance:
          best_distance = distance
          best_match = subsegment
          start_id = i
          end_id = i+subsegment_length

  # Calculate DTW distance for the initial subsegment length
  distance, _ = fastdtw(x, y[start_id:end_id])

  while True:
      # Check the next longer subsegment to the right one by one
      if subsegment_length < len(y):
          end_id += 1
          extended_subsegment = y[start_id:end_id]
          extended_distance, _ = fastdtw(x, extended_subsegment)

          if extended_distance < distance:
              distance = extended_distance
          else:
              # If increasing the length doesn't improve the distance, break the loop
              end_id -= 1
              break

  while start_id > 0:
      # Check the next longer subsegment to the left one by one
      if start_id > 0:
          start_id -= 1
          extended_subsegment = y[start_id:end_id]
          extended_distance, _ = fastdtw(x, extended_subsegment)

          if extended_distance < distance:
              distance = extended_distance
          else:
              # If increasing the length doesn't improve the distance, break the loop
              start_id += 1
              break

  # Update the best match if a better subsegment is found
  if distance < best_distance:
      best_distance = distance
      best_match = y[start_id:end_id]

  # Return the most similar subsegment
  return best_match, start_id, end_id, best_distance

def split_random(input_list, min_size=20, max_size=100):
    result = []
    remaining_list = input_list[:]
    res_idx = [0]
    last_index = 0
    
    while remaining_list:
        # Randomly select a chunk size between min_size and max_size
        chunk_size = random.randint(min_size, max_size)
        
        # Ensure that the chunk size doesn't exceed the remaining list length
        chunk_size = min(chunk_size, len(remaining_list))
        
        # Take the chunk from the beginning of the remaining list
        chunk = remaining_list[:chunk_size]
        
        # Remove the chunk from the remaining list
        remaining_list = remaining_list[chunk_size:]

        # Calculate index
        index = last_index + chunk_size
        last_index = index
        
        # Append the chunk and the index to the result list
        result.append(chunk)
        res_idx.append(index)
    
    return result, res_idx

min_l = 40
max_l = 100
window = max_l*2

def segment_dtw(match):

    try:

        # sequences in and out
        bad = match[0]
        good = match[1]
    
        # Work only with pitches for matching
        y = [i.pitch for i in bad]
        y1 = [i.pitch for i in good]
        
        # Random split into chunks
        in_chunks, in_idx = split_random(y, min_l, max_l)
        
        idx_chunks = []
        distances = []
        
        # Keep track of where we are to ID the matches in the pre-chunked sequence
        start_id = 0
        
        # Go over each chunk and find its match in the 'good' out sequence
        for i, query in enumerate(in_chunks):
            # Keep track of where we are to ID the matches in the pre-chunked sequence
            current_pos = len([item for chunk in in_chunks[:i+1] for item in chunk])
            # Only consider the approximate area around the current chunk
            window_start = (current_pos - window) if current_pos>=window else 0
            window_end = (current_pos + window) if current_pos<=(len(y1)-window) else len(y1)
            
            result, start, end, distance = find_dtw_greedy(query, y1[window_start:window_end])
    
            # Update start and end in relation to the whole 'good' sequence
            start = window_start + start
            end = window_start + end
            
            # Save the absolute indexes + distance
            idx_chunks.append([[start_id, current_pos], [start, end], distance])
    
            # Update start id
            start_id = current_pos
    
        segmented_matches = []
        
        # Use the saved indexes to segment the original data
        # Output is [match_in, match_out, distance]
        for chunk in idx_chunks:
            seg_in = good[chunk[0][0]:chunk[0][1]]
            seg_out = bad[chunk[1][0]:chunk[1][1]]
            dist = chunk[2]
            segmented_matches.append([seg_in, seg_out, dist])
            
        return segmented_matches
        
    except:
        return []

if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--name_out", type=str, help="Specify the name out variable")
    args = parser.parse_args()
    
    # Path to indexes of matched scores
    keep_idx_path = 'data/keep_idx.txt'
    
    # Initialize an empty list to store the kept indexes
    kept_indexes = []
    
    # Check if the keep_idx.txt file exists
    if os.path.exists(keep_idx_path):
        # If it exists, load the existing indexes from the file
        with open(keep_idx_path, 'r') as file:
            lines = file.readlines()
            kept_indexes = [int(line.strip()) for line in lines]
    
    matches = pickle.load(open("data/matches_short.p", "rb")) 
    matches = [matches[i] for i in kept_indexes]

    res = progress_map(segment_dtw, matches, process_timeout=600, n_cpu=6)
    pickle.dump(res, open(f"{args.name_out}.p", "wb"))

