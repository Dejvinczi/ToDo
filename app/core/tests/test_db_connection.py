"""
Tests for application database connection.
"""
import pytest
from django.db import connection


@pytest.mark.django_db
def test_db_connection():
    """Test database connection."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

    assert result == (1,)
