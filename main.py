import typer
import requests
import urllib.parse
import os
from rich import print

app = typer.Typer()

URL = os.environ.get("API_URL") or "https://scamonator.onrender.com/"

@app.command()
def submit(user_email: str, report_email: str):
    """
    Submit a user to scamonator
    """
    response = requests.post(URL+"submit/", json={"report_email": report_email, "user_email": user_email})
    match response.status_code:
        case 404:
            print("[red]404 not found[/red]")
        case 422:
            print("[red]Json not valid - Internal Error[/red]")
        case 400:
            print("[red]Not a valid email address![/red]")
        case 200:
            print("[green]Submitted![/green]")
        case _:
            print("[purple]Unknown error[/purple]")
    
@app.command()
def check(email: str):
    """
    Check a user against scamonator
    """
    email = urllib.parse.quote(email)
    response = requests.get(URL+"emails/{}/".format(urllib.parse.quote(email)))
    try:
        num_reports = response.json()
    except requests.JSONDecodeError:
        print("Received Invalid Json!")
        raise typer.Exit(1)
    except TypeError:
        print("Error converting to integer!")
        raise typer.Exit(1)
    if num_reports == 1:
        print("[yellow]1 user reported this email as a scam![/yellow]")
    elif num_reports == 0:
        print("[green]0 users reported this email as a scam![/green]")
    else:
        print("[orange]{} users reported this email as a scam![/orange]".format(num_reports))
    
    
if __name__ == "__main__":
    app()
