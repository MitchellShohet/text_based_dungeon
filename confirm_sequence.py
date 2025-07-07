def confirm_sequence(question, confirmation_text, denial_text):
    choosing = True
    confirm = False
    while choosing == True:
        print(question)
        print(" YES")
        print(" NEVERMIND")
        selection = input("\n - ").upper()
        if selection == "NO" or selection == "NEVERMIND" or selection == "NOPE" or selection == "NOE":
            choosing = False
            print(denial_text)
        elif selection == "YES":
            confirm = True
            choosing = False
            print(confirmation_text)
        else: print(" Please answer YES or NEVERMIND")
    return confirm
