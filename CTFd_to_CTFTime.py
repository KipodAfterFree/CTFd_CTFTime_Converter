import requests
from sys import stderr
from json import dumps

HOSTNAME = "https://ctf.kaf.sh"
API = HOSTNAME + "/api/v1/scoreboard"


def convert(ctfd_json):
    """Receives a CTFd endpoint url, and prints out the CTFTime scoreboard feed"""
    if ctfd_json["success"] != True:
        print("Couldn't download the scoreboard", file=stderr)
        return

    teams = ctfd_json["data"]

    # Filter to teams that actually played
    teams = sorted(teams, key=lambda team: team["score"], reverse=True)
    teams = filter(lambda team: team["score"] > 0, teams)

    # Sort teams
    ctftime_teams = []

    for teamnum, team in enumerate(teams):
        ctftime_teams.append(
            {"pos": teamnum + 1, "team": team["name"], "score": team["score"]}
        )
    return {"standings": ctftime_teams}


def main():
    scoreboard = requests.get(API).json()
    with open("ctftime.json", "w") as f:
        ctftime = convert(scoreboard)
        ctftime_str = dumps(ctftime)
        f.write(ctftime_str)


if __name__ == "__main__":
    main()