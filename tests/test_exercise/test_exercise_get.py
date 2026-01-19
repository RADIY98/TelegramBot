import pytest

from . import exercise

@pytest.mark.parametrize(
    "settings, name, answer",
    [
        ("5: 12,12,12,12", "Первое упражнение", "Упражнение - Первое упражнение\nВес - 5 \nКоличество подходов - 12,12,12,12"),
        ( "5: 12,12,12,12/n 10: 24,24,24,24", "Первое упражнение", "Упражнение - Первое упражнение\nВес - 5 \nКоличество подходов - 12,12,12,12\n\nВес - 10 \nКоличество подходов - 24,24,24,24")
    ]
)
def test_get_exercise_name(settings, name, answer):
    exercise_obj = exercise.Exercise({
        "Settings": settings,
        "Name": name
    })

    assert exercise_obj.get_exercise_str() == answer
