import re

variables = []
functions = []
classes = []
member_data = []
member_functions = []

def classify(parsed, c = False):#list of tokens, bool is_class
    obj = {}
    reg = ''
    for t in parsed:#iterate tokens in list 
        if len(reg) == 0 and t[0] == 'undefined': 
            continue #funcs, vars, class must start with type, keyword, adt.. not undefined
        else:
            reg+=t[0][0]#add first letter of type into reg string
            if t[0] in obj: #key already exists in obj dictionary
                obj[t[0]+str(len(reg))] = t[1]
            else: obj[t[0]] = t[1] #new key 
        if t[0] == 'expression' or t[0] == 'body': #all declarations of vars end with expression, funcs/classes with body  
            obj['reg'] = reg
            # print('reg', reg)
            # print('obj', obj)
            if re.match('^aiu?k?i?b$', reg): classes.append(obj)
            elif re.match('k?til.*b$', reg): #optional(keyword)type-identifier-list-*-body
                if c == True: member_functions.append(obj)
                else: functions.append(obj)
            elif re.match('k?tie.*$', reg): #optional(keyword)-type-identifer-expression 
                if c == True: member_data.append(obj)
                else: variables.append(obj)
            elif re.match('k?il.*b$', reg): #to catch class instantiation 
                member_functions.append(obj)
            obj = {}
            reg = ''

