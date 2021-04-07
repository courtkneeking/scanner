import re 
import classifier

types = ["int", "bool", "char", "void", "float", "bool", "double", 
"std::string", 
"std::vector<double>", "std::vector<std::string>", "std::vector<float>" ] #needs all cpp types 
keywords = ["const", "static", "public:", "public", "private:", "private", "virtual"] 
adts = ["class", "struct"]
discard = ["PYBIND11_MODULE", "PYBIND11_PLUGIN"]
change_state = '({=;'
escape_chars = {'\n', '\t'}
def parse(line):
    tokens = [] #list of tuples ('type':'content')
    buffer = '' #for storing between states 
    stack = '' #for balancing parenthesis, braces..
    state = 'undefined' #initial state, change to list, body, expression 

    ignore_stack = ''
    ignore_bool = False

    for l in line:
        if ignore_bool == True:
            if ignore_stack.startswith('//') and l == '\n':#exit ignore
                ignore_bool = False
                ignore_stack = ""
            elif ignore_stack.endswith('*/'):
                ignore_bool = False
                ignore_stack = ""
            else:
                ignore_stack+=l
                continue
        elif buffer.endswith('//') or buffer.endswith('/*'):#start ignore 
            ignore_bool = True
            ignore_stack = buffer[-2:]+l
            buffer = buffer[:-2]
            continue
        l = " " if l in escape_chars else l
        if state == 'undefined':
            if l in change_state: #change state
                if len(buffer) > 0:#empty buffer 
                    for word in buffer.split():#create tokens not of type list, body or expression
                        if word in discard: continue
                        elif word in adts: tokens.append(('adt', word))
                        elif word in types: tokens.append(('type', word))
                        elif word in keywords: tokens.append(('keyword', word))
                        elif re.match("^[A-Za-z0-9_&-]*$", word): tokens.append(('identifier', word))
                        else: tokens.append(('undefined', word))   
                    buffer =""
                if l == '(': state = 'list' 
                elif l == '{': state = 'body'
                else: state = 'expression'
        buffer+=l
        if state == 'list':
            if l == ')': stack =stack[0:-1]
            elif l == '(': stack += l
            if len(stack)==0:#create tokens of type list, expression or body 
                tokens.append((state, buffer))
                state = 'undefined'
                buffer = ''
        elif state == 'body':
            if l == '}': stack =stack[0:-1]
            elif l == '{': stack += l
            if len(stack)==0:#create tokens of type list, expression or body 
                tokens.append((state, buffer))
                state = 'undefined'
                buffer = ''
        elif state == 'expression':
            if l == ';':
                tokens.append((state, buffer))
                state = 'undefined'
                buffer = ''
    return tokens
