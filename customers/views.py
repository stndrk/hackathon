from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Analysis, AddressDetails, KYCDetails
import json
from django.shortcuts import get_object_or_404


@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer = Customer(**data)
        customer.save()
        customer_id = customer.pk  
        return JsonResponse({'message': 'Customer created successfully', 'id': customer_id}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            fields = [
                'first_name', 'last_name', 'mobile', 'alternate_mobile', 'mother_name',
                'father_name', 'gender', 'email', 'dob', 'residence_type',
                'current_residence_since', 'education_level', 'marital_status',
                'spouse_name', 'bank_name', 'saving_account_no', 'ifsc_code',
                'account_holder_name', 'existing_loan', 'purpose_of_loan',
                'joined_on', 'loan_rejection_reason']
            for field in fields:
                if field in data:
                    setattr(customer, field, data[field])
            customer.save()
            return JsonResponse({'message': 'Customer updated successfully'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'GET':
        serialized_data = {}
        payload = json.loads(request.body)
        for field in payload:
            if hasattr(customer, field):
                serialized_data[field] = getattr(customer, field)
        return JsonResponse(serialized_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#########################################################################################################################
def create_analysis(request, customer_id):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            analysis = Analysis.objects.create(
                customer_id=customer_id,
                credit_score=payload.get('credit_score'),
                family_income=payload.get('family_income'),
                monthly_income=payload.get('monthly_income'),
                home_type=payload.get('home_type'),
                existing_loan=payload.get('existing_loan'),
                purpose_of_loan=payload.get('purpose_of_loan'),
                requested_amount=payload.get('requested_amount')
            )
            analysis_id = analysis.pk 
            return JsonResponse({'message': 'Analysis entry created successfully', 'analysis_id': analysis_id}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def fetch_analysis_by_id(request, customer_id):
    if request.method == 'GET':
        analysis_record = Analysis.objects.filter(customer_id=customer_id).values().first()
        if analysis_record:
            return JsonResponse({'analysis_record': analysis_record})
        else:
            return JsonResponse({'error': 'Analysis record not found for the given Customer'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def update_analysis(request, customer_id, analysis_id):
    if request.method == 'PUT':
        try:
            payload = json.loads(request.body)
            data = Analysis.objects.get(customer_id=customer_id, pk=analysis_id)
            data.credit_score = payload.get('credit_score', data.credit_score)
            data.family_income = payload.get('family_income', data.family_income)
            data.monthly_income = payload.get('monthly_income', data.monthly_income)
            data.home_type = payload.get('home_type', data.home_type)
            data.existing_loan = payload.get('existing_loan', data.existing_loan)
            data.purpose_of_loan = payload.get('purpose_of_loan', data.purpose_of_loan)
            data.save()
            return JsonResponse({'message': 'Analysis entry updated successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Analysis.DoesNotExist:
            return JsonResponse({'error': 'Analysis record not found for the given Customer'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

################################################################################################################
def create_address(request, customer_id):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            address_instance = AddressDetails.objects.create(
                customer_id=customer_id,
                address_type=payload.get('address_type'),
                address_line1=payload.get('address_line1'),
                address_line2=payload.get('address_line2', ''),
                pincode=payload.get('pincode'),
                city=payload.get('city'),
                state=payload.get('state')
            )
            return JsonResponse({'message': 'Address entry created successfully'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def fetch_addresses_by_type(request, customer_id, address_type):
    if request.method == 'GET':
        try:
            addresses = AddressDetails.objects.filter(customer_id=customer_id, address_type=address_type).values()
            return JsonResponse({'addresses': list(addresses)}, status=200)
        except AddressDetails.DoesNotExist:
            return JsonResponse({'error': 'Addresses not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def update_address_by_type(request, customer_id, address_type):
    if request.method == 'PUT':
        try:
            payload = json.loads(request.body)
            addresses = AddressDetails.objects.filter(customer_id=customer_id, address_type=address_type)
            for address in addresses:
                address.address_line1 = payload.get('address_line1', address.address_line1)
                address.address_line2 = payload.get('address_line2', address.address_line2)
                address.pincode = payload.get('pincode', address.pincode)
                address.city = payload.get('city', address.city)
                address.state = payload.get('state', address.state)
                address.save()
            return JsonResponse({'message': 'Addresses updated successfully'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except AddressDetails.DoesNotExist:
            return JsonResponse({'error': 'Addresses not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def fetch_all_addresses_by_customer(request, customer_id):
    if request.method == 'GET':
        addresses = AddressDetails.objects.filter(customer_id=customer_id).values()
        if addresses:
            return JsonResponse({'addresses': list(addresses)}, status=200)
        else:
            return JsonResponse({'error': 'Addresses not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


######################################################################################################
def create_kyc_details(request, customer_id):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            kyc_details = KYCDetails.objects.create(
                customer_id=customer_id,
                photo=payload.get('photo'),
                photo_url=payload.get('photo_url'),
                aadhaar_number=payload.get('aadhaar_number'),
                aadhaar_front_photo=payload.get('aadhaar_front_photo'),
                aadhaar_back_photo=payload.get('aadhaar_back_photo'),
                aadhaar_url=payload.get('aadhaar_url'),
                pan_number=payload.get('pan_number'),
                pan_photo=payload.get('pan_photo'),
                pan_url=payload.get('pan_url'),
                driving_license_number=payload.get('driving_license_number'),
                driving_license_photo=payload.get('driving_license_photo'),
                driving_license_url=payload.get('driving_license_url'),
                other_document_name=payload.get('other_document_name'),
                other_document_number=payload.get('other_document_number'),
                other_document_photo=payload.get('other_document_photo'),
                other_document_url=payload.get('other_document_url'),
            )
            kyc_id = kyc_details.pk 
            return JsonResponse({'message': 'KYC Details entry created successfully', 'kyc_id': kyc_id}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def fetch_kyc_details(request, customer_id):
    if request.method == 'GET':
        try:
            kyc_details = KYCDetails.objects.get(customer_id=customer_id)
            serialized_data = {
                'photo': kyc_details.photo.url,
                'photo_url': kyc_details.photo_url,
                'aadhaar_number': kyc_details.aadhaar_number,
                'aadhaar_front_photo': kyc_details.aadhaar_front_photo,
                'aadhaar_back_photo': kyc_details.aadhaar_back_photo,
                'aadhaar_url': kyc_details.aadhaar_url,
                'pan_number': kyc_details.pan_number,
                'pan_photo': kyc_details.pan_photo,
                'pan_url': kyc_details.pan_url,
                'driving_license_number': kyc_details.driving_license_number,
                'driving_license_photo': kyc_details.driving_license_photo,
                'driving_license_url': kyc_details.driving_license_url,
                'other_document_name': kyc_details.other_document_name,
                'other_document_number': kyc_details.other_document_number,
                'other_document_photo': kyc_details.other_document_photo,
                'other_document_url': kyc_details.other_document_url
            }
            return JsonResponse(serialized_data, status=200)
        except KYCDetails.DoesNotExist:
            return JsonResponse({'error': 'KYC Details not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def update_kyc_details(request, customer_id):
    if request.method == 'PUT':
        try:
            payload = json.loads(request.body)
            kyc_details = KYCDetails.objects.get(customer_id=customer_id)
            kyc_details.photo = payload.get('photo', kyc_details.photo)
            kyc_details.photo_url = payload.get('photo_url', kyc_details.photo_url)
            kyc_details.aadhaar_number = payload.get('aadhaar_number', kyc_details.aadhaar_number)
            kyc_details.aadhaar_front_photo = payload.get('aadhaar_front_photo', kyc_details.aadhaar_front_photo)
            kyc_details.aadhaar_back_photo = payload.get('aadhaar_back_photo', kyc_details.aadhaar_back_photo)
            kyc_details.aadhaar_url = payload.get('aadhaar_url', kyc_details.aadhaar_url)
            kyc_details.pan_number = payload.get('pan_number', kyc_details.pan_number)
            kyc_details.pan_photo = payload.get('pan_photo', kyc_details.pan_photo)
            kyc_details.pan_url = payload.get('pan_url', kyc_details.pan_url)
            kyc_details.driving_license_number = payload.get('driving_license_number', kyc_details.driving_license_number)
            kyc_details.driving_license_photo = payload.get('driving_license_photo', kyc_details.driving_license_photo)
            kyc_details.driving_license_url = payload.get('driving_license_url', kyc_details.driving_license_url)
            kyc_details.other_document_name = payload.get('other_document_name', kyc_details.other_document_name)
            kyc_details.other_document_number = payload.get('other_document_number', kyc_details.other_document_number)
            kyc_details.other_document_photo = payload.get('other_document_photo', kyc_details.other_document_photo)
            kyc_details.other_document_url = payload.get('other_document_url', kyc_details.other_document_url)

            kyc_details.save()
            return JsonResponse({'message': 'KYC Details updated successfully'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except KYCDetails.DoesNotExist:
            return JsonResponse({'error': 'KYC Details not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)