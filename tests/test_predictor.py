from predictor import predict_win_probability, get_model


def test_probability_is_between_zero_and_one():
    model = get_model()
    prediction = predict_win_probability(
        {
            "batting_team": "CSK",
            "bowling_team": "MI",
            "city": "Chennai",
            "current_runs": 125,
            "overs_completed": 12.0,
            "wickets": 2,
            "target_runs": 170,
        },
        model=model,
    )

    assert 0 <= prediction <= 1


def test_different_inputs_change_prediction():
    model = get_model()
    baseline = predict_win_probability(
        {
            "batting_team": "CSK",
            "bowling_team": "MI",
            "city": "Chennai",
            "current_runs": 125,
            "overs_completed": 12.0,
            "wickets": 2,
            "target_runs": 170,
        },
        model=model,
    )
    pressure_case = predict_win_probability(
        {
            "batting_team": "CSK",
            "bowling_team": "MI",
            "city": "Chennai",
            "current_runs": 70,
            "overs_completed": 15.0,
            "wickets": 6,
            "target_runs": 170,
        },
        model=model,
    )

    assert baseline != pressure_case
