# third-party imports
import click

# local imports
from shpkpr.cli import options
from shpkpr.cli.entrypoint import CONTEXT_SETTINGS
from shpkpr.cli.logger import pass_logger
from shpkpr.template import load_values_from_environment
from shpkpr.template import render_json_template


@click.command('deploy', short_help='Deploy application from template.', context_settings=CONTEXT_SETTINGS)
@options.force
@options.template_file
@options.env_prefix
@options.marathon_client
@pass_logger
def cli(logger, marathon_client, env_prefix, template_file, force):
    """Deploy application from template.
    """
    # read and render deploy template using values from the environment
    values = load_values_from_environment(prefix=env_prefix)
    rendered_template = render_json_template(template_file, **values)

    marathon_client.deploy_application(rendered_template, force=force).wait()
