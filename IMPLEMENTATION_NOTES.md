# Multi-Cryptocurrency Middleman Bot Implementation Notes

## Overview
This document outlines the major changes made to support multiple cryptocurrencies (Litecoin, Solana, and USDT Polygon) in the Discord Middleman Bot.

## Key Changes

### 1. Main Embed Redesign
- **File:** `commands/MmEmbed.py`
- Updated embed title to "Rainy MM & Exch"
- Added professional description explaining the escrow service
- Changed button label to "Select The Cryptocurrency"

### 2. Cryptocurrency Selection System
- **New File:** `view/cryptoSelectModal.py`
- Created a new view with three buttons:
  - Litecoin (LTC)
  - Solana (SOL)
  - USDT Polygon (USDT)
- Each button opens the registration modal with the selected cryptocurrency

### 3. Updated Registration Flow
- **File:** `view/startModal.py`
- Added `crypto_type` parameter to track selected cryptocurrency
- Updated ticket channel naming to include crypto type (e.g., `username-mm-ltc`)
- Store crypto_type in process JSON files
- Display cryptocurrency type in embeds and logs

### 4. Multi-Crypto Wallet Functions
- **File:** `function.py`
- Updated `create_wallet()` to accept crypto_type parameter
- Updated `check_transactions()` to handle different blockchain APIs
- Updated `send_to_address()` for multi-crypto support
- Renamed `convertToLtc()` to `convertToFiat()` with support for all three cryptos

### 5. Updated Transaction Flow
- **File:** `view/confirmRoles.py`
- Reads crypto_type from process file
- Creates wallet based on selected cryptocurrency
- Displays cryptocurrency-specific information in all embeds
- Converts amounts correctly based on crypto type (different decimal places)

### 6. Updated Modals and Buttons
All modals and buttons now support crypto_type:
- `view/confirmDeal.py` - Pass crypto_type to wallet modal
- `view/refundButton.py` - Pass crypto_type to refund modal
- `view/walletModal.py` - Show crypto-specific placeholders and labels
- `view/refundModal.py` - Handle crypto-specific refunds

### 7. Developer Release Command
- **New File:** `commands/releaseCommand.py`
- Developer-only command to manually release stuck funds
- Requires developer role to be configured
- Logs all release actions
- Usage: `/release ticket_uid private_key recipient_address`

### 8. Developer Role Setup
- **New File:** `commands/setDevRole.py`
- Command to configure developer role: `/setup-developer-role @role`
- Only the buyer (owner) can set this role

### 9. Configuration Updates
- **File:** `config.json`
- Added `developer_role_id` field
- Added `solana_api_key` field (for future Solana implementation)
- Added `polygon_api_key` field (for future USDT Polygon implementation)

### 10. Process File Structure
- **File:** `process/exemple.json`
- Added `crypto_type` field to track cryptocurrency for each ticket

## Important Notes

### Current Implementation Status
1. **Litecoin (LTC)** - Fully implemented using BlockCypher API
2. **Solana (SOL)** - Placeholder functions return errors (API integration needed)
3. **USDT Polygon** - Placeholder functions return errors (API integration needed)

### Required API Integrations (To Be Completed)

#### For Solana Support:
- Implement wallet generation using Solana Web3.js or similar
- Implement transaction monitoring
- Implement fund transfers
- Add Solana API key to config
- Update conversion rates

#### For USDT Polygon Support:
- Implement wallet generation for Polygon network
- Implement USDT token transaction monitoring
- Implement USDT token transfers
- Add Polygon API key to config
- Update conversion rates

### Configuration Required

1. **Bot Token:** Set in `config.json`
2. **Buyer ID:** Your Discord user ID in `config.json`
3. **BlockCypher API:** For Litecoin transactions
4. **Developer Role:** Use `/setup-developer-role` command
5. **Ticket Category:** Use `/setup-category` command
6. **Logs Channel:** Use `/setup-logs` command (optional)
7. **Color & Footer:** Customize in `config.json`

### Security Considerations

1. **Private Keys:** Never share or log private keys
2. **Developer Role:** Only trusted developers should have this role
3. **Release Command:** Logged for audit purposes
4. **Wallet Security:** Wallets are generated per transaction
5. **API Keys:** Store securely in config.json (add to .gitignore)

### Future Enhancements

1. Complete Solana integration
2. Complete USDT Polygon integration
3. Add support for additional cryptocurrencies
4. Implement transaction fee handling
5. Add refund timeout mechanism
6. Implement dispute resolution system
7. Add transaction history tracking
8. Create admin dashboard for monitoring

## Commands Reference

### User Commands
- `/help` - Show all available commands
- `/ping` - Test bot responsiveness

### Admin Commands (Whitelist/Buyer)
- `/middleman-embed` - Send the main panel
- `/setup-category` - Set ticket category
- `/setup-logs` - Enable logging
- `/disable-logs` - Disable logging
- `/whitelist-add` - Add user to whitelist
- `/whitelist-remove` - Remove user from whitelist
- `/whitelist-list` - Show whitelisted users
- `/change-api-key` - Update BlockCypher API key

### Buyer Only Commands
- `/setup-developer-role` - Set developer role

### Developer Commands (Requires Developer Role)
- `/release` - Manually release stuck funds

## Testing Checklist

- [ ] Test LTC wallet creation
- [ ] Test LTC transaction monitoring
- [ ] Test LTC fund transfer
- [ ] Test cryptocurrency selection UI
- [ ] Test ticket creation with each crypto
- [ ] Test role confirmation flow
- [ ] Test deal confirmation
- [ ] Test refund process
- [ ] Test developer release command
- [ ] Test permission checks
- [ ] Test logging system
- [ ] Verify SOL placeholder functions
- [ ] Verify USDT placeholder functions

## Deployment Notes

1. Install all required dependencies from `requirements.txt`
2. Configure `config.json` with your values
3. Set up developer role using `/setup-developer-role`
4. Set up ticket category using `/setup-category`
5. Optionally enable logs using `/setup-logs`
6. Send the middleman panel using `/middleman-embed`
7. Add API keys for Solana and Polygon when implementing those features

## Support

For issues or questions about this implementation, please refer to the original developer (scarlxrd1337) or check the repository documentation.
