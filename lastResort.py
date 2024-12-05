import itertools

def lastResort(lista_correta):
    """
    This function generates all permutations and combinations of the words in lista_correta,
    saves the results to a file called 'last_resort.txt'.
    """
    last_resort_words = set()  # Use a set to avoid duplicate words

    # Loop through each word in lista_correta
    for word in lista_correta:
        # Generate all possible permutations of lengths 2 up to the full length of the word
        for length in range(2, len(word) + 1):
            for perm in itertools.permutations(word, length):
                last_resort_words.add(''.join(perm))  # Add each permutation as a new word

    # Save all the brute-forced words to last_resort.txt
    with open('last_resort.txt', 'w') as last_resort_file:
        for word in sorted(last_resort_words):  # Sort words alphabetically before saving
            last_resort_file.write(word + '\n')

    print(f"Brute-forced words saved to 'last_resort.txt'.")