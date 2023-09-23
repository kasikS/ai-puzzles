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
    people_set = set(people.keys())
    zero_genes = people_set - one_gene - two_genes
    no_trait = people_set - have_trait

    result = 1

    for person in zero_genes:
        genes_mother = genes_number(people[person]['mother'], one_gene, two_genes)
        genes_father = genes_number(people[person]['father'], one_gene, two_genes)

        # prob having number of genes
        if people[person]['mother'] is None and people[person]['father'] is None:
            result = result * prob_has_genes(0)
        else:
            result = result * prob_transfer(0, genes_mother) * prob_transfer(0, genes_father)
        # trait
        result = result * prob_trait(person,0, have_trait)

    for person in one_gene:
        genes_mother = genes_number(people[person]['mother'], one_gene, two_genes)
        genes_father = genes_number(people[person]['father'], one_gene, two_genes)

        # prob having number of genes
        if people[person]['mother'] is None and people[person]['father'] is None:
            result = result * prob_has_genes(1)
        else:
            result = result * (prob_transfer(0, genes_mother) * prob_transfer(1, genes_father) + prob_transfer(1, genes_mother) * prob_transfer(0, genes_father))

        # trait
        result = result * prob_trait(person, 1, have_trait)

    for person in two_genes:
        genes_mother = genes_number(people[person]['mother'], one_gene, two_genes)
        genes_father = genes_number(people[person]['father'], one_gene, two_genes)

        # prob having number of genes
        if people[person]['mother'] is None and people[person]['father'] is None:
            result = result * prob_has_genes(2)
        else:
            result = result * prob_transfer(1, genes_mother) * prob_transfer(1, genes_father)

        # trait
        result = result * prob_trait(person, 2, have_trait)

    return result


def prob_has_genes(genes):  # (genes_number, person, people): for future, when we have bigger tree
    return PROBS['gene'][genes]


def prob_transfer(genes_transferred, genes_parent):
    if genes_transferred == 0:
        if genes_parent == 0:
            return 1 - PROBS["mutation"]  # * prob_has_genes(0)
        elif genes_parent == 1:
            return 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])  # * prob_has_genes(1)
        elif genes_parent == 2:
            return PROBS["mutation"]  # * prob_has_genes(2)

    elif genes_transferred == 1:
        if genes_parent == 0:
            return PROBS["mutation"]  # * prob_has_genes(0)
        elif genes_parent == 1:
            return 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])  # * prob_has_genes(1)
        elif genes_parent == 2:
            return 1-PROBS["mutation"]  # * prob_has_genes(2)

    raise RuntimeError()


def genes_number(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def prob_trait(person, genes, have_trait):
    if person in have_trait:
        return PROBS["trait"][genes][True]
    else:
        return PROBS["trait"][genes][False]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    people_set = set(probabilities.keys())
    zero_genes = people_set - one_gene - two_genes
    no_trait = people_set - have_trait

    for person in zero_genes:
        probabilities[person]['gene'][0] += p

    for person in one_gene:
        probabilities[person]['gene'][1] += p

    for person in two_genes:
        probabilities[person]['gene'][2] += p

    for person in have_trait:
        probabilities[person]['trait'][True] += p

    for person in no_trait:
        probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for entry in probabilities.values():
        scale = 1/(entry['gene'][0] + entry['gene'][1] + entry['gene'][2])
        entry['gene'][0] *= scale
        entry['gene'][1] *= scale
        entry['gene'][2] *= scale

        scale = 1/(entry['trait'][False] + entry['trait'][True])
        entry['trait'][False] *= scale
        entry['trait'][True] *= scale


if __name__ == "__main__":
    main()
