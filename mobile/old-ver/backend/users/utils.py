from .models import Memory


def get_user_memory(user):
    """Get all memory records for a user"""
    memories = Memory.objects.filter(user=user).values_list("content", flat=True)
    return list(memories)