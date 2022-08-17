"A collections of functions that reply to errors."
import logging
import httpx
from discord.ext import commands
from api import safebooru


def read_timeout(_: commands.Context, error: httpx.ReadTimeout):
    "This gets triggered if the bot gets a read timout."
    logging.warning("Bot got a timeout from %s", error.request.url)


def missing_permissions(is_bot: bool):
    "This gets triggered when bot or client doesn't have correct permissions."
    def inner(
        ctx: commands.Context,
        error: commands.BotMissingPermissions or commands.MissingPermissions
        ):
        if not ctx.guild:
            ctx.send("This command has to be called inside of a guild!")
            return
        if is_bot:
            ctx.send(
                "I do not have the right permissions to execute this command.\n"
                f"Permissions that are missing: ({', '.join(error.missing_perms)})"
            )
        else:
            ctx.send(
                "You are missing permissions to run this command.\n"
                f"Permissions that are missing: ({', '.join(error.missing_perms)})"
            )

    return inner


def safebooru_connection_error(ctx: commands.Context, _: safebooru.SafebooruConnectionError):
    "This is triggered when the connection to safebooru fails."
    ctx.send("Something went wrong with the safebooru.org api.")


def safebooru_nothing_found(ctx: commands.Context, error: safebooru.SafebooruNothingFound):
    "This is triggerd if nothing is found on safebooru query."
    ctx.send(
        f"Couldn't find something for given tags. ({', '.join(list(error.tags))})")


def missing_required_argument(ctx: commands.Context, _: commands.MissingRequiredArgument):
    "This is triggerd if the invoker didn't give all the necessary arguments."
    ctx.send_help(ctx.command)


error_dictionary = {
    commands.MissingPermissions: missing_permissions(False),
    commands.BotMissingPermissions: missing_permissions(True),
    safebooru.SafebooruConnectionError: safebooru_connection_error,
    safebooru.SafebooruNothingFound: safebooru_nothing_found,
    commands.MissingRequiredArgument: missing_required_argument
}
