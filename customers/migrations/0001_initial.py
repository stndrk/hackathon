# Generated by Django 4.2.7 on 2023-12-04 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collaborators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('alternate_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('mother_name', models.CharField(max_length=50)),
                ('father_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('residence_type', models.CharField(max_length=50)),
                ('current_residence_since', models.DateField()),
                ('education_level', models.CharField(max_length=50)),
                ('marital_status', models.CharField(max_length=50)),
                ('spouse_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_name', models.CharField(max_length=100)),
                ('saving_account_no', models.CharField(max_length=50)),
                ('ifsc_code', models.CharField(max_length=20)),
                ('account_holder_name', models.CharField(max_length=100)),
                ('joined_on', models.DateTimeField()),
                ('loan_rejection_reason', models.CharField(max_length=200)),
                ('additional_details', models.JSONField(blank=True, null=True)),
                ('error', models.CharField(max_length=200)),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collaborators.collaboratordetails')),
            ],
        ),
        migrations.CreateModel(
            name='KYCDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='kyc_photos/')),
                ('photo_url', models.URLField(blank=True)),
                ('aadhaar_number', models.CharField(max_length=12, unique=True)),
                ('aadhaar_front_photo', models.ImageField(upload_to='aadhaar_photos/')),
                ('aadhaar_back_photo', models.ImageField(upload_to='aadhaar_photos/')),
                ('aadhaar_url', models.URLField(blank=True)),
                ('pan_number', models.CharField(max_length=10, unique=True)),
                ('pan_photo', models.ImageField(upload_to='pan_photos/')),
                ('pan_url', models.URLField(blank=True)),
                ('driving_license_number', models.CharField(max_length=20, unique=True)),
                ('driving_license_photo', models.ImageField(upload_to='license_photos/')),
                ('driving_license_url', models.URLField(blank=True)),
                ('other_document_name', models.CharField(blank=True, max_length=50)),
                ('other_document_number', models.CharField(blank=True, max_length=20)),
                ('other_document_photo', models.ImageField(blank=True, upload_to='other_document_photos/')),
                ('other_document_url', models.URLField(blank=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_score', models.IntegerField()),
                ('family_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('home_type', models.CharField(max_length=100)),
                ('existing_loan', models.BooleanField(default=False)),
                ('purpose_of_loan', models.TextField()),
                ('eligible_amount', models.IntegerField()),
                ('roi', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requested_amount', models.IntegerField()),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='AddressDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('Permanent', 'Permanent'), ('Current', 'Current'), ('Work', 'Work'), ('Other', 'Other')], max_length=20)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
