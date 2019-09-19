import os, sys, re, smsClass
from consolemenu import *
from consolemenu.items import *
from prettytable import *
from colorama import init, Fore
# first message on the first occurance of #
smsMsgs = []
init()

'''
help function
'''
def help():
    print('Arguements:')
    print('\t-h:  \tdisplay help menu')
    print('\t-f:  \tpath to file (from cwd) %s' % os.getcwd())
    print('\t-o:  \tpath to output (default cwd: %s)' % os.getcwd())

'''
display all messages command
'''
def displayAll():
    smsTable = PrettyTable()
    smsTable.field_names = [Fore.BLACK+'Date'+Fore.WHITE, Fore.BLUE+'Type'+Fore.WHITE, Fore.LIGHTCYAN_EX+'Number'+Fore.WHITE, Fore.MAGENTA+'Message'+Fore.WHITE]
    for sms in smsMsgs:
        smsTable.add_row([Fore.BLACK+sms.get_date()+Fore.WHITE, Fore.BLUE+sms.get_type()+Fore.WHITE, Fore.LIGHTCYAN_EX+sms.get_number()+Fore.WHITE, Fore.MAGENTA+sms.get_message()+Fore.WHITE])
    print(smsTable)
    input('Continue')

'''
message counter
'''
def countMessages():
    # count all messages
    # list of the unique numbers
    numbers = []
    for sms in smsMsgs:
        if [sms.get_number(), 0] not in numbers:
            numbers.append([sms.get_number(), 0])
    total = len(smsMsgs)
    for sms in smsMsgs:
        number = sms.get_number()
        for i in range(len(numbers)):
            if number == numbers[i][0]:
                numbers[i][1] += 1
    messagesCount = PrettyTable()
    messagesCount.field_names = [Fore.GREEN+'Number'+Fore.WHITE, Fore.BLUE+'Number of messages'+Fore.WHITE, Fore.RED+'Percent Messaged'+Fore.WHITE]
    messagesCount.add_row([Fore.GREEN+'Total'+Fore.WHITE, Fore.BLUE+str(total)+Fore.WHITE, Fore.RED+'100%'+Fore.WHITE])
    def sortSecond(val):
        return val[1]
    numbers.sort(key = sortSecond, reverse = True)
    for number in numbers:
        percent = number[1] / total
        percent *= 100
        percent = str(percent)
        messagesCount.add_row([Fore.GREEN+number[0]+Fore.WHITE, Fore.BLUE+str(number[1])+Fore.WHITE, Fore.RED+percent+Fore.WHITE])
    print(messagesCount)
    input('Continue')

'''
menu function will return index of method to call, args
'''
def menu():
    menu = ConsoleMenu('SMS Dump Analyzer', 'Main Menu')
    display = FunctionItem('Display All Messages', displayAll)
    analytics = FunctionItem('Count Messages', countMessages)
    menu.append_item(display)
    menu.append_item(analytics)
    menu.show()


# need to interpret args
filename = ''
output = '' # need to figure out how to format the output
args = sys.argv
if len(args) == 1:
    # no args specified    
    print('No arguements specified')
    help()
    sys.exit(0)
else:
    # will interpret
    if '-h' in args:
        help()
        sys.exit(0)
    else:
        for i in range(len(args)):
            if '-f' in args[i]:
                if len(args) < i+1:
                    help()
                    print('No file specified')
                    sys.exit(0)
                filename = args[i+1]
                if not os.path.isfile(filename):
                    print('File does not exist: %s' % filename)
                    sys.exit(0)
            if '-o' in args[i]:
                if len(args) > i+1:
                    help()
                    print('No output specified, using default')
                else:
                    output = args[i+1]

    # after the args interpretation
    # read the file
    messages = []
    with open(filename, 'r') as smsDump:
        allLines = smsDump.readlines()
        for i in range(len(allLines)):
            # need to take the lines from the first # to the next #
            first = -1
            second = -1
            if '#' in allLines[i]:
                first = i
                for k in range(first+1, len(allLines)):
                    if '#' in allLines[k]:
                        second = k
                        break
            # now need to concat all the rows inbtw
            msg = ''
            for j in range(first+1, second-1):
                line = allLines[j]
                line = line.replace('\t', '').replace('\n','')
                msg += line+'\n'
            if msg != '':
                messages.append(msg)
                i+=second
        smsDump.close()
    
    for msg in messages:
        # convert them to SMS variables
        try:
            msg = msg.split('\n')
            date = msg[1].replace('Date: ','')
            type = msg[0].replace('Type: ','')
            number = msg[2].replace('Address: ','').replace('+1','').replace('(','').replace(')','').replace('-','').replace(' ','').strip()
            message = msg[4].replace('Message: ','').replace('$U$','')
            if '0x' in message:
                index = message.find('0x')
                message = message[:index]
            smsMsgs.append(smsClass.SMS(date, number, message, type))
        except Exception as e:
            #print('exception with: %s' % msg)
            i = 0
            # invalid number
    
    smsMsgs.sort(key=smsClass.SMS.get_number, reverse=True)
    
    menu()
