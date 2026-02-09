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
    caller_frame = None
    try:
        # Get the caller's frame (one level up)
        caller_frame = frame.f_back
        
        # Check if there is a caller frame
        if caller_frame is None:
            print("Called from module: Unknown")
            return "Unknown"
        
        # Get the module name from the caller's globals
        module = caller_frame.f_globals.get('__name__', 'Unknown')
        
        print(f"Called from module: {module}")
        return module
    finally:
        # Clean up frame references to avoid reference cycles
        if caller_frame is not None:
            del caller_frame
        del frame
