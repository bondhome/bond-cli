from bond import app
from bond.cli.console import console_terminate

if __name__ == "__main__":
    try:
        app.run()
    finally:
        console_terminate()
