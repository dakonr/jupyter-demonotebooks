#!/usr/bin/python
import uvicorn
import sys
import getopt
import os

def main(argv):
    os.environ['DEV'] = '1'
    host_addr = 'localhost'
    port_num = '8088'
    #parse arguments
    try:
        opts, args = getopt.getopt(argv, 'h:p:l:', ['host=', 'port=', 'dev='])
    except getopt.GetoptError:
        print('main.py --host <host> --port <port> --dev <dev 1=True, other=false>')
        sys.exit(2)
    for opt, arg in opts:
        print(arg)
        if opt == '--help':
            print('test.py --host <host> --port <port> --dev <dev 1=True, other=false>')
            sys.exit()
        elif opt in ('-h', '--host'):
            host_addr = arg
        elif opt in ('-p', '--port'):
            port_num = arg
        elif opt in ('-d', '--dev'):
            os.environ["DEV"] = arg
            print('dev =' + os.environ.get('DEV'))
    #Development Mode
    if int(os.environ.get('DEV')) == 1:
        host_addr = 'localhost'
        port_num = '8000'

    uvicorn.run('app:app', host=host_addr, port=int(port_num), reload=True)


if __name__ == '__main__':
    main(sys.argv[1:])
