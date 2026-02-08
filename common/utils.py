"""Utility functions shared across all pipeline components."""


def check(component_name: str) -> str:
    """
    Check function that can be called from any component.
    
    Args:
        component_name: Name of the component calling this function
        
    Returns:
        A message confirming the check was successful
    """
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message
