import sys
import re 

types = ["int", "bool", "char", "void", "float", "bool", "double", 
"std::string", "std::vector<double>", ] #needs all cpp types 
keywords = ["const", "static", "public:", "private:", "virtual"] 
adts = ["class", "struct"]

#types we want to save 
variables = []
functions = []
classes = []
member_data = []
member_functions = []

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()
    for filename in sys.argv[1:]:
        f = open(filename).read()
        parsed_f = parse(f)#create tokens from file string
        classify(parsed_f)#classify tokens into lists above 
    for c in classes:
        parsed_c = parse(c['body'][1:-1])#create tokens inside class
        classify(parsed_c, True)


def parse(line):
    tokens = []#list of tuples ('type':'content')
    buffer = ''#for storing between states 
    stack = ''#for balancing parenthesis, braces..
    state = 'undefined'#initial state, change to list, body, expression or ignore
    for l in line:
        if l == '\n': #ignore escape characters 
            if state == 'ignore': state = 'undefined'#for backslashes 
            else: l = " "
        if state == 'undefined':
            if l == "(" or l == "{" or l == "=" or l == ";": #change state
                if len(buffer) > 0 and buffer.isspace() == False:#empty buffer 
                    for word in buffer.split():#create tokens not of type list, body or expression
                        if word in adts: tokens.append(('adt', word))
                        elif word in types: tokens.append(('type', word))
                        elif word in keywords: tokens.append(('keyword', word))
                        elif re.match("^[A-Za-z0-9_&-]*$", word): tokens.append(('identifier', word))
                        else: tokens.append(('undefined', word))
                    buffer =""
                if l == '(': state = 'list' 
                elif l == '{': state = 'body'
                else: state = 'expression'
            elif l == '/': state = 'ignore'
            else:
                buffer+=l
        if state == 'list' or state == 'body' or state == 'expression':
            if l == ')' or l == '}':
                stack =stack[0:-1]
            elif state == 'expression' and l == ';':
                stack =stack[0:-1]
            elif l == '(' or l == '{' or l == '=':
                stack += l
            buffer+=l
            if len(stack)==0:#create tokens of type list, expression or body 
                tokens.append((state, buffer))
                state = 'undefined'
                buffer = ''
    return tokens

def classify(parsed, c = False):#list of tokens, bool is_class
    obj = {}
    reg = ''
    for t in parsed:#iterate tokens in list 
        if len(reg) == 0 and t[0] == 'undefined': continue #funcs, vars, class must start with type, keyword, adt.. not undefined
        else:
            reg+=t[0][0]#add first letter of type into reg string
            if t[0] in obj: #key already exists in obj dictionary
                obj[t[0]+str(len(reg))] = t[1]
            else: obj[t[0]] = t[1] #new key 
        if t[0] == 'expression' or t[0] == 'body': #all declarations of vars end with expression, funcs/classes with body  
            obj['reg'] = reg
            if re.match('^aib$', reg): classes.append(obj)
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

main()
print('classes: ')
for c in classes:
    print(c['identifier'])
print('------')
print('member_functions: ')
for m in member_functions:
    print(m['identifier'])
print('------')
print('member_data: ')
for md in member_data:
    print(md['identifier'])
print('variables: ')
for v in variables:
    print(v['identifier'])
print('------')
print('functions: ')
for f in functions:
    print(f['identifier'])
print('------')


