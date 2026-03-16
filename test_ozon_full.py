from bots.ozon_bot import OzonBot
bot = OzonBot()
bot.connect()
reviews = bot.get_unanswered_reviews()
print(f'Found {len(reviews)} unanswered')
if reviews:
    print('Sample:', reviews[0])
bot.process_reviews()
print('Processing complete - check logs for answers sent!')

