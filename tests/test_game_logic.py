from logic_utils import check_guess, update_score, get_range_for_difficulty, parse_guess

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug 2 regression: hint messages were swapped
def test_too_high_message_says_go_lower():
    _, message = check_guess(80, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message for too-high guess, got: {message}"

def test_too_low_message_says_go_higher():
    _, message = check_guess(20, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in message for too-low guess, got: {message}"

# Bug 3 regression: secret was cast to string on even attempts causing alphabetical comparison
def test_check_guess_numeric_not_string_comparison():
    # 9 > "38" alphabetically but 9 < 38 numerically — must treat secret as int
    outcome, _ = check_guess(9, 38)
    assert outcome == "Too Low", "Numeric comparison failed: 9 should be less than 38"

# Bug 5 regression: Hard range was 1-50, smaller than Normal (1-100)
def test_hard_range_larger_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) > (normal_high - normal_low), "Hard range should be wider than Normal"

# Bug 7 regression: too-high guesses on even attempts were adding points instead of subtracting
def test_wrong_guess_never_adds_points():
    score_after_too_high = update_score(100, "Too High", 2)  # attempt 2 = even, was the buggy case
    assert score_after_too_high < 100, "A wrong guess should never increase the score"

def test_wrong_guess_subtracts_points():
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too Low", 3) == 95

# Edge case 1: negative numbers are parsed as valid integers but fall outside the game range
def test_negative_number_parses_successfully():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5  # documents that no range guard exists in parse_guess

def test_negative_number_is_too_low():
    outcome, _ = check_guess(-5, 50)
    assert outcome == "Too Low", "A negative guess should always be Too Low for any positive secret"

# Edge case 2: extremely large numbers are accepted and compared numerically
def test_extremely_large_number_parses_successfully():
    ok, value, err = parse_guess("999999")
    assert ok is True
    assert value == 999999  # documents that no upper bound guard exists

def test_extremely_large_number_is_too_high():
    outcome, _ = check_guess(999999, 50)
    assert outcome == "Too High", "An enormous guess should always be Too High"

# Edge case 3: decimals are silently truncated toward zero, not rounded
def test_decimal_truncates_down():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7, "7.9 should truncate to 7, not round to 8"

def test_decimal_truncates_negative():
    ok, value, err = parse_guess("-2.9")
    assert ok is True
    assert value == -2, "-2.9 should truncate to -2 via int(float()), not -3"
