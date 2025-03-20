import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initialization of the joint probability
    j_probability = 1

    for i in people:
        # Initialization of personal probability
        probability = 1

        # Finding number of genes of given person
        num_of_genes = 0
        if i in one_gene:
            num_of_genes = 1
        elif i in two_genes:
            num_of_genes = 2

        # Finding if given person have trait
        has_trait = False
        if i in have_trait:
            has_trait = True

        # If no parents (always are both missing), use default values:
        if not people[i]["mother"]:
            probability *= PROBS['gene'][num_of_genes]

        # Else calculate probability of number of genes from parents:
        else:
            # Calculating the probability that mother is giving a copy 
            # of mutated gene to her child
            m_probability = PROBS["mutation"]
            if people[i]["mother"] in two_genes:
                m_probability = 1 - PROBS['mutation']
            elif people[i]["mother"] in one_gene:
                m_probability = 0.5

            # Calculating the probability that father is giving a copy 
            # of mutated gene to his child
            f_probability = PROBS["mutation"]
            if people[i]["father"] in two_genes:
                f_probability = 1 - PROBS['mutation']
            elif people[i]["father"] in one_gene:
                f_probability = 0.5
            
            # If the child has 2 mutated genes, it got them from both parents
            # so it is independent probability
            if num_of_genes == 2:
                probability *= m_probability * f_probability

            # If child has 1 mutated gene, than we need to calculate probability
            # of inheriting it from the mother OR the father
            elif num_of_genes == 1:
                probability *= (1 - m_probability) * f_probability + \
                    (1 - f_probability) * m_probability
            
            # If the child hasn't mutated genes, it didn't get them from parents
            # so it is independent probability
            else:
                probability *= (1 - m_probability) * (1 - f_probability)

        # Finding joint probability of having or not having mutated genes
        # and having or not having trait
        probability *= PROBS['trait'][num_of_genes][has_trait]
        j_probability *= probability
    return j_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for i in probabilities:

        num_of_genes = 0
        if i in one_gene:
            num_of_genes = 1
        if i in two_genes:
            num_of_genes = 2

        has_trait = False
        if i in have_trait:
            has_trait = True

        # Updating probability distributions of gene and trait
        probabilities[i]['gene'][num_of_genes] += p

        probabilities[i]['trait'][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """   
    for i in probabilities:
        # Finding sum of gene probability distrubution
        gene_sum = sum(probabilities[i]["gene"].values())

        # Normalization of gene probabilities 
        for key in probabilities[i]["gene"]:
            probabilities[i]['gene'][key] /= gene_sum
            
        # Finding sum of trait probability distrubution
        trait_sum = sum(probabilities[i]["trait"].values())

        # Normalization of trait probabilities 
        for key in probabilities[i]["trait"]:
            probabilities[i]['trait'][key] /= trait_sum
    return probabilities

    
if __name__ == "__main__":
    main()
