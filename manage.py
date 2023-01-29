#!/usr/bin/env python

import typer
import uvicorn  # type: ignore


manager = typer.Typer()


@manager.command()
def runserver(reload: bool = True):
    uvicorn.run("project.app:app", host="0.0.0.0", port=8080, reload=reload)


if __name__ == "__main__":
    manager()
