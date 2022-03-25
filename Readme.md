# Discord SelfBot
Example - print all messages in console:
    
	from discord_selfbot import SelfBot
    
    bot = SelfBot("YourToken")
    
    
    def test_handler(message):
        print(f"{message.guild.name}: {message.channel.name}\n{message.author}\n{message.content}")
    
    
    bot.add_message_handler(test_handler)
    
    if __name__ == '__main__':
        bot.run()