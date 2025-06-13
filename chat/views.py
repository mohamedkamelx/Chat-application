from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import UserProfile, Friends, Messages
from chat.serializers import MessageSerializer


def get_friends_list(user_id):
    """
    Get the list of friends for a user by ID.
    """
    try:
        user = UserProfile.objects.get(id=user_id)
        friend_relations = user.friends_set.all()
        friends = [UserProfile.objects.get(id=relation.friend) for relation in friend_relations]
        return friends
    except UserProfile.DoesNotExist:
        return []


def get_user_id(username):
    """
    Retrieve the user ID by username.
    """
    user = get_object_or_404(UserProfile, username=username)
    return user.id


def index(request):
    """
    Display the home page with user's friends if authenticated.
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html")

    user_id = get_user_id(request.user.username)
    friends = get_friends_list(user_id)
    return render(request, "chat/Base.html", {'friends': friends})


def search(request):
    """
    Search for users, excluding the current user.
    """
    current_user = request.user
    users = list(UserProfile.objects.exclude(username=current_user.username))

    if request.method == "POST":
        query = request.POST.get("search", "")
        matched_users = [user for user in users if query in user.name or query in user.username]
        return render(request, "chat/search.html", {'users': matched_users})

    displayed_users = users[:10] if len(users) > 10 else users
    user_id = get_user_id(current_user.username)
    friends = get_friends_list(user_id)
    return render(request, "chat/search.html", {'users': displayed_users, 'friends': friends})


def add_friend(request, name):
    """
    Add a user to the current user's friend list.
    """
    current_user = request.user
    current_user_id = get_user_id(current_user.username)
    curr_user = get_object_or_404(UserProfile, id=current_user_id)
    friend_user = get_object_or_404(UserProfile, username=name)

    already_friends = curr_user.friends_set.filter(friend=friend_user.id).exists()

    if not already_friends:
        print("Friend Added!")
        curr_user.friends_set.create(friend=friend_user.id)
        friend_user.friends_set.create(friend=current_user_id)

    return redirect("/search")


def chat_view(request, username):
    """
    Render chat page between current user and selected friend.
    """
    friend_user = get_object_or_404(UserProfile, username=username)
    current_user_id = get_user_id(request.user.username)
    current_user = get_object_or_404(UserProfile, id=current_user_id)

    messages = Messages.objects.filter(
        sender_name=current_user_id, receiver_name=friend_user.id
    ) | Messages.objects.filter(
        sender_name=friend_user.id, receiver_name=current_user_id
    )

    if request.method == "GET":
        friends = get_friends_list(current_user_id)
        return render(
            request, "chat/messages.html",
            {
                'messages': messages.order_by('timestamp'),
                'friends': friends,
                'curr_user': current_user,
                'friend': friend_user
            }
        )


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    GET: Fetch unseen messages from sender to receiver and mark as seen.
    POST: Send a new message.
    """
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})

        # Mark messages as seen
        messages.update(seen=True)

        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
