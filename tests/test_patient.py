"""Tests for the Patient model."""

import pytest
from inflammation.models import Patient

@pytest.mark.skip(reason="Patient model not implemented yet")
def test_create_patient():
    """Test that we can create a patient with a name."""

    name = "Alice"
    p = Patient(name=name)

    assert p.name == name
