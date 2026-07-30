RUBRIC = """
SPECIAL CASE - read this first, and check it carefully.
Look at the CORRECT ANSWER, not at the bot answer.

If the CORRECT ANSWER itself says the information is not in
the document, then a BOT ANSWER that declines is PERFECT.
Score 5 on all three.

If the CORRECT ANSWER contains real facts and the BOT ANSWER
declines anyway, that is a FAILURE - score accuracy 1. The
information existed and the bot did not find it. Do not give
credit for declining when there was an answer to give.

ACCURACY - does it match the CORRECT ANSWER?
  5 = says everything the correct answer says
  3 = leaves out a detail, but nothing the customer
      would act on differently
  1 = contradicts the correct answer, OR adds a fact the
      correct answer does not contain, OR drops a
      CONDITION so the answer is misleading
      (example: "delivery is free" when it is only free
      above 500 rupees)

RELEVANCE - does it answer THIS question?
  5 = answers the question, nothing extra
  3 = answers it, but padded with things nobody asked
  1 = talks about something else

FORMAT - is it a clean sentence you could send to a customer?
  5 = full sentence, correct punctuation, ready to send
  3 = understandable but scrappy
  1 = fragments, labels, slashes, or a raw dump
"""

if __name__ == "__main__":
    print(RUBRIC)