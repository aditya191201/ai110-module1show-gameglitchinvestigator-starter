from logic_utils import check_guess

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
