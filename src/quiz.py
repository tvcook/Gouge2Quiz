

#Main

def main():
    from random import shuffle
    from quizutils import quiz
    import sys

    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CRED    = '\33[31m'
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    missedindex = []
    score = 0

    print("                                                                                                          ")
    print("  /$$$$$$                                                 /$$$$$$         /$$$$$$            /$$          ")
    print(" /$$__  $$                                               /$$__  $$       /$$__  $$          |__/          ")
    print("| $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$       |__/  \ $$      | $$  \ $$ /$$   /$$ /$$ /$$$$$$$$")
    print("| $$ /$$$$ /$$__  $$| $$  | $$ /$$__  $$ /$$__  $$        /$$$$$$/      | $$  | $$| $$  | $$| $$|____ /$$/")
    print("| $$|_  $$| $$  \ $$| $$  | $$| $$  \ $$| $$$$$$$$       /$$____/       | $$  | $$| $$  | $$| $$   /$$$$/ ")
    print("| $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/      | $$            | $$/$$ $$| $$  | $$| $$  /$$__/  ")
    print("|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$      | $$$$$$$$      |  $$$$$$/|  $$$$$$/| $$ /$$$$$$$$")
    print(" \______/  \______/  \______/  \____  $$ \_______/      |________/       \____ $$$ \______/ |__/|________/")
    print("                               /$$  \ $$                                      \__/                        ")
    print("                              |  $$$$$$/                                                                  ")
    print("                               \______/                                                                   ")
    print("                                                                                                          ")
    print("$ - Written by: Tanner Cook")
    print("$ - Version: 1.0")
    for i in range(3):
        print("$")

    print("$ - Loading PDF...")
    if len(sys.argv) < 2:
        print("$ - " + CRED + "Error: No PDF source provided..." + CEND)

    else:
        data = quiz(sys.argv[1])
        shuffle(data.questions)

        print("$ - " + CGREEN + "PDF loaded successfully!" + CEND)
        print("$ - " + "There are " + str(len(data.questions)) + " questions available.")
        print("$ - How many questions would you like to include in the quiz? ")

        while True:
            try:
                input = int(raw_input("$ - Please a number between 1 and " + str(len(data.questions))  + ": "))
            except ValueError:
                print("$ - " + CRED + "Error: Enter a number within the given range." + CEND)
                continue

            if input < 1 and input > len(data.questions):
                print("$ - " + CRED + "Error: Enter a number within the given range." + CEND)
                continue
            else:
                break

        print("$ - Let's begin...")
        print("$")
        print("$ - " + CYELLOW + "Exam: " + data.exam + CEND)
        print("$ - " + CYELLOW + "Test Bank: " + data.bank + CEND)
        print("$")

        for i in range(input):
            count = 7
            print("$ - " + CBOLD + "(" + str(i) + "/" + str(input) + ")" + CEND)
            print("$")
            print("$ - " + CBOLD + str(data.questions[i].number) + ": " + data.questions[i].question + CEND)
            print("$")
            print("$ - A. " + data.questions[i].answers['A'])
            print("$ - B. " + data.questions[i].answers['B'])
            print("$ - C. " + data.questions[i].answers['C'])
            print("$ - D. " + data.questions[i].answers['D'])
            print("$")
            print("$")

            while True:
                selection = raw_input("$ - Enter selection: ")
                if selection.lower() not in ('a', 'b', 'c', 'd'):
                    count += 2
                    print("$ - " + CRED + "Error: Please select A, B, C, or D" + CEND)
                else:
                    break

            for _ in range(count):
                sys.stdout.write(CURSOR_UP_ONE + ERASE_LINE)
                sys.stdout.flush()

            def printanswer(ans, letter, i):
                if i.answer in letter:
                    # print green
                    i.answers[letter] = CGREEN + letter + ". " + i.answers[letter] + CEND
                    print("$ - " + i.answers[letter])
                elif ans in letter.lower() and i.answer not in letter:
                    # print red
                    i.answers[letter] = CRED + letter + ". " + i.answers[letter] + CEND
                    print("$ - " + i.answers[letter])
                else:
                    # print white
                    i.answers[letter] = letter + ". " + i.answers[letter]
                    print("$ - " + i.answers[letter])

            printanswer(selection, 'A', data.questions[i])
            printanswer(selection, 'B', data.questions[i])
            printanswer(selection, 'C', data.questions[i])
            printanswer(selection, 'D', data.questions[i])

            if selection.upper() in data.questions[i].answer:
                score += 1
                print("$ - " + CGREEN + "Correct! :)" + CEND)
                print("$")
            else:
                missedindex.append(i)
                print("$ - " + CRED + "Incorrect! :("+ CEND)
                print("$")

            raw_input("$ - Press Enter to continue...")

            for _ in range(11):
                sys.stdout.write(CURSOR_UP_ONE + ERASE_LINE)
                sys.stdout.flush()


    percentage = (float(score)/float(input)) * 100
    print("$ - Your score is " + str(percentage) + "% (" + str(score) + "/" + str(input) + ")")
    print("$")

    while True:
        sel = raw_input("$ - Would you like to review your missed questions? (Yes/No) ")
        if sel.lower() not in ('y', 'n', 'yes', 'no'):
            print("$ - " + CRED + "Error: Please enter Yes/No" + CEND)
        else:
            break

    if sel.lower() in ('y', 'yes'):
        for index in missedindex:
            print("$")
            print("$ - " + CBOLD + str(data.questions[index].number) + ": " + data.questions[index].question + CEND)
            print("$")
            print("$ - A. " + data.questions[index].answers['A'])
            print("$ - B. " + data.questions[index].answers['B'])
            print("$ - C. " + data.questions[index].answers['C'])
            print("$ - D. " + data.questions[index].answers['D'])
            print("$")

    print("$")
    print("$ - Bye!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n$ - Bye!")
