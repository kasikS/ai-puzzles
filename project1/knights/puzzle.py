from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(AKnight, And(AKnight, AKnave)),
    # Implication(AKnight, And(AKnight, AKnave)),
    # Implication(AKnave, Not(And(AKnight, AKnave))),

    Biconditional(AKnight, Not(AKnave)),
    # Or(AKnave, AKnight),
    # Not(And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
Biconditional(AKnight, And(AKnave, BKnave)),
    # Implication(AKnight, And(AKnave, BKnave)),
    # Implication(AKnave, Not(And(AKnave, BKnave))),

    Biconditional(AKnight, Not(AKnave)),
    # Or(AKnave, AKnight),
    # Not(And(AKnight, AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # Or(BKnave, BKnight),
    # Not(And(BKnight, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),

    Biconditional(AKnight, Not(AKnave)),
    # Or(AKnave, AKnight),
    # Not(And(AKnight, AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # Or(BKnave, BKnight),
    # Not(And(BKnight, BKnave)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Or(AKnight, AKnave)),

    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    #Biconditional(BKnight, Implication(AKnave, Not(AKnave))),
    #
    # Implication(BKnave, Not(Implication(AKnight, AKnave))),
    # Implication(BKnave, Not(Implication(AKnave, Not(AKnave)))),

    Implication(CKnight, AKnight), # C says "A is a knight."
    Implication(CKnave, Not(AKnight)),

    Implication(BKnight, CKnave), # B says "C is a knave."
    Implication(BKnave, Not(CKnave)),

    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),
    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),
    Or(CKnave, CKnight),
    Not(And(CKnight, CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
