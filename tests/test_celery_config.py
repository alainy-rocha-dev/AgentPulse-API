import pytest
from app.core.celery_app import celery_app

def test_celery_config_resilience():
    assert celery_app.conf.task_acks_late is True
    assert celery_app.conf.task_time_limit == 300
    assert celery_app.conf.task_serializer == "json"
