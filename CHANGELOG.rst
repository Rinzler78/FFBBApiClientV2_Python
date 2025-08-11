=========
Changelog
=========

Version 0.1.0
==============

**Breaking Changes & Improvements**

- 🏗️ **Major Package Restructure**: Reorganized codebase into logical packages:

  - ``clients/``: API client classes for FFBB services interaction
  - ``models/``: Data models and structures returned by APIs
  - ``helpers/``: Class extensions and utility helpers
  - ``utils/``: Data conversion utilities (renamed from ``converters``)

- 🔧 **Import Path Updates**:

  - Main imports remain unchanged (backward compatible)
  - Internal imports updated to reflect new structure
  - Added comprehensive ``__init__.py`` files for easy access

- 📚 **Enhanced Documentation**:

  - Added architecture documentation explaining new package structure
  - Added comprehensive examples and usage patterns
  - Updated README with package structure information
  - Migration guide for users of internal imports

- ✅ **Improved Maintainability**:

  - Clear separation of concerns between packages
  - Reduced circular dependencies
  - Better code organization following domain-driven design
  - Enhanced testability and modularity

- 🧪 **Testing**: All unit tests updated and passing with new structure

**Migration Notes**

- Public API remains fully backward compatible
- If using internal imports, update to new package structure
- See architecture documentation for detailed migration guide

Version 0.0.1
=============

- Welcome
