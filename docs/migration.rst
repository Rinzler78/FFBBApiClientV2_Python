=========
Migration
=========

This guide helps you migrate from the old package structure to the new organized structure introduced in version 0.1.0.

Public API Migration (No Changes Required)
===========================================

**Good News**: If you were using the public API, **no changes are required**!

The following imports continue to work exactly as before:

.. code-block:: python

    # These imports are unchanged and fully supported
    from ffbb_api_client_v2 import FFBBAPIClientV2, ApiFFBBAppClient
    from ffbb_api_client_v2 import MeilisearchClient, MeilisearchFFBBClient
    from ffbb_api_client_v2 import MultiSearchQuery, Live
    from ffbb_api_client_v2 import MeilisearchClientExtension
    from ffbb_api_client_v2 import generate_queries

Your existing code should work without any modifications!

Internal Imports Migration
===========================

If you were importing directly from internal modules, you'll need to update your imports.

Client Imports
--------------

**Before (v0.0.x):**

.. code-block:: python

    from ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient
    from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
    from ffbb_api_client_v2.meilisearch_ffbb_client import MeilisearchFFBBClient
    from ffbb_api_client_v2.ffbb_api_client_v2 import FFBBAPIClientV2

**After (v0.1.0+):**

.. code-block:: python

    # Option 1: Use public API (recommended)
    from ffbb_api_client_v2 import ApiFFBBAppClient, MeilisearchClient
    from ffbb_api_client_v2 import MeilisearchFFBBClient, FFBBAPIClientV2

    # Option 2: Use new package structure
    from ffbb_api_client_v2.clients import ApiFFBBAppClient, MeilisearchClient
    from ffbb_api_client_v2.clients import MeilisearchFFBBClient, FFBBAPIClientV2

Helper Imports
--------------

**Before (v0.0.x):**

.. code-block:: python

    from ffbb_api_client_v2.meilisearch_client_extension import MeilisearchClientExtension
    from ffbb_api_client_v2.http_requests_helper import catch_result, default_cached_session
    from ffbb_api_client_v2.http_requests_utils import http_get_json, http_post_json
    from ffbb_api_client_v2.multi_search_query_helper import generate_queries

**After (v0.1.0+):**

.. code-block:: python

    # Option 1: Use public API (recommended)
    from ffbb_api_client_v2 import MeilisearchClientExtension, generate_queries

    # Option 2: Use new package structure
    from ffbb_api_client_v2.helpers import MeilisearchClientExtension
    from ffbb_api_client_v2.helpers import catch_result, default_cached_session
    from ffbb_api_client_v2.helpers import http_get_json, http_post_json
    from ffbb_api_client_v2.helpers import generate_queries

Model Imports
-------------

**Before (v0.0.x):**

.. code-block:: python

    from ffbb_api_client_v2.lives import Live, lives_from_dict
    from ffbb_api_client_v2.external_id import ExternalID
    from ffbb_api_client_v2.multi_search_query import MultiSearchQuery
    from ffbb_api_client_v2.MultiSearchResults import MultiSearchResults

**After (v0.1.0+):**

.. code-block:: python

    # Option 1: Use public API (recommended)
    from ffbb_api_client_v2 import Live, ExternalID, MultiSearchQuery, MultiSearchResults

    # Option 2: Use new package structure
    from ffbb_api_client_v2.models import Live, lives_from_dict
    from ffbb_api_client_v2.models import ExternalID, MultiSearchQuery
    from ffbb_api_client_v2.models import MultiSearchResults

Utility Imports
---------------

**Before (v0.0.x):**

.. code-block:: python

    from ffbb_api_client_v2.converters import from_datetime, from_str, from_int

**After (v0.1.0+):**

.. code-block:: python

    # Note: 'converters' renamed to 'converter_utils'
    from ffbb_api_client_v2.utils.converter_utils import from_datetime, from_str, from_int

Migration Steps
===============

1. **Update Import Statements**

   Replace old internal imports with public API imports where possible:

   .. code-block:: python

       # Before
       from ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient

       # After
       from ffbb_api_client_v2 import ApiFFBBAppClient

2. **Update Converter Imports**

   The ``converters`` module was renamed to ``converter_utils``:

   .. code-block:: python

       # Before
       from ffbb_api_client_v2.converters import from_datetime

       # After
       from ffbb_api_client_v2.utils.converter_utils import from_datetime

3. **Test Your Changes**

   Run your tests to ensure everything works correctly:

   .. code-block:: bash

       python -m pytest your_tests/

Common Migration Issues
=======================

Issue: Import Not Found
-----------------------

**Error:**
``ModuleNotFoundError: No module named 'ffbb_api_client_v2.converters'``

**Solution:**
Update to use the new path:

.. code-block:: python

    # Replace this
    from ffbb_api_client_v2.converters import from_datetime

    # With this
    from ffbb_api_client_v2.utils.converter_utils import from_datetime

Issue: Class Not Found in Module
---------------------------------

**Error:**
``ImportError: cannot import name 'SomeClass' from 'ffbb_api_client_v2.some_module'``

**Solution:**
Use the public API instead:

.. code-block:: python

    # Replace this
    from ffbb_api_client_v2.some_module import SomeClass

    # With this
    from ffbb_api_client_v2 import SomeClass

Migration Script
================

Here's a Python script to help identify imports that need updating:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Script to find imports that need migration
    """
    import os
    import re

    def find_old_imports(directory):
        """Find old import patterns in Python files"""
        old_patterns = [
            r'from ffbb_api_client_v2\.converters import',
            r'from ffbb_api_client_v2\.[a-z_]+_client import',
            r'from ffbb_api_client_v2\.http_requests_',
            r'from ffbb_api_client_v2\.multi_search_query_helper import',
        ]

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        content = f.read()
                        for i, line in enumerate(content.splitlines(), 1):
                            for pattern in old_patterns:
                                if re.search(pattern, line):
                                    print(f"{filepath}:{i}: {line.strip()}")

    if __name__ == "__main__":
        find_old_imports(".")

Benefits of Migration
====================

Migrating to the new package structure provides:

- **Better Code Organization**: Logical separation of clients, models, and utilities
- **Improved Maintainability**: Clearer dependencies and relationships
- **Enhanced Development**: Better IDE support and code navigation
- **Future-Proof**: Foundation for future enhancements and extensions

Need Help?
==========

If you encounter issues during migration:

1. Check that you're using the latest version (0.1.0+)
2. Review the architecture documentation
3. Look at the examples for usage patterns
4. Check the test files for reference implementations

The public API remains stable, so most applications should require minimal changes.
