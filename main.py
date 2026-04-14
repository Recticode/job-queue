import typer

app = typer.Typer()

@app.command()
def enqueue():
    print("not ready yet")

@app.command()
def dequeue():
    print("not ready yet")

if __name__ == "__main__":
    app()