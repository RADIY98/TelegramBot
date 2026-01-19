import pytest
from contextlib import nullcontext

from . import exercise

class TestExerciseSplitFunction:
    @pytest.mark.parametrize(
        "settings, answer, expectation",
        [
            ("25: 13", {"25": "13"}, nullcontext()),
            ("25: 12,12,12,12",{"25": "12,12,12,12"}, nullcontext()),
            ("25: 12,12/n35: 15,15", {"25": "12,12", "35": "15,15"}, nullcontext()),
            ("", {}, pytest.raises(Exception))
        ]
    )
    def test_split_settings(self, settings, answer, expectation):
        with expectation:
            assert exercise.Exercise.split_settings(settings) == answer
