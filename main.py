import sys 
import scanner

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()
    for filename in sys.argv[1:]:
        f = open(filename).read()
        s = scanner.Scanner()
        s.parse(f, False)#parse for classes, stand-alone functions, stand-alone vars 
        for c in s.types['classes']:#parse classes for member_functions and member_data 
            s.parse(c['body'][1:-1], True) 
        for t in s.types:
            print(t)
            for i in s.types[t]:
                print(i['identifier'])
            print('----------')   
main()
