"""pyGtoP custom exceptions."""

class NoSuchLigandError(Exception):
    """The exception raised if a specific ligand is requested which does not
    exist."""
    pass



class NoSuchTargetError(Exception):
    """The exception raised if a specific target is requested which does not
    exist."""
    pass



class NoSuchTargetFamilyError(Exception):
    """The exception raised if a specific target family is requested which does not
    exist."""
    pass



class NoSuchInteractionError(Exception):
    """The exception raised if a specific interaction is requested which does not
    exist."""
    pass



class NoSuchTypeError(Exception):
    """The exception raised if a random ligand or target is requested of a type
    which does not exist."""
    pass
