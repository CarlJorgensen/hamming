#!/usr/bin/env python3

import random
from heapq import heappush, heappop, heapify
#from collections import defaultdict
import numpy as np


letters = [chr(i) for i in range(ord('a'), ord('p')+1)]
random_probs = [random.random() for _ in range(16)]
total_prob = sum(random_probs)
probabilities = {letters[i]: random_probs[i] / total_prob for i in range(16)}

print(probabilities)


def huffman_coding(probabilities):
    heap = [[weight, [symbol, ""]] for symbol, weight in probabilities.items()]
    heapify(heap)

    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


probabilities = {'a': 0.12203875810129212, 'b': 0.020509263365227078,
                 'c': 0.02714211596554311, 'd': 0.14192492337915266,
                 'e': 0.027127842520334976, 'f': 0.13955669953962205,
                 'g': 0.02515812755438861, 'h': 0.06428070468180194,
                 'i': 0.09467323604956333, 'j': 0.017027460818087058,
                 'k': 0.011860298516799277, 'l': 0.06466591969498053,
                 'm': 0.08908382996310737, 'n': 0.06071359217118773,
                 'o': 0.06486072095037503, 'p': 0.029376506728537168}

entropy = -np.sum([p * np.log2(p) for p in probabilities.values()])

codes = huffman_coding(probabilities)

code_dict = {item[0]: item[1] for item in codes}

avg_length = np.sum([len(code) * prob for symbol, prob in probabilities.items() for code in [code_dict[symbol]]])

print("Entropy:", entropy)
print("Average length:", avg_length)


def is_prefix_free(codes):
    for code1 in codes.values():
        for code2 in codes.values():
            if code1 != code2 and code1.startswith(code2):
                return False
    return True


for letter, code in code_dict.items():
    print(f"{letter}: {code}")


def huffman_decoding(encoded_string, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    bits = ''
    decoded_output = []

    for bit in encoded_string:
        bits += bit
        if bits in reverse_codes.keys():
            decoded_output.append(reverse_codes[bits])
            bits = ''

    return decoded_output


encoded_string = "01001101110011001111111011110000"
decoded_symbols = huffman_decoding(encoded_string, code_dict)

print("Decoded symbols:", decoded_symbols)