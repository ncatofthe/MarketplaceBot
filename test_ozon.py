from bots.ozon_bot import OzonBot
bot = OzonBot()
print('Connect:', bot.connect())
reviews = bot.get_unanswered_reviews()
print('Found', len(reviews), 'reviews')
if reviews:
    print('First 3:', reviews[:3])
else:
    print('No reviews found')

