def min_distance_between_words_in_order(str, words):
    words_list = str.split()
    n = len(words)
    positions = [-1] * n  # Array to store positions of words in order
    minDistance = float('inf')
    current_word_index = 0

    for i in range(len(words_list)):
        if words_list[i] == words[current_word_index]:
            positions[current_word_index] = i
            current_word_index += 1
            
            # If we found all words in order at least once
            if current_word_index == n:
                # Calculate distance between first and last words
                current_distance = positions[-1] - positions[0]
                if current_distance < minDistance:
                    minDistance = current_distance
    
    # If we didn't find all words in order
    if current_word_index != n:
        return -1
    
    return minDistance

if __name__ == "__main__":
   print(min_distance_between_words_in_order("find nearest find nearest find store store a nearest store", ["find", "nearest", "store"]))
