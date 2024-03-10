from django.db import models
from collaborators.models import Collaborators

class Customer(models.Model):
    collaborator = models.ForeignKey(Collaborators, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    email = models.EmailField()
    dob = models.DateField()
    residence_type = models.CharField(max_length=50)
    current_residence_since = models.DateField()
    education_level = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50)
    spouse_name = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100)
    saving_account_no = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=100)
    joined_on = models.DateTimeField()
    loan_rejection_reason = models.CharField(max_length=200)
    additional_details = models.JSONField(blank=True, null=True)
    error = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Analysis(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    credit_score = models.IntegerField()
    family_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    home_type = models.CharField(max_length=100)
    existing_loan = models.BooleanField(default=False)
    purpose_of_loan = models.TextField()
    eligible_amount = models.IntegerField()
    roi = models.DecimalField(max_digits=10, decimal_places=2)
    requested_amount = models.IntegerField()

    def __str__(self):
        return f"Analysis ID: {self.pk}"

class AddressDetails(models.Model):
    ADDRESS_TYPES = (
        ('Permanent', 'Permanent'),
        ('Current', 'Current'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.customer}'s {self.address_type} Address"
    
class KYCDetails(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='kyc_photos/')
    photo_url = models.URLField(blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    aadhaar_front_photo = models.ImageField(upload_to='aadhaar_photos/')
    aadhaar_back_photo = models.ImageField(upload_to='aadhaar_photos/')
    aadhaar_url = models.URLField(blank=True)
    pan_number = models.CharField(max_length=10, unique=True)
    pan_photo = models.ImageField(upload_to='pan_photos/')
    pan_url = models.URLField(blank=True)
    driving_license_number = models.CharField(max_length=20, unique=True)
    driving_license_photo = models.ImageField(upload_to='license_photos/')
    driving_license_url = models.URLField(blank=True)
    other_document_name = models.CharField(max_length=50, blank=True)
    other_document_number = models.CharField(max_length=20, blank=True)
    other_document_photo = models.ImageField(upload_to='other_document_photos/', blank=True)
    other_document_url = models.URLField(blank=True)

    def __str__(self):
        return f"KYC Details for {self.customer.first_name} {self.customer.last_name}"
