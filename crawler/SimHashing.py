from hashlib import md5

# from zlib import crc32

def SimHash(frequencies, numBits:int=64) -> tuple():
    """Compute a similarity hash for the passed in dict.
    
    Parameters
    ----------
    frequencies : dict
        a dict containing URL tokens (key) and the corresponding count (value)
    
    numBits : int
        number of bits to represent the hash (32,64)
    
    Returns
    -------
    tuple
        a tuple containing a binary vector representation of the dict passed in
    """
    # NOTE: Implementation for md5 below
    hashes = dict()
    for key in frequencies.keys():
        hash_v = md5(key.encode()).digest()[:8] # byte representation
        hashes[key] = hash_v # store hash values into hashes

    binary_vector = ""
    for bit_index in range(numBits):
        value = 0
        byte_index = bit_index // 8 # create a byte_index using bit_index in the range
        for key, hash_v in hashes.items():
            # preform bit-shift operation (which is shifting bit_index % 8 spots) 
            # on the hash's byte value to target a specific bit
            # then use that bit with the AND operation
            if (hash_v[byte_index] >> (bit_index%8)) & 1:
                value += frequencies[key] # if bit is 1 then we add the frequency to the value
            else:
                value -= frequencies[key] # if bit is 0 we subtract the frequency to the value
        if value >= 0:
            binary_vector += "1" # append 1 if value is non-negative
        else:
            binary_vector += "0" # append 0 if value is negative
    '''
    NOTE: Implementation for crc32 below
    for bit_index in range(32):
        value = 0
        byte_index = bit_index
        for key, hash in hashes.items():
            if (hash >> bit_index) & 1:
                value += frequencies[key]
            else:
                value -= frequencies[key]
        if value >= 0:
            binary_vector.append(1)
        else:
            binary_vector.append(0)
    '''
    return binary_vector

def ComputeSimHashSimilarity(vector1, vector2):
    """Compute the sim hash similarity between two tuples.
    
    Parameters
    ----------
    vector1 : string
        a string containing binary vector representation of it's similarity score
    vector2 : string
        a string containing binary vector representation of it's similarity score
        
    Returns
    -------
    int
        an int indicating the number of bits similar between the two tuple hash vectors (vector1 & vector2)
    """
    count = 0
    for i in range(len(vector1)):
        if vector1[i] == vector2[i]:
            count += 1
    return count

# Hearty's Tests

def TestComputeSimHash():
    string1 = """
    The Importance of Healthy Eating

    Healthy eating is essential for maintaining overall well-being and preventing chronic diseases. A balanced diet rich in fruits, vegetables, whole grains, and lean proteins provides the necessary nutrients for the body to function optimally. Proper nutrition boosts the immune system, enhances energy levels, and promotes mental clarity.
    Incorporating a variety of foods into your diet ensures you get a wide range of vitamins and minerals. For example, leafy greens are high in vitamins A, C, and K, while citrus fruits provide a good source of vitamin C. Whole grains like oats and brown rice offer fiber, which aids in digestion and helps maintain a healthy weight.
    Healthy eating also plays a significant role in disease prevention. Consuming a diet high in antioxidants from fruits and vegetables can reduce the risk of heart disease, cancer, and other illnesses. Additionally, reducing the intake of processed foods, sugar, and unhealthy fats can help prevent conditions like obesity, diabetes, and hypertension.
    Developing healthy eating habits from a young age can lead to long-term benefits. Teaching children the importance of nutrition can establish lifelong healthy habits. Preparing meals at home and involving children in the cooking process can make healthy eating enjoyable and educational.
    In conclusion, prioritizing healthy eating is vital for maintaining physical and mental health. By making informed food choices and incorporating a variety of nutritious foods into your diet, you can enhance your quality of life and reduce the risk of chronic diseases. Start making small changes today for a healthier future.
    """

    string2 = """
    The Significance of Nutritious Eating
    Nutritious eating is crucial for sustaining overall health and avoiding chronic ailments. A well-rounded diet that includes fruits, vegetables, whole grains, and lean proteins supplies the body with essential nutrients needed for optimal performance. Good nutrition strengthens the immune system, improves energy levels, and supports mental sharpness.
    Incorporating diverse foods into your diet guarantees an ample supply of vitamins and minerals. For instance, leafy greens are rich in vitamins A, C, and K, whereas citrus fruits are excellent sources of vitamin C. Whole grains such as oats and brown rice provide fiber, which aids digestion and assists in weight management.
    Nutritious eating is also key in preventing diseases. A diet abundant in antioxidants from fruits and vegetables can lower the risk of heart disease, cancer, and other health issues. Moreover, cutting down on processed foods, sugar, and unhealthy fats can help avert conditions like obesity, diabetes, and high blood pressure.
    Instilling nutritious eating habits from an early age can yield long-lasting advantages. Educating children about the significance of nutrition can foster lifelong healthy practices. Cooking meals at home and involving children in meal preparation can make healthy eating both fun and instructive.
    In summary, focusing on nutritious eating is essential for both physical and mental well-being. By making smart food choices and including a variety of nutrient-dense foods in your diet, you can improve your life quality and minimize the risk of chronic diseases. Begin making gradual changes today for a healthier tomorrow

    """

    text1_tokens = Tokenize(string1)
    text2_tokens = Tokenize(string2)

    text1_freqMap = ComputeTokenFreq(text1_tokens)
    text2_freqMap = computeTokenFreq(text2_tokens)

    assert sim_hash(text1_freqMap) != (), "The function returned an empty tuple"
    assert sim_hash(text2_freqMap) != (), "The function returned an empty tuple"

    print(sim_hash(text1_freqMap))
    print(sim_hash(text2_freqMap))

    print("All test cases passed")

def TestComputeSimilarity():
    string1 = """
    The Importance of Healthy Eating
    Healthy eating is essential for maintaining overall well-being and preventing chronic diseases. A balanced diet rich in fruits, vegetables, whole grains, and lean proteins provides the necessary nutrients for the body to function optimally. Proper nutrition boosts the immune system, enhances energy levels, and promotes mental clarity.
    Incorporating a variety of foods into your diet ensures you get a wide range of vitamins and minerals. For example, leafy greens are high in vitamins A, C, and K, while citrus fruits provide a good source of vitamin C. Whole grains like oats and brown rice offer fiber, which aids in digestion and helps maintain a healthy weight.
    Healthy eating also plays a significant role in disease prevention. Consuming a diet high in antioxidants from fruits and vegetables can reduce the risk of heart disease, cancer, and other illnesses. Additionally, reducing the intake of processed foods, sugar, and unhealthy fats can help prevent conditions like obesity, diabetes, and hypertension.
    Developing healthy eating habits from a young age can lead to long-term benefits. Teaching children the importance of nutrition can establish lifelong healthy habits. Preparing meals at home and involving children in the cooking process can make healthy eating enjoyable and educational.
    In conclusion, prioritizing healthy eating is vital for maintaining physical and mental health. By making informed food choices and incorporating a variety of nutritious foods into your diet, you can enhance your quality of life and reduce the risk of chronic diseases. Start making small changes today for a healthier future.
    """

    string2 = """
    The Significance of Nutritious Eating
    Nutritious eating is crucial for sustaining overall health and avoiding chronic ailments. A well-rounded diet that includes fruits, vegetables, whole grains, and lean proteins supplies the body with essential nutrients needed for optimal performance. Good nutrition strengthens the immune system, improves energy levels, and supports mental sharpness.
    Incorporating diverse foods into your diet guarantees an ample supply of vitamins and minerals. For instance, leafy greens are rich in vitamins A, C, and K, whereas citrus fruits are excellent sources of vitamin C. Whole grains such as oats and brown rice provide fiber, which aids digestion and assists in weight management.
    Nutritious eating is also key in preventing diseases. A diet abundant in antioxidants from fruits and vegetables can lower the risk of heart disease, cancer, and other health issues. Moreover, cutting down on processed foods, sugar, and unhealthy fats can help avert conditions like obesity, diabetes, and high blood pressure.
    Instilling nutritious eating habits from an early age can yield long-lasting advantages. Educating children about the significance of nutrition can foster lifelong healthy practices. Cooking meals at home and involving children in meal preparation can make healthy eating both fun and instructive.
    In summary, focusing on nutritious eating is essential for both physical and mental well-being. By making smart food choices and including a variety of nutrient-dense foods in your diet, you can improve your life quality and minimize the risk of chronic diseases. Begin making gradual changes today for a healthier tomorrow

    """
    text1_tokens = tokenize(string1)
    text2_tokens = tokenize(string2)

    text1_freqMap = computeTokenFreq(text1_tokens)
    text2_freqMap = computeTokenFreq(text2_tokens)

    hash1 = sim_hash(text1_freqMap)
    hash2 = sim_hash(text2_freqMap)
    
    assert compute_sim_hash_similarity(hash1, hash2) != 0

    print(compute_sim_hash_similarity(hash1, hash2))
    print("All test cases passed")
    
    

if __name__ == "__main__":
    # d1 = {"high":1, "low":1, "begging":1}
    # d2 = {"high":6, "low":20, "begging":1}
    # hash1 = sim_hash(d1)
    # hash2 = sim_hash(d2)
    
    # print(hash1,hash2)
    # print(compute_sim_hash_similarity(hash1, hash2))

    TestComputeSimHash()
    TestComputeSimilarity()
             