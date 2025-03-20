import os
import random
import re
import sys

# Damping Factor - probablity that a link is selected from the current page. Otherwise a page from the corpus is switched to at random.
DAMPING = 0.85
SAMPLES = 10000


def main():
    """ Main function to run pagerank algorithm """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    If a page has no outgoing links, returns an equal probability for all pages in the corpus
    """

    probability = {}
    # Assigning the rest of damping factor probability 
    # equally to all pages of corpus 
    for i in corpus:
        probability[i] = (1 - damping_factor) / len(corpus)

    # Equal distribution of damping factor probability 
    # among links of given page
    if corpus[page]:
        for link in corpus[page]:
            probability[link] += damping_factor / len(corpus[page])
            
    # Equal distribution of damping factor probability among 
    # all pages if given page has no links
    else:
        for link in corpus:
            probability[link] += damping_factor / len(corpus)
    
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    In this case sampling would be more accurate by directly
    sampling, without transition model.
    """

    samples = {}
    for i in corpus:
        samples[i] = 0
    
    # Random page to start at
    first_page = random.choice(list(corpus.keys()))

    # Sampling n number of times
    iterations = n
    while iterations > 0:
        # Random number from 1 to 100 for implementing
        # damping factor
        percent = random.randint(1, 100)

        # Implementing restart of randomly opening page 
        # based on damping factor
        if percent > damping_factor * 100:
            first_page = random.choice(list(corpus.keys()))

        # Opening random link among the links on that page
        link = ""
        if corpus[first_page]:
            link = random.choice(list(corpus[first_page]))
        elif not corpus[first_page]:
            link = random.choice(list(corpus.keys()))

        # Avoiding to open link that leads to the same page
        if link == first_page:
            continue

        # Counting the number of times a page has been viewed
        else:
            samples[link] += 1
            first_page = link
        iterations -= 1

    # Approximate normalization
    for i in samples:
        samples[i] /= n

    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Assigning equal probability to every page
    iter_ranks = {}
    for i in corpus:
        iter_ranks[i] = 1 / len(corpus)

    # Dictionary for calculating page probability changes
    compare_ranks = {}
    for i in corpus:
        compare_ranks[i] = 0

    # Probability based only on damping factor and number of pages
    unconditional_probability = (1 - damping_factor) / len(corpus)

    # Looping until there is no significant probability changes
    loop = 1
    while loop > 0.001:
        loop = 0
        # Calculating probability for page to be next chosen one
        for page in corpus:
            next_page_probability = 0
            for next_page in corpus:
                # if possible next page has no links
                if len(corpus[next_page]) == 0:
                    next_page_probability += iter_ranks[next_page] * (1 / len(corpus))
                # If possible next page has link to page
                elif page in corpus[next_page]:
                    next_page_probability += iter_ranks[next_page] / len(corpus[next_page])
                
            # Calculating joint probability for page and 
            new_probability = unconditional_probability + damping_factor * next_page_probability

            # Adding  new probability to dictionary for comparing with previous probability
            compare_ranks[page] = new_probability
 
        # Normalising probabilities of comparing dictionary
        normalisation_factor = abs(1 - sum(i for i in compare_ranks.values())) / len(compare_ranks)
        if sum(i for i in compare_ranks.values()) > 1:
            for page in compare_ranks:
                compare_ranks[page] -= normalisation_factor
        elif sum(i for i in compare_ranks.values()) < 1:
            for page in compare_ranks:
                compare_ranks[page] += normalisation_factor 
        
        # Checking if there is significant changes in probabilities
        for page in iter_ranks:
            if abs(iter_ranks[page] - compare_ranks[page]) > 0.001:
                loop = 1

        # Assigning newly calculated probabilities
        for i in iter_ranks:
            iter_ranks[i] = compare_ranks[i]

    return iter_ranks 

        
if __name__ == "__main__":
    main()