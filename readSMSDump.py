import os, sys, re, smsClass
from consolemenu import *
from consolemenu.items import *
from prettytable import *
from colorama import init, Fore
import machineLearningMessage
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
        percent = percent[:percent.find('.')+3]
        messagesCount.add_row([Fore.GREEN+number[0]+Fore.WHITE, Fore.BLUE+str(number[1])+Fore.WHITE, Fore.RED+percent+'%'+Fore.WHITE])
    print(messagesCount)
    input('Continue')

'''
colorize function
'''
def colorize(fields, colors):
    string = []
    for i in range(len(fields)):
        string.append(str(colors[i])+str(fields[i])+Fore.WHITE)
    return string

'''
ratio of incoming to outgoing per person
'''
def ratio():
    # [number,  # incoming, # outgoing]
    numbers = []
    for sms in smsMsgs:
        if [sms.get_number(), 0, 0] not in numbers:
            numbers.append([sms.get_number(), 0, 0])
    for sms in smsMsgs:
        # now to detemine the type
        type = sms.get_type()
        if 'Incoming' in type:
            for i in range(len(numbers)):
                if sms.get_number() in numbers[i][0]:
                    numbers[i][1] += 1
        elif 'Outgoing' in type:
            for i in range(len(numbers)):
                if sms.get_number() in numbers[i][0]:
                    numbers[i][2] += 1

    ratioTable = PrettyTable()
    ratioTable.field_names = colorize(['Number', 'Incoming', 'Outgoing', 'Ratio (Incoming / Outgoing)'], [Fore.BLUE, Fore.RED, Fore.GREEN, Fore.MAGENTA])
    
    # sort method
    def getRatio(number):
        inC = int(number[1])
        out = int(number[2])
        if out != 0:
            return (inC/out)
        else:
            return -1

    numbers.sort(key = getRatio, reverse = True)
    for number in numbers:
        incoming = int(number[1])
        outgoing = int(number[2])
        if outgoing != 0:
            ratio = incoming / outgoing
            ratio = str(ratio)
            ratio = ratio[:ratio.find('.')+3]
        elif outgoing == 0:
            ratio = '0 Outgoing'        
        if incoming == 0:
            ratio = '0 Incoming'
        ratioTable.add_row(colorize([number[0], number[1], number[2], ratio], [Fore.BLUE, Fore.RED, Fore.GREEN, Fore.MAGENTA]))
    print(ratioTable)
    input('Continue')

'''
find most popular time with # of messages and % of total vs # sent in this time
'''
def timeRatio():
    # 1 hour time blocks
    # list of lists
    timeList = []
    for i in range(0, 24):
        timeList.append(0)
    for sms in smsMsgs:
        time = sms.get_date()
        split = time.split(' ')
        hour = int(split[1].split(':')[0])
        timeList[hour] += 1
    totalMsg = len(smsMsgs)

    newList = []
    for i in range(len(timeList)):
        newList.append([i, timeList[i]])

    # sort method
    def second(val):
        return val[1]

    newList.sort(key = second, reverse = True)

    timeRatio = PrettyTable()
    timeRatio.field_names = colorize(['Hour','Total Messages','Percentage Activity'], [Fore.GREEN, Fore.BLUE, Fore.RED])

    # to 12 hr
    def hr12(time):
        time+=7
        if time > 24:
            return str(time-24)+ 'AM'
        if time > 12:
            return str(time-12)+' PM'
        if time == 12:
            return str(time) + ' PM'
        else:
            return str(time) + ' AM'

    for i in newList:
        ratio = (i[1] / totalMsg)*100
        ratio = str(ratio)
        ratio = ratio[:ratio.find('.')+3]
        timeRatio.add_row(colorize([hr12(i[0]), i[1], ratio+'%'], [Fore.GREEN, Fore.BLUE, Fore.RED]))
    print(timeRatio)


    input('')

'''
look for popular words
'''
def machineIt():
    msgList= []
    for sms in smsMsgs:
        msgList.append(sms.get_message())
    machineLearningMessage.similarCheck(msgList)
    input('')


'''
menu function will return index of method to call, args
'''
def menu():
    menu = ConsoleMenu('SMS Dump Analyzer', 'Main Menu')
    display = FunctionItem('Display All Messages', displayAll)
    analytics = FunctionItem('Count Messages', countMessages)
    ratioBtn = FunctionItem('Ratio Incoming / Outgoing', ratio)
    timeBtn = FunctionItem('Time ratio', timeRatio)
    learning = FunctionItem('Find Used Words', machineIt)
    menu.append_item(display)
    menu.append_item(learning)
    menu.append_item(timeBtn)
    menu.append_item(analytics)
    menu.append_item(ratioBtn)
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
