import sys 
import scanner
import classifier

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()
    for filename in sys.argv[1:]:
        f = open(filename).read()
        parsed_f = scanner.parse(f)#create tokens from file string
        classifier.classify(parsed_f)
    for c in classifier.classes:
        parsed_c = scanner.parse(c['body'][1:-1])#create tokens inside class
        classifier.classify(parsed_c, True)

def p():
    print('classes: ')
    for c in classifier.classes:
        print(c['identifier'])
    print('------')
    print('member_functions: ')
    for m in classifier.member_functions:
        print(m['identifier'])
    print('------')
    print('member_data: ')
    for md in classifier.member_data:
        print(md['identifier'])
    print('------')
    print('variables: ')
    for v in classifier.variables:
        print(v['identifier'])
    print('------')
    print('functions: ')
    for f in classifier.functions:
        print(f['identifier'])
    print('------')

main()
p()