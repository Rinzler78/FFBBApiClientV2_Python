# FFBB API Client V2 - Examples

This directory contains practical examples demonstrating how to use the FFBB API Client V2.

## Files

### `quick_start.py`
Basic usage example showing the most common operations:
- Searching for basketball clubs
- Getting detailed organization information
- Checking live matches
- Retrieving current seasons

**Run it:**
```bash
python examples/quick_start.py
```

### `complete_usage_example.py`
Comprehensive example demonstrating all major features:
- Type-safe model objects
- Field selection (BASIC, DEFAULT, DETAILED)
- Error handling
- Multi-search functionality
- Competition details
- Advanced API usage patterns

**Run it:**
```bash
python examples/complete_usage_example.py
```

## Prerequisites

1. **Install the package:**
   ```bash
   pip install ffbb_api_client_v2
   ```

2. **Set up your environment:**
   Create a `.env` file in the project root:
   ```bash
   API_FFBB_APP_BEARER_TOKEN=your_ffbb_api_token_here
   MEILISEARCH_BEARER_TOKEN=your_meilisearch_token_here
   ```

3. **Install python-dotenv** (if not already installed):
   ```bash
   pip install python-dotenv
   ```

## Key Features Demonstrated

- **🏀 Complete API Coverage**: Access to all FFBB services
- **🔧 Type-Safe Models**: Strongly-typed response objects
- **⚡ Field Selection**: Optimize queries with custom field sets
- **🔍 Multi-Search**: Search across all resource types
- **🛡️ Error Handling**: Robust error handling patterns
- **📊 Real Data**: Examples work with real FFBB API data

## What You'll Learn

- How to initialize the FFBB API Client V2
- Working with model-based responses instead of raw dictionaries
- Using field selection for performance optimization
- Handling API errors gracefully
- Searching across different resource types
- Getting detailed information about clubs, competitions, and seasons

## Next Steps

After running these examples, check out:
- The comprehensive test suite in `tests/` for more usage patterns
- The main documentation in `README.rst`
- The API reference documentation

## Support

If you encounter any issues:
1. Check your API tokens are correctly set in the `.env` file
2. Ensure you have a stable internet connection
3. Review the error messages - the client provides detailed error information
4. Check the test files for additional usage examples
