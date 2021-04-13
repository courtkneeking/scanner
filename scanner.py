import re 

class Scanner:
    recognize = dict(
        types = {"int", "bool", "char", "void", "float", "bool", "double", 
        "std::string", "std::vector<double>", "std::vector<std::string>", "std::vector<float>"},#needs all cpp types 
        keywords = {"const", "static", "public:", "public", "private:", "private", "virtual"
        },
        adts =  {"class", "struct"},
        discard =  {"PYBIND11_MODULE", "PYBIND11_PLUGIN"},
        change_state = '({=;',
        escape_chars = {'\n', '\t'})
    regexes = dict(
        is_class = '^aiu?k?i?b$',#adt-identifier-(optional-undefined,keyword,identifier)-endswithbody
        is_function = 'k?til.*b$', #optional(keyword)type-identifier-list-endswithbody
        is_variable =  'k?tie.*$', #optional(keyword)-type-identifer-expression 
        is_constructor = 'k?il.*b$')#optional(keyword)-identifer-list-endswithbody 
    def __init__(self):
        self.tokens = [] #list of tuples ('type':'content')
        self.buffer = '' #for storing between states 
        self.stack = '' #for balancing parentheses, braces..
        self.state = 'undefined' #initial state, change to list, body, expression 
        self.types = dict(
            variables = [],
            functions = [],
            classes = [],
            member_data = [],
            member_functions = [],
        )

    def empty_buffer(self):
        for word in self.buffer.split():#create tokens not of type list, body or expression
            if word in Scanner.recognize['discard']: continue
            elif word in Scanner.recognize['adts']: self.tokens.append(('adt', word))
            elif word in Scanner.recognize['types']: self.tokens.append(('type', word))
            elif word in Scanner.recognize['keywords']: self.tokens.append(('keyword', word))
            elif re.match("^[A-Za-z0-9_&-]*$", word): self.tokens.append(('identifier', word))
            else: self.tokens.append(('undefined', word))   
            self.buffer =""

    def create_token(self):
        self.tokens.append((self.state, self.buffer))
        self.state = 'undefined'
        self.buffer = ''

    def parse(self, line, c=False):
        self.tokens = []
        ignore = ''
        for l in line:
            if ignore:
                if ignore.endswith('*/') or (ignore.startswith('//') and l == '\n'):
                    ignore = ""#exit ignore
                else:
                    ignore+=l
                    continue
            elif self.buffer.endswith('//') or self.buffer.endswith('/*'):
                ignore= self.buffer[-2:]+l#start ignore 
                self.buffer = self.buffer[:-2]
                continue
            l = " " if l in Scanner.recognize['escape_chars'] else l
            if self.state == 'undefined':
                if l in Scanner.recognize['change_state']: 
                    if len(self.buffer) > 0:
                        self.empty_buffer()
                    if l == '(': self.state = 'list' 
                    elif l == '{': self.state = 'body'
                    else: self.state = 'expression'
            self.buffer+=l
            if self.state == 'list':
                if l == ')': self.stack =self.stack[0:-1]
                elif l == '(': self.stack += l
                if len(self.stack)==0:
                    self.create_token()
            elif self.state == 'body':
                if l == '}': self.stack =self.stack[0:-1]
                elif l == '{': self.stack += l
                if len(self.stack)==0:
                    self.create_token()
            elif self.state == 'expression' and l == ';': self.create_token()
        self.classify(c)

    #create objects from token stream
    #assumption: all declarations of vars,funcs,classes start with keyword,identifier,type,adt and end with expression or body 
    def classify(self, c):#c bool is_class
        obj = {}
        reg = ''
        for t in self.tokens:
            if len(reg) == 0 and t[0] == 'undefined': #throw away
                continue 
            else: #append first letter of type to reg string, add token to object
                reg+=t[0][0]
                if t[0] in obj: #check if token type already exists in obj dict to avoid data loss
                    obj[t[0]+str(len(reg))] = t[1]
                else: obj[t[0]] = t[1]  
            if t[0] == 'expression' or t[0] == 'body':#classify object using regex string  
                obj['reg'] = reg
                if re.match(Scanner.regexes['is_class'], reg): self.types['classes'].append(obj)
                elif re.match(Scanner.regexes['is_function'], reg): 
                    if c == True: self.types['member_functions'].append(obj)
                    else: self.types['functions'].append(obj)
                elif re.match(Scanner.regexes['is_variable'], reg): 
                    if c == True: self.types['member_data'].append(obj)
                    else: self.types['variables'].append(obj)
                elif re.match(Scanner.regexes['is_constructor'], reg): 
                    self.types['member_functions'].append(obj)
                obj = {}
                reg = ''
