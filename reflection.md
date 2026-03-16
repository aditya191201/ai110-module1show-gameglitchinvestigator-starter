# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first opened the game it looked like a normal number guessing game, but almost everything was quietly wrong. The most obvious problem was that the hints were backwards. I guessed 50 when the secret was 38, and the game told me to go higher. I also noticed that before I had even made a single guess, the counter already showed one attempt used. Clicking "New Game" after finishing a round completely froze the game and made it impossible to submit another guess. On top of that, Hard difficulty was actually easier than Normal because it used a smaller number range, and the game would sometimes give you points for guessing incorrectly.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) as my primary AI collaborator throughout this project, working in an interactive chat-driven workflow directly in the terminal alongside my editor.

Correct suggestion: Claude correctly identified that the "Go HIGHER!" and "Go LOWER!" messages in check_guess were swapped. When the guess was greater than the secret the code was telling the player to go higher, which is the wrong direction. Claude suggested swapping the two return strings and I verified it by reading the logic myself. If my guess is bigger than the secret I need to guess lower, so the fix made sense. I also confirmed it by running two pytest cases that both passed after the change.

Incorrect or misleading suggestion: When Claude first applied the Bug 2 fix it only updated the try block and left the same reversed messages sitting in the except TypeError fallback a few lines below. The fix looked complete at first glance but the function still had the wrong strings further down. I caught this by reading through the entire check_guess function after the edit and noticing the fallback branch still said "Go HIGHER!" for a too-high guess. The issue was fully resolved when the logic was moved into logic_utils.py and I made sure both branches were corrected at the same time.

---

## 3. Debugging and testing your fixes

A bug felt fixed only when I could point to a specific line that was wrong, explain why it was wrong, and then show the corrected behavior either in the running app or through a passing test. Eyeballing a change was never enough on its own because the original code had bugs that looked plausible at first glance.

For Bug 1 I opened the app fresh and confirmed the counter showed "Attempts left: 8" before any guess was submitted, which matched the expected behavior after changing the initial value from 1 to 0. For Bug 2 I wrote two pytest cases, test_too_high_message_says_go_lower and test_too_low_message_says_go_higher, that each unpacked the tuple returned by check_guess and checked the message string directly. Before the fix both tests would have failed because the messages were reversed. After the fix all five tests in the file passed, which gave me confidence the logic was correct and not just accidentally working.

Claude helped design the regression tests for Bug 2. I described what the function returned and Claude suggested asserting on the message half of the tuple rather than just the outcome string, which is what the original tests were doing incorrectly. That was useful because it also exposed the pre-existing flaw in the starter tests, where they compared the full tuple to a plain string and silently passed for the wrong reason.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
