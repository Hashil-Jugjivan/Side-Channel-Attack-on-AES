import random
import scipy
from scipy import stats
import matplotlib.pyplot as plot
import numpy as np
import csv

def calculate_hamming_weight(plain_text_index_byte, each_key_byte_guess):
    plain_text_index_byte_int = int(plain_text_index_byte) # Convert Decimal String to Integer
    each_key_byte_guess_int = each_key_byte_guess

    added_round_key = plain_text_index_byte_int ^ each_key_byte_guess_int # XOR
    high_nibble = (added_round_key >> 4) & 0xF # 4 bits each for high nibble
    low_nibble = added_round_key & 0xF # 4 bits each for low nibble

    sbox = sbox_arr[high_nibble][low_nibble] # sbox lookup

    if isinstance(sbox, str): # Accept strings like '0x89'
        sbox = int(sbox, 16)
    hamming_weight = bin(sbox).count('1') # Calculate Hamming Weight
    return hamming_weight

def pearson_calculation(key_guess_predictions, actual_power_values):
    try:
        corr_mat = np.corrcoef(key_guess_predictions, actual_power_values)
        corr_value = abs(corr_mat[0,1])
    except:
        for i in range(len(actual_power_values)):
            actual_power_values[i] = float(actual_power_values[i])
        corr_mat = np.corrcoef(key_guess_predictions, actual_power_values)
        corr_value = abs(corr_mat[0,1])
    return corr_value 

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

sbox_arr = [] # Holds the 2D Sbox (16x16) from the original 1D Sbox list
for i in range(0, len(Sbox), 16): # Get Sbox in 16x16 matrix
    row = []
    for j in range(16):
        row.append(Sbox[i+j]) # Grab the indiviual Sbox values
    sbox_arr.append(row)
for row_index in range(16): # Convert all values in 2D sbox_arr to Hex String
    for col_index in range(16):
        sbox_arr[row_index][col_index] = hex(sbox_arr[row_index][col_index])
# print("sbox_arr: ", sbox_arr)





csv_data = list(csv.reader(open('waveform.csv', 'r')))
# print(csv_data)
model_traces = len(csv_data)
waveform_datapoints = len(csv_data[0])
print("Model Traces: {0}, Waveform Datapoints: {1}".format(model_traces, waveform_datapoints))

# 16 Bytes Key (128 Bits), but each byte of the key is 8 Bits, from 0x00 (0) to 0xFF (256)
key_bruteforce_list = []
for i in range(0, 256):
    key_bruteforce_list.append(i)

plain_text_list = []
cipher_text_list = []
power_values_list = []
for row in csv_data:
    plain_text_list.append(row[0]) # Final print(len(plain_text_list)) # Output: 110
    cipher_text_list.append(row[1]) # Final print(len(cipher_text_list)) # Output: 110
    power_values_list.append(row[2:]) # Final print(len(power_values_list)) # Output: 110
# power_values = [
#   [t1_p1, t1_p2, t1_p3, ..., t1_p2500],  # Trace for plaintext 1, aka Encryption 1
#   [t2_p1, t2_p2, t2_p3, ..., t2_p2500],  # Trace for plaintext 2, aka Encryption 2
#       ...
#   [t110_p1, t110_p2, t110_p3, ..., t110_p2500],  # Trace for plaintext 110, aka Encryption 110
# ]
plain_text_length = len(plain_text_list[0]) # Just use the first element to get the length, Output: 32 hex chars = 16 bytes
cipher_text_length = len(cipher_text_list[0]) # Just use the first element to get the length, Output: 32 hex chars = 16 bytes


# Transpose the power values to group by time index
power_values_transposed = []
for i in range(len(power_values_list[0])): # Assume all traces with same length of 2500
    time_slice = []
    for trace in power_values_list:
        time_slice.append(trace[i])
    power_values_transposed.append(time_slice)
power_values_transposed = power_values_transposed[:2500] # Keep only the first 2500 time indices in case there are more
# power_values_transposed = [
#   [t1_p1, t2_p1, t3_p1, ..., t110_p1],  # All traces at time index 1
#   [t1_p2, t2_p2, t3_p2, ..., t110_p2],  # All traces at time index 2
#       ...
#   [t1_p2500, t2_p2500, t3_p2500, ..., t110_p2500],  # All traces at time index 2500
# ]

key = []
key_count = 1
for index in range(0, plain_text_length, 2): # Because Each Byte (ie 0x2B) is 2 Hex Chars; Index = 0, 2, 4, ..., 30; a total of 16 ITERATIONS because 16 Bytes
    # Build a matrix of Hamming Weights for each key guess VS each plaintext; given the key index byte (1 of 16 bytes)
    
    hw_of_all_plaintexts_with_different_keys = [] # 2D Matrix that stores PREDICTED power leakge (Hamming Weights) for the indexed byte for all plaintexts, each tested across 256 possible key guesses
    for plain_text in plain_text_list: # Iterate through all 110 plaintexts
        # plain_text_index_byte is the decimal value of the indexed byte in the plaintext
        plain_text_index_byte = str(int(plain_text[index:index+2], 16)) # Convert hex string of plain text indexed byte to decimal string

        hw_of_plaintext_but_with_different_keys = []
        for each_guessed_key_byte in key_bruteforce_list: # Guess/Iterate Key from 0x00 to 0xFF (1 byte, 8 bits)
            calculated_hamming_weight = calculate_hamming_weight(plain_text_index_byte, each_guessed_key_byte)
            hw_of_plaintext_but_with_different_keys.append(calculated_hamming_weight)

        hw_of_all_plaintexts_with_different_keys.append(hw_of_plaintext_but_with_different_keys) # Append the list of hamming weights for each key guess
    # print(len(hw_of_all_plaintexts_with_different_keys)) # Output of 110 different plaintexts
    # print(len(hw_of_all_plaintexts_with_different_keys[0])) # Output of 256 different key guesses per plaintext

    hw_of_all_plaintexts_with_different_keys_transposed = [] # Flip the rows and columns around
    number_of_plaintexts = len(hw_of_all_plaintexts_with_different_keys) # 110 plaintexts
    number_of_different_keys = len(hw_of_all_plaintexts_with_different_keys[0]) # Should be 256, one for each key guess
    for each_different_key in range(number_of_different_keys):
        new_row = []
        for each_different_plaintext in range(number_of_plaintexts):
            new_row.append(hw_of_all_plaintexts_with_different_keys[each_different_plaintext][each_different_key])
        hw_of_all_plaintexts_with_different_keys_transposed.append(new_row) # Append the new row to the transposed matrix
    # print(len(hw_of_all_plaintexts_with_different_keys_transposed)) # Output of 256 different key guesses per plaintext
    # print(len(hw_of_all_plaintexts_with_different_keys_transposed[0])) # Output of 110 different plaintexts per key


    # Now Compare Expected Leakage (Hamming Weights) with Measured Power Traces Values (Actual Leakage)
    # - We already have a matrix of predicted power leakages for all possible key guesses (via Hamming weight)
    # - A matrix of actual power measurements from the device during encryption (after transpose)
    # - Finds which key guess has the highest Pearson correlation with the actual power measurements; which means it's the best match, and thus likely the correct key byte

    matrix_correlation_scores = [] # For each key guess row, compute correlation with every power trace point (column)

    # Iterate list of 256 rows, each representing the predicted leakage (Hamming weights) for one key guess across all plaintexts
    for key_guess_index in range(len(hw_of_all_plaintexts_with_different_keys_transposed)): # Looping through each key guess from 0 to 255
        key_guess_predictions = hw_of_all_plaintexts_with_different_keys_transposed[key_guess_index] # Predicted leakage (e.g., Hamming weight of the S-box output) for that specific key guess across all 110 plaintexts
        # print(len(key_guess_predictions)) # Output: 110 plaintexts

        correlations_with_all_timepoints = [] # Store correlation score between key guess and each time point here

        for time_index in range(len(power_values_transposed)): # Looping through each time point from 0 to 2499
            actual_power_values = power_values_transposed[time_index] # Actual power measured at that specific moment across all plaintexts

            # Compute correlation between "Predicted 110 Hamming weights for this key guess" & "110 Actual power measurements at this specific time index"
            # IF they correlate well, maybe this key guess is correct, and this time index is when the SBox operation happened.
            correlation = pearson_calculation(key_guess_predictions, actual_power_values)
            correlations_with_all_timepoints.append(correlation) # Save the correlation score for this time point

        # After testing this key guess with all time indices, save the list of correlation scores.
        matrix_correlation_scores.append(correlations_with_all_timepoints)

    # Now find the position of the maximum correlation score for each key guess
    max_correlation_per_key_guess = [max(correlations) for correlations in matrix_correlation_scores]
    best_key_guess = np.argmax(max_correlation_per_key_guess) # Get the best key guess
    best_time_index_for_that_key = np.argmax(matrix_correlation_scores[best_key_guess])
    best_correlation_value = matrix_correlation_scores[best_key_guess][best_time_index_for_that_key]
    best_key_guess_hex = hex(best_key_guess) # Convert the best key guess to hex

    key.append(best_key_guess_hex) # Append the best key guess to the key list
    print("Key Byte {0}: {1} ({2}) from Time Index {3} with Correlation Value {4}".format(key_count, best_key_guess, best_key_guess_hex, best_time_index_for_that_key, best_correlation_value)) # Print the best key guess and its hex value
    key_count += 1

    """
    # Plotting
    plot.figure(figsize=(12, 6))
    plot.plot(range(256), matrix_correlation_scores, color='blue', linewidth=1.5)
    plot.title('Pearson Correlation of Key Guesses vs Actual Power Trace')
    plot.xlabel('Key Byte Guess (0 to 255)')
    plot.ylabel('Correlation Value')
    plot.grid(True)
    plot.axvline(x=best_key_guess, color='red', linestyle='--', label=f'Correct Key: {best_key_guess}')
    plot.legend()
    plot.tight_layout()
    plot.show()
    """

print(key)