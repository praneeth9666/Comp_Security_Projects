#!/usr/bin/python3

import sys, math, functools, time
from collections import Counter

#taken from Wikipedia
letter_freqs = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02361,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
plain_text = 'ethicslawanduniversitypolicieswarningtodefendasystemyouneedtobeabletot\
hinklikeanattackerandthatincludesunderstandingtechniquesthatcanbeusedt\
ocompromisesecurityhoweverusingthosetechniquesintherealworldmayviolate\
thelawortheuniversitysrulesanditmaybeunethicalundersomecircumstancesev\
enprobingforweaknessesmayresultinseverepenaltiesuptoandincludingexpuls\
ioncivilfinesandjailtimeourpolicyineecsisthatyoumustrespecttheprivacya\
ndpropertyrightsofothersatalltimesorelseyouwillfailthecourseactinglawf\
ullyandethicallyisyourresponsibilitycarefullyreadthecomputerfraudandab\
useactcfaaafederalstatutethatbroadlycriminalizescomputerintrusionthisi\
soneofseverallawsthatgovernhackingunderstandwhatthelawprohibitsifindou\
btwecanreferyoutoanattorneypleasereviewitsspoliciesonresponsibleuseoft\
echnologyresourcesandcaenspolicydocumentsforguidelinesconcerningproper'
def vigenere_encrypt(plaintext, key):
    """Encrypts the given plaintext using the Vigenère cipher with the provided key."""
    plaintext = plaintext.upper()
    key = key.upper()
    extended_key = (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]
    ciphertext = []
    for p_char, k_char in zip(plaintext, extended_key):
        if p_char in alphabet:
            shift = (alphabet.index(p_char) + alphabet.index(k_char)) % 26
            ciphertext.append(alphabet[shift])
        else:
            ciphertext.append(p_char)
    
    return ''.join(ciphertext)



def pop_var(s):
    """Calculate the population variance of letter frequencies in given string."""
    freqs = Counter(s)
    mean = sum(float(v)/len(s) for v in freqs.values())/len(freqs)
    return sum((float(freqs[c])/len(s)-mean)**2 for c in freqs)/len(freqs)
def mean_frequency_variance(ciphertext, key_length):
    """Calculate the mean of the frequency variances for each Caesar cipher in the Vigenère ciphertext."""
    variances = []
    for i in range(key_length):                                  # Get every k-th character starting from index i
        group = ciphertext[i::key_length]
        variance = pop_var(group)
        variances.append(variance)
    mean_variance = sum(variances) / len(variances)             # Calculate the mean of these variances
    return mean_variance

def index_of_coincidence(segment):
    """Calculate the Index of Coincidence for a given text segment."""
    freqs = Counter(segment)
    N = len(segment)
    ic = sum(freq * (freq - 1) for freq in freqs.values()) / (N * (N - 1))
    return ic

def best_key_length(ciphertext):
    """Determine the most likely key length."""
    best_key_length = 2
    min_variance = float('inf')
    ic_threshold = 0.065                            # Index of Coincidence for English is around 0.065

    for key_length in range(2, 14):
        variance = mean_frequency_variance(ciphertext, key_length)
        ic_values = [index_of_coincidence(ciphertext[i::key_length]) for i in range(key_length)]
        avg_ic = sum(ic_values) / len(ic_values)                    
        if variance < min_variance and avg_ic > ic_threshold - 0.01:    # Check variance and IC to determine the best key length
            min_variance = variance
            best_key_length = key_length

    return best_key_length


def chi_squared_statistic(s):
    """Calculate chi-squared statistic comparing the letter frequencies of s to English letter frequencies."""
    expected_freq = {char: len(s) * freq for char, freq in letter_freqs.items()}
    observed_freq = Counter(s)
    chi_sq = 0.0
    for char in alphabet:
        expected = expected_freq.get(char, 0)
        observed = observed_freq.get(char, 0)
        chi_sq += ((observed - expected) ** 2) / expected if expected != 0 else 0
    return chi_sq

def get_caesar_shift(text):
    """Find the best Caesar shift that matches English frequencies using the chi-squared test."""
    min_chi_sq = float('inf')
    best_shift = 0
    for shift in range(26):
        shifted_text = ''.join(alphabet[(alphabet.index(c) - shift) % 26] for c in text)
        chi_sq = chi_squared_statistic(shifted_text)
        if chi_sq < min_chi_sq:
            min_chi_sq = chi_sq
            best_shift = shift
    return best_shift

def find_key(ciphertext, key_length):
    """Determine the Vigenère key given the ciphertext and key length."""
    key = []
    for i in range(key_length):
        group = ciphertext[i::key_length]
        shift = get_caesar_shift(group)
        key_char = alphabet[shift]
        key.append(key_char)
    return ''.join(key)



if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "").upper()
    
    #################################################################
    # Your code to determine the key and decrypt the ciphertext here
    '''print(pop_var(plain_text))
        # Test the function
    key = "yz"
    cipher_text = vigenere_encrypt(plain_text, key)
    #print(f"Plaintext:  {plain_text}")
    #print(f"Key:        {key}")
    #print(f"Ciphertext: {cipher_text}")
    print(pop_var(cipher_text))
    print(mean_frequency_variance(cipher_text,2))
    key = "uvwxyz"
    cipher_text = vigenere_encrypt(plain_text, key)
    print(mean_frequency_variance(cipher_text,2))
    print(mean_frequency_variance(cipher_text,3))
    print(mean_frequency_variance(cipher_text,4))
    print(mean_frequency_variance(cipher_text,5))'''
    best_key_len = best_key_length(cipher) #find the length of the key
    key = find_key(cipher, best_key_len) #Guessing the key based on length
    print(key)

