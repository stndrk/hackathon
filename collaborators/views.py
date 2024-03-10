from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Collaborators
import json,pdb

@csrf_exempt
def create(request):
    pdb.set_trace()
    if request.method == 'POST':
        data = json.loads(request.body.strip())
        collaborator = Collaborators(**data)
        collaborator.save()
        collaborator_data = {
        'id': collaborator.id,
        'mobile': collaborator.mobile,
        'email': collaborator.email
        }
        return JsonResponse({'message': 'Collaborator created successfully', 'collaborator': collaborator_data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        collaborator_data = Collaborators.objects.filter(id=data.get('id')).first()
        if collaborator_data:
            # Update fields based on the received data
            for key, value in data.items():
                setattr(collaborator_data, key, value)
            collaborator_data.save()
            return JsonResponse({'message': 'Collaborator updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Collaborator not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch(request):
    data = json.loads(request.body)
    collaborator = Collaborators.objects.filter(id=data.get('id')).values().first()
    if request.method == 'GET':
        serialized_data = [{
            'name': collaborator.get('name'),
            'father_name': collaborator.get('father_name'),
            'mother_name': collaborator.get('mother_name'),
            'email': collaborator.get('email'),
            'mobile': collaborator.get('mobile'),
            'gender': collaborator.get('gender'),
            'joined_on': collaborator.get('joined_on'),
            'designation': collaborator.get('designation'),
            'address': collaborator.get('address'),
            'city': collaborator.get('city'),
            'state': collaborator.get('state'),
            'pan_number': collaborator.get('pan_number'),
            'alternate_number': collaborator.get('alternate_number'),
            'is_active': collaborator.get('is_active'),
            'is_verified': collaborator.get('is_verified')
        }]
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def user_collaborators(request):
    if request.method == 'GET':
        user = request.user  
        collaborators = user.collaborators.all()
        serialized_data = [{
            'name': collaborator.name,
            'father_name': collaborator.father_name,
            'mother_name': collaborator.mother_name,
            'email': collaborator.email,
            'mobile': collaborator.mobile,
            'gender': collaborator.gender,
            'joined_on': collaborator.joined_on,
            'designation': collaborator.designation,
            'address': collaborator.address,
            'city': collaborator.city,
            'state': collaborator.state,
            'pan_number': collaborator.pan_number,
            'alternate_number': collaborator.alternate_number,
            'is_active': collaborator.is_active,
            'is_verified': collaborator.is_verified
        } for collaborator in collaborators]
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
