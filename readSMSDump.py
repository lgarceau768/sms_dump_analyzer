import os, sys, re, smsClass

# first message on the first occurance of #

'''
help function
'''
def help():
    print('Arguements:')
    print('\t-h:  \tdisplay help menu')
    print('\t-f:  \tpath to file (from cwd) %s' % os.getcwd())
    print('\t-o:  \tpath to output (default cwd: %s)' % os.getcwd())



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
    
    smsMsgs = []
    for msg in messages:
        # convert them to SMS variables
        try:
            msg = msg.split('\n')
            date = msg[1].replace('Date: ','')
            type = msg[0].replace('Type: ','')
            number = msg[2].replace('Address: ','').replace('+1','')
            number = number[:3]+'-'+number[3:6]+'-'+number[6:]
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
    
    number = input('Please enter a number to retrieve the messages: ')

    for sms in smsMsgs:
        if sms.get_number() == number:
            print(sms)
