
"""Main application factory for ScriptVoice - Refactored for modularity."""

from interface_factory import create_interface

# Re-export the main interface creation function for backward compatibility
__all__ = ['create_interface']
