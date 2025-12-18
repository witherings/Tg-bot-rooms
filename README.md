# Brawl Stars Private Code Generator Bot

## What is this bot?

A Telegram bot that generates unique Brawl Stars team invitation codes with customizable offsets. Share private team invitations with your friends easily!

## Features

- 🎮 Generate 10 unique team codes at once
- 🔗 Get direct Brawl Stars invitation links
- 📊 Customizable offset values (5, 10, 20, 50, 100 or custom)
- 💾 Support for direct codes and invitation links
- 📝 All activity logged to PostgreSQL database
- ✅ Channel subscription verification

## How to use

1. **Send a code**: Send your team code (e.g., `XWADUQNY`) or an invitation link to the bot
2. **Choose offset**: Use `/offset` to select how many positions to shift, or use the default (+50)
3. **Get invitations**: Receive 10 new unique codes with direct Brawl Stars invitation links
4. **Copy & share**: Click the link or copy the code and send to your friends!

## Commands

- `/start` - Start using the bot
- `/generate` - Generate new codes
- `/offset` - Change the offset value
- `/help` - Show help information
- `/cancel` - Cancel current operation

## What is an offset?

The offset determines how many positions to shift from the original code. For example:
- Original code: `XWADUQNY` (ID: 12345)
- Offset +50: New codes start from ID 12395

This lets you generate different codes from the same base!

## Requirements

- Channel subscription (or temporary access)
- Valid Brawl Stars team code
- Internet connection

## Privacy

- All generated codes are unique and private to your team
- User data is stored only for logging purposes
- No data is shared with third parties

## Support

For help or issues, contact: @neighty_bs channel

---

**Made with ❤️ for Brawl Stars players**
