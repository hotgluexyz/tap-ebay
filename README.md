# tap-ebay

A Singer tap for extracting data from the eBay API.

Built with the [Hotglue Tap SDK](https://github.com/hotgluexyz/HotglueTapSDK) for Singer Taps.

## Features

- Extracts order data from eBay Fulfillment API
- OAuth 2.0 authentication with automatic token refresh
- Incremental sync support using `lastModifiedDate`
- Comprehensive schema coverage for eBay orders

## Installation

### Using Poetry (Recommended)

```bash
poetry install
```

### Using pip

```bash
pip install -e .
```

## Configuration

### Required Configuration

The tap requires the following configuration parameters:

- `refresh_token` - OAuth refresh token for eBay API
- `client_id` - eBay application client ID
- `client_secret` - eBay application client secret

### Configuration File

Create a `config.json` file with your credentials:

```json
{
  "refresh_token": "your_refresh_token",
  "client_id": "your_client_id",
  "client_secret": "your_client_secret"
}
```

### Authentication Setup

To obtain OAuth credentials for eBay:

1. Register your application at [eBay Developers Program](https://developer.ebay.com/)
2. Create an application and obtain your client ID and client secret
3. Generate a refresh token using the OAuth flow
4. Add these credentials to your configuration file

## Usage

### Discovery Mode

To discover available streams and their schemas:

```bash
tap-ebay --config config.json --discover > catalog.json
```

### Sync Mode

To extract data:

```bash
tap-ebay --config config.json --catalog catalog.json
```

### With State File

To perform incremental syncs:

```bash
tap-ebay --config config.json --catalog catalog.json --state state.json
```

### Check Version

```bash
tap-ebay --version
```

### Get Help

```bash
tap-ebay --help
```

## Available Streams

### Orders Stream

Extracts order data from the eBay Fulfillment API.

**Endpoint:** `/sell/fulfillment/v1/order`

**Primary Key:** `orderId`

**Replication Key:** `lastModifiedDate`

## Development

### Setup Development Environment

```bash
# Install poetry if you haven't already
pip install poetry

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Run Tests

```bash
poetry run pytest
```

### Code Quality

The project uses the following tools for code quality:

```bash
# Format code
poetry run black tap_ebay

# Sort imports
poetry run isort tap_ebay

# Lint code
poetry run flake8 tap_ebay

# Type checking
poetry run mypy tap_ebay
```

### Run Linting Suite

```bash
poetry run tox
```

## API Documentation

For more information about the eBay API:

- [eBay Fulfillment API Documentation](https://developer.ebay.com/api-docs/sell/fulfillment/overview.html)
- [eBay OAuth Documentation](https://developer.ebay.com/api-docs/static/oauth-tokens.html)

## Singer Specification

This tap follows the [Singer specification](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md) for data extraction.

## License

Apache 2.0

## Support

For issues and questions, please open an issue in the repository.
