import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    true_false = lambda v: 1 if v == 'TRUE' else 0

    def convert_data(row):
        months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9,
                  'Nov': 10, 'Dec': 11}
        visitor_type = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 2}

        integers = [0, 2, 4, 11, 12, 13, 14]
        floats = [1, 3, 5, 6, 7, 8, 9]

        for index in range(len(row)):
            if index in integers:
                row[index] = int(row[index])
            elif index in floats:
                row[index] = float(row[index])
            elif index == 10:
                row[10] = months[row[10]]
            elif index == 15:
                row[15] = visitor_type[row[15]]
        # row[16] = 1 if row[16] == 'TRUE' else 0
            elif index == 16:
                row[16] = true_false(row[16])
            else:
                raise RuntimeError
        return row

    with open(filename) as csvfile:
        userdata = csv.reader(csvfile)
        next(userdata)
 #       evidence, label = [convert_data(row[0:17])  for row in userdata]
        # label = [1 if row[17] == 'TRUE' else 0 for row in userdata]
 #       label = [true_false(row[17]) for row in userdata]

        evidence = []
        label = []
        for row in userdata:
            evidence.append(convert_data(row[0:17]))
            label.append(true_false(row[17]))
    return evidence, label


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    alg = KNeighborsClassifier(n_neighbors=1)
    alg.fit(evidence, labels)
    return alg



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    predicted_positive = 0
    actual_positive = 0
    predicted_negative = 0
    actual_negative = 0

    for label, prediction in zip(labels, predictions):
        if label:
            actual_positive += 1
            if prediction:
                predicted_positive += 1
        else:
            actual_negative += 1
            if not prediction:
                predicted_negative += 1
    sensitivity = predicted_positive/actual_positive
    specificity = predicted_negative/actual_negative

    return sensitivity, specificity


if __name__ == "__main__":
    main()
