from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
from django.http.multipartparser import MultiPartParser
import json
from .forms import CustomUserCreationForm
from .serializers import (
    serialize_user,
    serialize_item,
    serialize_bid,
    serialize_question,
)
from .utils import json_response
from .models import User, Item, Bid, Question


@require_http_methods(["POST"])
def api_signup(request: HttpRequest) -> JsonResponse:
    """
    User registration endpoint.

    Accepts:
        - username: str
        - email: str
        - password1: str
        - password2: str
        - date_of_birth: str (optional, YYYY-MM-DD format)
        - profile_image: File (optional)

    Returns:
        Success: {success: true, data: {user: UserDict}}
        Error: {success: false, errors: {field: [errors]}}
    """
    form = CustomUserCreationForm(request.POST, request.FILES)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return json_response(data={"user": serialize_user(user)}, status=201)
    else:
        # Convert form errors to dictionary format
        errors: dict[str, list[str]] = {
            field: [str(error) for error in error_list]
            for field, error_list in form.errors.items()
        }
        return json_response(errors=errors, status=400)


@require_http_methods(["POST"])
def api_login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint.

    Accepts:
        - username: str
        - password: str

    Returns:
        Success: {success: true, data: {user: UserDict}}
        Error: {success: false, error: str}
    """
    import json

    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "")
    except (json.JSONDecodeError, AttributeError):
        return json_response(error="Invalid request data", status=400)

    if not username or not password:
        return json_response(error="Username and password are required", status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return json_response(data={"user": serialize_user(user)})
    else:
        return json_response(error="Invalid credentials", status=401)


@require_http_methods(["POST"])
@login_required
def api_logout(request: HttpRequest) -> JsonResponse:
    """
    User logout endpoint.

    Returns:
        {success: true}
    """
    logout(request)
    return json_response(data={})


@ensure_csrf_cookie
@require_http_methods(["GET"])
def api_get_user(request: HttpRequest) -> JsonResponse:
    """
    Get current authenticated user.
    Also sets the CSRF cookie for subsequent requests.

    Returns:
        Success: {success: true, data: {user: UserDict}}
        Error: {success: false, error: str}
    """
    if not request.user.is_authenticated:
        return json_response(error="Not authenticated", status=401)

    return json_response(data={"user": serialize_user(request.user)})


@ensure_csrf_cookie
@require_http_methods(["GET"])
def api_csrf(request: HttpRequest) -> JsonResponse:
    """
    Endpoint to get CSRF cookie.
    Call this before making POST/PUT requests if CSRF cookie is not set.

    Returns:
        {success: true}
    """
    return json_response(data={})


@require_http_methods(["PUT"])
@login_required
def api_update_profile(request: HttpRequest) -> JsonResponse:
    """
    Update user profile endpoint using PUT.
    Manually parses multipart data since Django doesn't populate request.POST for PUT.

    Accepts:
        - email: str
        - date_of_birth: str (optional, YYYY-MM-DD format)
        - profile_image: File (optional)

    Returns:
        Success: {success: true, data: {user: UserDict}}
        Error: {success: false, errors: {field: [errors]}}
    """
    user = request.user

    # Handle multipart/form-data manually for PUT requests
    if request.content_type and "multipart/form-data" in request.content_type:
        # Use Django's MultiPartParser to extract data and files from the raw request
        parser = MultiPartParser(request.META, request, request.upload_handlers)
        put_data, files = parser.parse()

        email = put_data.get("email", "").strip()
        date_of_birth = put_data.get("date_of_birth", "").strip()
        profile_image = files.get("profile_image")
    else:
        # Fallback for standard JSON bodies if needed
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
            date_of_birth = data.get("date_of_birth", "").strip()
            profile_image = None
        except (json.JSONDecodeError, AttributeError):
            return json_response(error="Invalid request data", status=400)

    # Validation
    if not email:
        return json_response(error="Email is required", status=400)

    # Check if email is already taken by another user
    if User.objects.filter(email=email).exclude(id=user.id).exists():
        return json_response(
            errors={"email": ["This email is already in use"]}, status=400
        )

    # Update user fields
    user.email = email

    if date_of_birth:
        try:
            user.date_of_birth = date_of_birth
        except Exception as e:
            return json_response(errors={"date_of_birth": [str(e)]}, status=400)

    # Handle profile image upload
    if profile_image:
        user.profile_image = profile_image

    try:
        user.save()
        return json_response(data={"user": serialize_user(user)})
    except Exception as e:
        return json_response(error=f"Failed to update profile: {str(e)}", status=500)


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
@login_required
def api_items(request: HttpRequest) -> JsonResponse:
    """
    GET: List all active items with optional search
    POST: Create new item
    """
    if request.method == "GET":
        search_query: str = request.GET.get("search", "").strip()
        items = Item.objects.filter(is_active=True)

        if search_query:
            items = items.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        items = items.order_by("-created_at")
        return json_response(data={"items": [serialize_item(item) for item in items]})

    else:  # POST - Create new item
        title: str = request.POST.get("title", "").strip()
        description: str = request.POST.get("description", "").strip()
        starting_price_str: str = request.POST.get("starting_price", "").strip()
        end_date_str: str = request.POST.get("end_date", "").strip()
        picture = request.FILES.get("picture")

        # Validation
        errors: dict[str, list[str]] = {}
        if not title:
            errors["title"] = ["Title is required"]
        if not description:
            errors["description"] = ["Description is required"]
        if not starting_price_str:
            errors["starting_price"] = ["Starting price is required"]
        if not end_date_str:
            errors["end_date"] = ["End date is required"]
        if not picture:
            errors["picture"] = ["Picture is required"]

        if errors:
            return json_response(errors=errors, status=400)

        try:
            starting_price = Decimal(starting_price_str)
            if starting_price <= 0:
                return json_response(
                    errors={"starting_price": ["Price must be positive"]}, status=400
                )
        except (ValueError, TypeError):
            return json_response(
                errors={"starting_price": ["Invalid price format"]}, status=400
            )

        try:
            from dateutil import parser

            end_date = parser.isoparse(end_date_str)
            if end_date <= timezone.now():
                return json_response(
                    errors={"end_date": ["End date must be in the future"]}, status=400
                )
        except (ValueError, TypeError):
            return json_response(
                errors={"end_date": ["Invalid date format"]}, status=400
            )

        # Create item
        item = Item.objects.create(
            owner=request.user,
            title=title,
            description=description,
            starting_price=starting_price,
            current_price=starting_price,
            picture=picture,
            end_date=end_date,
        )

        return json_response(data={"item": serialize_item(item)}, status=201)


@require_http_methods(["GET"])
@login_required
def api_item_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    """Get single item with bids and questions"""
    try:
        item = Item.objects.get(id=item_id, is_active=True)
        bids = item.bids.all()[:20]  # Latest 20 bids
        questions = item.questions.all().order_by("-asked_at")

        return json_response(
            data={
                "item": serialize_item(item),
                "bids": [serialize_bid(bid) for bid in bids],
                "questions": [serialize_question(q) for q in questions],
            }
        )
    except Item.DoesNotExist:
        return json_response(error="Item not found", status=404)


@require_http_methods(["PUT"])
@login_required
def api_update_item(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    Update an item (only owner can update).

    Editable fields: title, description, picture (optional), end_date
    Starting price cannot be changed after creation.
    """
    try:
        item = Item.objects.get(id=item_id, is_active=True)
    except Item.DoesNotExist:
        return json_response(error="Item not found", status=404)

    # Only owner can update
    if item.owner != request.user:
        return json_response(error="Only the item owner can edit this item", status=403)

    # Handle multipart/form-data for PUT requests
    if request.content_type and "multipart/form-data" in request.content_type:
        parser = MultiPartParser(request.META, request, request.upload_handlers)
        put_data, files = parser.parse()

        title = put_data.get("title", "").strip()
        description = put_data.get("description", "").strip()
        end_date_str = put_data.get("end_date", "").strip()
        picture = files.get("picture")
    else:
        try:
            data = json.loads(request.body)
            title = data.get("title", "").strip()
            description = data.get("description", "").strip()
            end_date_str = data.get("end_date", "").strip()
            picture = None
        except (json.JSONDecodeError, AttributeError):
            return json_response(error="Invalid request data", status=400)

    # Validation
    errors: dict[str, list[str]] = {}
    if not title:
        errors["title"] = ["Title is required"]
    if not description:
        errors["description"] = ["Description is required"]
    if not end_date_str:
        errors["end_date"] = ["End date is required"]

    if errors:
        return json_response(errors=errors, status=400)

    # Parse and validate end_date
    try:
        from dateutil import parser as date_parser
        end_date = date_parser.isoparse(end_date_str)
        if end_date <= timezone.now():
            return json_response(
                errors={"end_date": ["End date must be in the future"]}, status=400
            )
    except (ValueError, TypeError):
        return json_response(
            errors={"end_date": ["Invalid date format"]}, status=400
        )

    # Update item fields
    item.title = title
    item.description = description
    item.end_date = end_date

    if picture:
        item.picture = picture

    try:
        item.save()
        return json_response(data={"item": serialize_item(item)})
    except Exception as e:
        return json_response(error=f"Failed to update item: {str(e)}", status=500)


@require_http_methods(["DELETE"])
@login_required
def api_delete_item(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    Delete an item (soft delete - sets is_active=False).
    Only the owner can delete their item.
    """
    try:
        item = Item.objects.get(id=item_id, is_active=True)
    except Item.DoesNotExist:
        return json_response(error="Item not found", status=404)

    # Only owner can delete
    if item.owner != request.user:
        return json_response(error="Only the item owner can delete this item", status=403)

    # Soft delete - preserve bid history
    item.is_active = False
    item.save()

    return json_response(data={}, status=200)


@require_http_methods(["POST"])
@login_required
def api_place_bid(request: HttpRequest, item_id: int) -> JsonResponse:
    """Place bid on an item"""
    try:
        data = json.loads(request.body)
        amount_raw = data.get("amount", "")
        amount_str = str(amount_raw).strip()
    except (json.JSONDecodeError, AttributeError):
        return json_response(error="Invalid request data", status=400)

    if not amount_str:
        return json_response(error="Bid amount is required", status=400)

    try:
        amount = Decimal(amount_str)
    except (ValueError, TypeError):
        return json_response(error="Invalid bid amount format", status=400)

    try:
        item = Item.objects.get(id=item_id, is_active=True)
    except Item.DoesNotExist:
        return json_response(error="Item not found", status=404)

    # Validation
    if item.owner == request.user:
        return json_response(error="Cannot bid on your own item", status=400)

    if item.is_ended:
        return json_response(error="Auction has ended", status=400)

    if amount <= item.current_price:
        return json_response(
            error=f"Bid must be higher than current price ${item.current_price}",
            status=400,
        )

    # Create bid and update item
    bid = Bid.objects.create(
        item=item,
        bidder=request.user,
        amount=amount,
    )

    item.current_price = amount
    item.save()

    return json_response(
        data={
            "item": serialize_item(item),
            "bid": serialize_bid(bid),
        }
    )


@require_http_methods(["POST"])
@login_required
def api_ask_question(request: HttpRequest, item_id: int) -> JsonResponse:
    """Ask question about an item"""
    try:
        data = json.loads(request.body)
        question_text: str = data.get("question_text", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return json_response(error="Invalid request data", status=400)

    if not question_text:
        return json_response(error="Question text is required", status=400)

    try:
        item = Item.objects.get(id=item_id, is_active=True)
    except Item.DoesNotExist:
        return json_response(error="Item not found", status=404)

    question = Question.objects.create(
        item=item,
        asker=request.user,
        question_text=question_text,
    )

    return json_response(data={"question": serialize_question(question)}, status=201)


@require_http_methods(["POST"])
@login_required
def api_answer_question(request: HttpRequest, question_id: int) -> JsonResponse:
    """Answer a question (only item owner can answer)"""
    try:
        data = json.loads(request.body)
        answer_text: str = data.get("answer_text", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return json_response(error="Invalid request data", status=400)

    if not answer_text:
        return json_response(error="Answer text is required", status=400)

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return json_response(error="Question not found", status=404)

    # Only item owner can answer
    if question.item.owner != request.user:
        return json_response(error="Only item owner can answer", status=403)

    question.answer_text = answer_text
    question.answered_at = timezone.now()
    question.save()

    return json_response(data={"question": serialize_question(question)})
