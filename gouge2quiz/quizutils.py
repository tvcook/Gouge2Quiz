import subprocess

class quiz:
    def __init__(self, pdf):
        self.rawtxtlist = []
        self.questions = []
        self.exam = None
        self.bank = []

        self.pdftotext(pdf)
        self.texttoquizdata(self.rawtxtlist)

    # Helper Functions:

    def pdftotext(self, pdf, page=None):
        """Retrieve all text from a PDF file.

        Arguments:
            pdf Path of the file to read.
            page: Number of the page to read. If None, read all the pages.

        Returns:
            A list of lines of text.
        """
        if page is None:
            args = ['pdftotext', '-layout', '-q', pdf, '-']
        else:
            args = ['pdftotext', '-f', str(page), '-l', str(page), '-layout',
                    '-q', pdf, '-']
        try:
            txt = subprocess.check_output(args, universal_newlines=True)
            lines = txt.splitlines()
        except subprocess.CalledProcessError:
            lines = []

        self.rawtxtlist = lines

    def texttoquizdata(self, linelist):
        """Convert lines of text into question objects

        Arguments:
            linelist: list of lines from PDF

        Returns:
            A list question objects
        """
        linelist = filter(None, linelist)
        num = 1
        found = False
        # multi line pointer
        start = 0
        tmp = quiz.quizquestion()

        for i in range(0, len(linelist)):
            linelist[i] = linelist[i].lstrip()
            cur = linelist[i]
            if cur.find(str(num)) is 0 and not found:
                tmp.number = len(self.questions) + 1
                found = True
                start = i+1
            if cur.find('Exam') is not -1:
                self.exam = linelist[i].split('Exam', 1)[-1].lstrip()
            if cur.find('Bank Name:') is not -1:
                bank = linelist[i].split('Bank Name:', 1)[-1].lstrip()
                self.bank.append(bank)
            if found:
                if cur.find('A.') is not -1:
                    # save question
                    tmp.question = ' '.join(linelist[start:i])
                    # clean up answer
                    linelist[i] = linelist[i].split('A.', 1)[-1].lstrip()
                    start = i
                elif cur.find('B.') is not -1:
                    # save answer A
                    tmp.answers['A'] = ' '.join(linelist[start:i])
                    # clean up answer
                    linelist[i] = linelist[i].split('B.', 1)[-1].lstrip()
                    start = i
                elif cur.find('C.') is not -1:
                    # save answer B
                    tmp.answers['B'] = ' '.join(linelist[start:i])
                    # clean up answer
                    linelist[i] = linelist[i].split('C.', 1)[-1].lstrip()
                    start = i
                elif cur.find('D.') is not -1:
                    # save answer C
                    tmp.answers['C'] = ' '.join(linelist[start:i])
                    # clean up answer
                    linelist[i] = linelist[i].split('D.', 1)[-1].lstrip()
                    start = i
                elif cur.find('Correct') is not -1:
                    if '(TRUE/FALSE)' in tmp.question:
                        # save answer B
                        tmp.answers['B'] = ' '.join(linelist[start:i])
                    else:
                        # save answer D
                        tmp.answers['D'] = ' '.join(linelist[start:i])
                    # save correct answer
                    tmp.answer = linelist[i].split('Correct', 1)[-1].lstrip()
                    # save and reset variables
                    #printQuestion(tmp)
                    self.questions.append(self.quizquestion(tmp))
                    tmp.reset()
                    if num >= 50:
                        num = 1
                    else:
                        num += 1
                    found = False
                else:
                    pass
                    #clean up extraneous characters
                    if cur[0] in ('O', 'R', 'D', 'E'):
                        linelist[i] = cur.lstrip('O R D E')

        self.bank = ', '.join(set(self.bank))

    # Debugging:

    def printquiz(self):
        """Print quiz for debugging purposes

        Arguments:
            None
        Returns:
            None
        """
        print("Exam: " + self.exam)
        print("Test Bank: " + self.bank)
        for question in self.questions:
            print("#" + str(question.number))
            print(question.question)
            print("A. " + question.answers['A'])
            print("B. " + question.answers['B'])
            if '(TRUE/FALSE)' not in question.question:
                print("C. " + question.answers['C'])
                print("D. " + question.answers['D'])
            print("Correct answer: " + question.answer)

    def printrawtxtlist(self):
        """Print rawtxtlist for debugging purposes

        Arguments:
            None
        Returns:
            None
        """
        for line in self.rawtxtlist:
            print(line)

    class quizquestion:
        def __init__(self, orig=None):
            if orig is None:
                self.non_copy_constructor()
            else:
                self.copy_constructor(orig)

        def non_copy_constructor(self):
            self.number = None
            self.question = None
            self.answers = {'A': None, 'B': None, 'C': None, 'D': None}
            self.answer = None

        def copy_constructor(self, orig):
            self.number = orig.number
            self.question = orig.question
            self.answers = {'A': orig.answers['A'], 'B': orig.answers['B'], 'C': orig.answers['C'], 'D': orig.answers['D']}
            self.answer = orig.answer

        def reset(self):
            self.number = None
            self.question = None
            self.answers = {'A': None, 'B': None, 'C': None, 'D': None}
            self.answer = None

def main():
    import sys
    CEND = '\33[0m'
    CRED = '\33[31m'

    if len(sys.argv) < 2:
        print(CRED + "Error: No PDF source provided..." + CEND)
    else:
        quizobj = quiz(sys.argv[1])
        if len(sys.argv) == 2:
            quizobj.printrawtxtlist()
        elif len(sys.argv) == 3:
            if sys.argv[2] in '-quiz':
                quizobj.printquiz()
            else:
                print(CRED + "Error: Unknown argument..." + CEND)
if __name__ == "__main__":
    main()
