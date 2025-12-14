#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "click",
#   "dycw-utilities",
#   "pytest-xdist",
#   "typed-settings[attrs, click]",
# ]
# ///
from __future__ import annotations

from logging import getLogger
from subprocess import check_call, check_output

from click import command
from typed_settings import click_options, option, settings
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config
from utilities.version import parse_version

_LOGGER = getLogger(__name__)


@settings
class Settings:
    dry_run: bool = option(default=False, help="Dry run the CLI")


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@click_options(Settings, "app", show_envvars_in_help=True)
def main(settings: Settings, /) -> None:
    if settings.dry_run:
        _LOGGER.info("Dry run; exiting...")
        return
    cmds1 = ["bump-my-version", "show", "current_version"]
    _LOGGER.info("Running '%s'...", " ".join(cmds1))
    version = parse_version(check_output(cmds1, text=True).rstrip("\n"))
    _LOGGER.info("Current version is %s", version)
    cmds2 = ["git", "tag", "-a", str(version), "HEAD", "-m", str(version)]
    _LOGGER.info("Running '%s'...", " ".join(cmds2))
    _ = check_call(cmds2)
    cmds3 = ["git", "push", "--tags", "--force", "--set-upstream", "origin"]
    _LOGGER.info("Running '%s'...", " ".join(cmds3))
    _ = check_call(cmds3)
    _LOGGER.info("Finished")


if __name__ == "__main__":
    basic_config(obj=__name__)
    main()
