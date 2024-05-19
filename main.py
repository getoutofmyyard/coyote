import sys
sys.path.insert(1, '.\\scripts')
from splash import splash
from cli import cli

def main():
    splash()
    cli()

if __name__ == "__main__":
    main()
