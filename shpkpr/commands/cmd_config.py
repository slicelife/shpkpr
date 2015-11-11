# third-party imports
import click

# local imports
from shpkpr import params
from shpkpr.cli import CONTEXT_SETTINGS
from shpkpr.cli import pass_context
from shpkpr.deploy import block_deployment


@click.group('config', short_help='Manage application configuration', context_settings=CONTEXT_SETTINGS)
@pass_context
def cli(ctx):
    """Manage application configuration"""


@cli.command('list', short_help='List application configuration.', context_settings=CONTEXT_SETTINGS)
@params.application
@pass_context
def list(ctx, application):
    """List application configuration."""
    ctx.vlog('Listing application config: %s', application)
    ctx.vlog('============================%s', '=' * len(application))

    # load existing config from marathon if available
    _existing = ctx.marathon_client.get_application(application)
    for k, v in sorted(_existing.env.items()):
        ctx.log("%s=%s", k, v)


@cli.command('set', short_help='Set application configuration.', context_settings=CONTEXT_SETTINGS)
@click.argument('env_vars', nargs=-1)
@params.application
@pass_context
def set(ctx, application, env_vars):
    """Set application configuration."""
    ctx.vlog('Setting application config: %s', application)
    ctx.vlog('============================%s', '=' * len(application))

    # load existing config from marathon if available
    _app = ctx.marathon_client.get_application(application)
    env_vars = dict([(x[0], x[1]) for x in [y.split('=') for y in env_vars]])
    for k, v in env_vars.items():
        _app.env[k] = v

    # redeploy the reconfigured application
    ctx.marathon_client.deploy_application(_app)


@cli.command('unset', short_help='Unset application configuration.', context_settings=CONTEXT_SETTINGS)
@click.argument('keys', nargs=-1)
@params.application
@pass_context
def unset(ctx, application, keys):
    """Unset application configuration."""
    ctx.vlog('Unsetting application config: %s', application)
    ctx.vlog('==============================%s', '=' * len(application))

    # load existing config from marathon if available
    _app = ctx.marathon_client.get_application(application)
    for key in keys:
        try:
            del _app.env[key]
        except KeyError:
            pass

    # redeploy the reconfigured application
    ctx.marathon_client.deploy_application(_app)
