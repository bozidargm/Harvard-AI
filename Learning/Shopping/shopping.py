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
    labels = []
    evidences = []
    month = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
             "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}

    with open(filename) as file:
        line = csv.DictReader(file)
        for i in line:
            evidence = []
            evidence.append(int(i['Administrative']))
            evidence.append(float(i['Administrative_Duration']))
            evidence.append(int(i['Informational']))
            evidence.append(float(i['Informational_Duration']))
            evidence.append(int(i['ProductRelated']))
            evidence.append(float(i['ProductRelated_Duration']))
            evidence.append(float(i['BounceRates']))
            evidence.append(float(i['ExitRates']))
            evidence.append(float(i['PageValues']))
            evidence.append(float(i['SpecialDay']))
            evidence.append(month[i['Month']])
            evidence.append(int(i['OperatingSystems']))
            evidence.append(int(i['Browser']))
            evidence.append(int(i['Region']))
            evidence.append(int(i['TrafficType']))
            evidence.append(1 if i['VisitorType'] == 'Returning_Visitor' else 0)
            evidence.append(0 if i['Weekend'] == "FALSE" else 1)
            labels.append(0 if i['Revenue'] == "FALSE" else 1)
            evidences.append(evidence)
          
    return (evidences, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Making instance of K-Nearest Neighbor Classifier
    # that konsider 1 nearest neighbor
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit model
    model.fit(evidence, labels)

    return model


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
    # Positive and negative labels
    total_positive = labels.count(1)
    total_negative = labels.count(0)

    # Correctly predicted positives and negatives
    true_positive = 0
    true_negative = 0

    for i in range(len(labels)):
        # Counting right predictions
        if labels[i] == 1 and predictions[i] == 1:
            true_positive += 1
        elif labels[i] == 0 and predictions[i] == 0:
            true_negative += 1

    # Calculating prediction rate
    sensitivity = true_positive / total_positive
    specificity = true_negative / total_negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
