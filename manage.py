#!/usr/bin/env python3
import logging
import os
from typing import List

import click
from cassandra.cluster import (Cluster,
                               Session)
from cassandra.cqlengine import connection
from cassandra_helpers.connectable import check_connection
from cassandra_helpers.keyspace import (keyspace_exists,
                                        create_keyspace,
                                        drop_keyspace)
from cassandra_helpers.models import sync_tables

from alcor.config import PROJECT_NAME
from alcor.models import Star
from alcor.models.simulation import Parameter
from alcor.services.data_access import (fetch,
                                        select_statement)
from alcor.services.results_processing import run_processing
from alcor.services.simulations import run_simulations
from alcor.types import RecordType
from alcor.utils import load_settings

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    logging.basicConfig(level=logging.DEBUG)
    contact_points = [os.environ['CASSANDRA_RPC_ADDRESS']]
    port = int(os.environ['CASSANDRA_RPC_PORT'])
    ctx.obj = dict(contact_points=contact_points,
                   port=port)


@main.command()
@click.option('--settings-path', '-p',
              default='settings.yml',
              type=click.Path(),
              help='Settings file path '
                   '(absolute or relative, '
                   'default "settings.yml").')
@click.option('--project-dir', '-d',
              required=True,
              type=click.Path(),
              help='Project directory path '
                   '(absolute or relative).')
@click.option('--clean',
              is_flag=True,
              help='Cleans destination keyspace.')
@click.pass_context
def simulate(ctx: click.Context,
             settings_path: str,
             project_dir: str,
             clean: bool) -> None:
    cluster_settings = ctx.obj
    contact_points = cluster_settings['contact_points']
    port = cluster_settings['port']

    keyspace_name = PROJECT_NAME

    check_connection(contact_points=contact_points,
                     port=port)
    with Cluster(contact_points=contact_points,
                 port=port) as cluster:
        session = cluster.connect()

        if clean:
            clean_keyspace(keyspace_name,
                           session=session)

        init_db(keyspace_name=keyspace_name,
                session=session)

        settings = load_settings(settings_path)
        os.chdir(project_dir)
        run_simulations(settings=settings,
                        session=session)


@main.command()
@click.option('--method', '-m',
              type=click.Choice(['raw',
                                 'full',
                                 'restricted']),
              default='restricted',
              help='Raw data sorting method '
                   '(raw - do nothing, '
                   'full - only declination and parallax selection criteria, '
                   'restricted - apply all criteria)')
@click.option('--nullify-radial-velocity', '-nrf',
              is_flag=True,
              help='Sets radial velocities to zero.')
@click.option('--luminosity-function', '-lf',
              is_flag=True,
              help='Prepare data for plotting luminosity function.')
@click.option('--velocity-clouds', '-uvw',
              is_flag=True,
              help='Prepare data for plotting velocity clouds.')
@click.option('--velocities-vs-magnitude', '-vm',
              is_flag=True,
              help='Prepare data for plots of velocities vs bol. magnitude .')
@click.option('--lepine-criterion', '-lcr',
              is_flag=True,
              help='Apply Lepine\'s criterion.')
@click.pass_context
def process(ctx: click.Context,
            method: str,
            nullify_radial_velocity: bool,
            luminosity_function: bool,
            velocity_clouds: bool,
            velocities_vs_magnitude: bool,
            lepine_criterion: bool) -> None:
    cluster_settings = ctx.obj
    contact_points = cluster_settings['contact_points']
    port = cluster_settings['port']

    keyspace_name = PROJECT_NAME

    check_connection(contact_points=contact_points,
                     port=port)
    with Cluster(contact_points=contact_points,
                 port=port) as cluster:
        session = cluster.connect()
        init_db(keyspace_name=keyspace_name,
                session=session)

        def callback(records: List[RecordType]) -> None:
            logger.debug(f'Starting processing '
                         f'"{Star.__table_name__}" table\'s records, '
                         f'number of records received: {len(records)}.')
            stars = [Star(**raw_star) for raw_star in records]
            run_processing(stars=stars,
                           method=method,
                           nullify_radial_velocity=nullify_radial_velocity,
                           luminosity_function=luminosity_function,
                           velocity_clouds=velocity_clouds,
                           velocities_vs_magnitude=velocities_vs_magnitude,
                           lepine_criterion=lepine_criterion)
            logger.debug(f'Successfully finished processing '
                         f'"{Star.__table_name__}" table\'s records, '
                         f'number of records processed: {len(records)}.')

        table_name = Star.__table_name__
        statement = select_statement(table_name=table_name)
        fetch(statement=statement,
              session=session,
              callback=callback)


def init_db(*,
            keyspace_name: str,
            session: Session) -> None:
    init_keyspace(keyspace_name,
                  session=session)
    session.set_keyspace(keyspace_name)
    connection.set_session(session)
    sync_tables(Parameter, Star)


def init_keyspace(name: str,
                  *,
                  session: Session) -> None:
    logger.info(f'Creating "{name}" keyspace.')
    create_keyspace(name,
                    session=session,
                    check_first=True)


def clean_keyspace(name: str,
                   *,
                   session: Session) -> None:
    if keyspace_exists(name,
                       session=session):
        logger.info(f'Dropping "{name}" keyspace.')
        drop_keyspace(name,
                      session=session)


if __name__ == '__main__':
    main()
