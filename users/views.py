from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,  random, string, pdb
from .models import User
from django.contrib.auth import logout as django_logout

#dummy user satendra@gmail.com=>fkwwAFSh1

@csrf_exempt
def create(request):
    user_data = json.loads(request.body.decode('utf-8'))
    user_name = user_data.get('user_name')
    email = user_data.get('email')
    mobile = user_data.get('mobile')
    user_type = user_data.get('user_type')
    collaborator_name = user_data.get('collaborator_name')
    lender_name = user_data.get('lender_name')
    unique_id = user_data.get('unique_id')
    is_active = user_data.get('is_active')
    is_verified = user_data.get('is_verified')

    if request.method == 'POST':
        if user_type == 'Admin' and is_verified:
            if User.objects.filter(email=email).exists() or User.objects.filter(mobile=mobile).exists():
                return JsonResponse({'error': 'Data already exists'}, status=400)
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
            new_user = User.objects.create(
                user_name=user_name,
                email=email,
                mobile=mobile,
                user_type=user_type,
                collaborator_name=collaborator_name,
                lender_name=lender_name,
                unique_id=unique_id,
                is_active=is_active,
                is_verified=is_verified
            )
            new_user.set_password(random_password)
            new_user.save()
            return JsonResponse({'message': 'User created successfully', 'password': random_password}, status=200)
        elif (user_type == 'Collaborator' or user_type == 'Lender') and isinstance(request.user, User):
            if User.objects.filter(email=email).exists() or User.objects.filter(mobile=mobile).exists():
                return JsonResponse({'error': 'Data already exists'}, status=400)
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
            new_user = User.objects.create(
                user_name=user_name,
                email=email,
                mobile=mobile,
                user_type=user_type,
                collaborator_name=collaborator_name,
                lender_name=lender_name,
                unique_id=unique_id,
                is_active=is_active,
                is_verified=is_verified
            )
            new_user.set_password(random_password)
            new_user.save()
            return JsonResponse({'message': 'User created successfully', 'password': random_password}, status=200)
        else:
            return JsonResponse({'error': 'Unauthorized user type for this action'}, status=400)
           
@csrf_exempt
def login(request):
    if request.method == 'POST':
        user_data = json.loads(request.body.decode('utf-8'))
        email = user_data.get('email')
        password = user_data.get('password')
        mobile = user_data.get('mobile')
        
        try:
            user = User.objects.get(Q(email=email) | Q(mobile=mobile))
            if user.is_verified and user.check_password(password):
                user_data = {
                    'user_id': user.id,
                    'email': user.email,
                    'mobile': user.mobile,
                    'user_type': user.user_type,
                    'collaborator_name': user.collaborator_name,
                    'lender_name': user.lender_name,
                    'is_active': user.is_active,
                    'is_verified': user.is_verified
                }
                return JsonResponse({'message': 'Login successful', 'user': user_data}, status=200)
            else:
                return JsonResponse({'error': 'Incorrect credentials'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        user_data = json.loads(request.body.decode('utf-8'))
        email = user_data.get('email')
        mobile = user_data.get('mobile')
        old_password = user_data.get('old_password')
        new_password = user_data.get('new_password')

        if not email and not mobile:
            return JsonResponse({'error': 'Email or mobile number is required'}, status=400)
        try:
            user = User.objects.get(Q(email=email) | Q(mobile=mobile))
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password updated successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Incorrect old password'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
