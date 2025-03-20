import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Defining context-free grammar rules
NONTERMINALS = """
S -> NP VP 

NP -> N | Det N | Det Adj N | NP PP 
PP -> P NP
VP -> V | V NP | V N P | VP Conj VP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    processed_sentence = []

    # Sentence tokenization
    tokenized = nltk.word_tokenize(sentence)

    # Making list of valid tokens
    for word in tokenized:
        if any(letter.isalpha() for letter in word):
            processed_sentence.append(word.lower())

    return processed_sentence


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP_chunks = []

    # Ekstracting solo noun phrase chunks using nltk.tree functions
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            chunk = subtree
            # Checking if noun phrase chunk has noun phrase inside
            while True:
                for branch in chunk.subtrees():
                    if branch.label() == "NP":
                        chunk = branch
                else:
                    break
            NP_chunks.append(chunk)

    return NP_chunks


if __name__ == "__main__":
    main()
