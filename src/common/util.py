"""Utility functions for KFP components."""
import inspect


def print_module_name():
    """
    Print the name of the calling module.
    
    This function inspects the call stack to determine which module
    called it and prints that module's name.
    """
    # Get the frame of the caller
    frame = inspect.currentframe()
    try:
        # Get the caller's frame (one level up)
        caller_frame = frame.f_back
        
        # Get the module name from the caller's globals
        module = caller_frame.f_globals.get('__name__', 'Unknown')
        
        print(f"Called from module: {module}")
        return module
    finally:
        # Clean up frame references to avoid reference cycles
        del frame
