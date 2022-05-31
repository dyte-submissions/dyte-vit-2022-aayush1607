import argparse
import csv

access_token = None
username = None
repos = dict()


def set_token_username(token,user):
    access_token = token
    username = user

def set_input(path_to_csv_file):
    file = open(path_to_csv_file)
    csvreader = csv.reader(file)
    next(csvreader)

    for row in csvreader:
        repos[row[0]]=row[1]
        
    print(repos)
    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-input", action="store", type=str, help="Enter input file name", required=True
    )
    parser.add_argument(
        "-update",
        action="store_true",
        help="use for updating the version and creating pr",
    )
    parser.add_argument(
        "dependency", metavar="dep", type=str, help="Enter dependency_name@version"
    )

    args = parser.parse_args()

    print(args.input)
    print(args.dependency)
    print(args.update)
    
    if args.update:
        username=input('Enter github username:')
        token=input('Enter github access token:')
        set_token_username(token,username)

    set_input(path_to_csv_file=args.input)
