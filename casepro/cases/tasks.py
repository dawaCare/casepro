from __future__ import absolute_import, unicode_literals

from casepro.orgs_ext.tasks import org_task
from celery.utils.log import get_task_logger
from datetime import timedelta
from django.utils import timezone
from djcelery_transactions import task

logger = get_task_logger(__name__)


@org_task('message-pull')
def pull_messages(org, started_on, prev_started_on):
    """
    Pulls new unsolicited messages for an org
    """
    from .models import Message

    # if we're running for the first time, then we'll fetch back to 1 hour ago
    if not prev_started_on:
        prev_started_on = timezone.now() - timedelta(hours=1)

    client = org.get_temba_client(api_version=1)

    num_messages = 0
    num_labelled = 0

    # grab all un-processed unsolicited messages
    pager = client.pager()
    while True:
        messages = client.get_messages(direction='I', _types=['I'], archived=False,
                                       after=prev_started_on, before=started_on, pager=pager)
        num_messages += len(messages)
        num_labelled += Message.process_unsolicited(org, messages)

        if not pager.has_more():
            break

    return {'messages': num_messages, 'labelled': num_labelled}


@task
def message_export(export_id):
    from .models import MessageExport

    export = MessageExport.objects.get(pk=export_id)
    export.do_export()
