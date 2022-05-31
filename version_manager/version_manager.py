import argparse
import csv
import requests
import base64
import json

access_token = None
username = None
repos = dict()
github_api_url = "https://api.github.com/repos/"


def set_token_username(token, user):
    access_token = token
    username = user


def set_input(path_to_csv_file):
    file = open(path_to_csv_file)
    csvreader = csv.reader(file)
    next(csvreader)

    for row in csvreader:
        repos[row[0].strip()] = row[1].strip()

    file.close()


def version_compare(v1, v2):

    a1 = v1.split(".")
    a2 = v2.split(".")
    n = len(a1)
    m = len(a2)

    a1 = [int(i) for i in a1]
    a2 = [int(i) for i in a2]

    if n > m:
        for i in range(m, n):
            a2.append(0)
    elif m > n:
        for i in range(n, m):
            a1.append(0)

    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(a1)):
        if a1[i] > a2[i]:
            return 1
        elif a2[i] > a1[i]:
            return -1
    return 0


def get_api_url(repo_url):
    _, url = repo_url.split("https://github.com/")
    url = github_api_url + url
    if url[-1] != "/":
        url += "/"
    url += "contents/package.json"
    return url

def create_fork(owner, repo_name, auth_token):
    payload = {
        owner: owner,
        repo_name: repo_name
    }
    data=json.dumps(payload)
    print(data)
    url = github_api_url+str(owner)+"/"+str(repo_name)+"/forks"
    print('url',url)
    usern = 'aayush1607'

    rpost = requests.post(url, auth=(usern, auth_token), data=data)
    print(rpost)


def check_versions(dependency, version):
    output = []
    for repo in repos:
        out_res = [repo, repos[repo]]
        url = get_api_url(repos[repo])
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            req = req.json()
            content = base64.b64decode(req["content"])
            package_json = json.loads(content)
            actual_version = package_json["dependencies"][dependency]
            if actual_version[0] == "^":
                actual_version = actual_version[1:]
            out_res.append(actual_version)
            if (
                dependency in package_json["dependencies"]
                and version_compare(actual_version, version) >= 0
            ):
                out_res.append(True)
            else:
                out_res.append(False)
        output.append(out_res)
        print(*out_res)
    return output

# def update_versions(checked_output, dependency, version):
#     for repo,repo_url,actual_version,isupdated in checked_output:
#         if not isupdated:
#             create_fork()

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
        username = input("Enter github username:")
        token = input("Enter github access token:")
        set_token_username(token, username)

    set_input(path_to_csv_file=args.input)

    dep, ver = args.dependency.split("@")
    checked_output=check_versions(dependency=dep, version=ver)

    # if args.update:
    #     updated_output=update_versions(checked_output, dependency, version)