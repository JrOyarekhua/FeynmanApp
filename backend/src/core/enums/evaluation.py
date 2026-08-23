from enum import Enum

class ConfidenceLevel(str, Enum):
    needs_improvement = 'needs_improvement'
    average = 'average'
    excellent = 'excellent'