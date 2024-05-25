from typing import Dict
from ..models import Profile
from django.contrib.auth.models import User


def profile_context(request) -> Dict[str, int]:
    if request.user.is_authenticated:
        return {"profile_id": Profile.objects.get(user=request.user).id}
    return {"error": "not logged in"}


def profile_avatar_context(request) -> Dict[str, int]:
    if request.user.is_authenticated:
        return {"profile_avatar": Profile.objects.get(user=request.user).avatar}
    return {"error": "not logged in"}
