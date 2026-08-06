IN_TOK, OUT_TOK = 1150, 20          # per frame, from the receipt
FRAMES_PER_DAY = 6 * 60 * 12        # every 10s, 12h open
PRICES = {"gpt-4o": (2.50, 10.00),
          "claude": (3.00, 15.00),
          "gemini-flash": (0.30, 2.50)}

for name, (p_in, p_out) in PRICES.items():
    per_frame = (IN_TOK * p_in + OUT_TOK * p_out) / 1_000_000
    monthly = per_frame * FRAMES_PER_DAY * 30
    print(f"{name:14} ${per_frame:.5f}/frame  ${monthly:8.2f}/month")