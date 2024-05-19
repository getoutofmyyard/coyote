import subprocess

def newline():
    print('')

def read_file(filepath):
    # Reads a file. Used most often for help files.
    try:
        with open(filepath,'r') as file:
            print(file.read())
            newline()
    except:
        newline()
        print('error~! Help file ' + filepath + ' is missing.')
        newline()

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    print(decoded_output.strip())