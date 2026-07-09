from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-6-6"
)
long_text = """
Dear Valued Partner, We wanted to inform you that starting from next month, 
our supplier will be raising the price of premium cotton bedsheets by 
approximately 8 percent due to increased raw material costs and shipping 
delays affecting the entire textile industry. This adjustment will apply 
to all orders placed after the first of the month. Existing orders and 
contracts already signed will be honored at the previous pricing until 
the end of this quarter. We recommend that hotel partners planning to 
refresh their linen inventory consider placing bulk orders in the coming 
two weeks to lock in the current rates. Please contact your account 
manager for further details or to schedule a call. Thank you for your 
continued business.
"""

summary = summarizer(long_text, max_length=60, min_length=20)

print(summary)