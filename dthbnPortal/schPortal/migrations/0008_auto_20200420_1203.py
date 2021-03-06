# Generated by Django 3.0.4 on 2020-04-20 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schPortal', '0007_school_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='lga_num',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lga_num', to='schPortal.LGA'),
        ),
        migrations.AlterField(
            model_name='school',
            name='User',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='school',
            name='sch_logo',
            field=models.FileField(null=True, upload_to='images/school/sch_logo'),
        ),
        migrations.AlterField(
            model_name='school',
            name='updated_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Indexing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='images/indexing/index_profile_img')),
                ('cadre', models.CharField(blank=True, max_length=200, null=True)),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.CharField(blank=True, max_length=200, null=True)),
                ('telephone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('religion', models.CharField(blank=True, max_length=200, null=True)),
                ('nationality', models.CharField(blank=True, max_length=200, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=200, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=200, null=True)),
                ('place_of_work', models.CharField(blank=True, max_length=200, null=True)),
                ('school_attended1', models.CharField(blank=True, max_length=200, null=True)),
                ('school_attended2', models.CharField(blank=True, max_length=200, null=True)),
                ('school_attended3', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification1', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification2', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification3', models.CharField(blank=True, max_length=200, null=True)),
                ('admission_year', models.CharField(blank=True, max_length=200, null=True)),
                ('graduation_year', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_address', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_name1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_address1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_phone1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_name2', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_address2', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_phone2', models.CharField(blank=True, max_length=200, null=True)),
                ('marriage_cert', models.ImageField(blank=True, null=True, upload_to='image/indexing/marriage_cert')),
                ('examination_number1', models.CharField(blank=True, max_length=100, null=True)),
                ('examination_year1', models.CharField(blank=True, max_length=20, null=True)),
                ('examination_type1', models.CharField(blank=True, max_length=20, null=True)),
                ('examination_number2', models.CharField(blank=True, max_length=100, null=True)),
                ('examination_year2', models.CharField(blank=True, max_length=20, null=True)),
                ('examination_type2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub1', models.CharField(blank=True, max_length=20, null=True)),
                ('grade1', models.CharField(blank=True, max_length=20, null=True)),
                ('sub2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub3', models.CharField(blank=True, max_length=20, null=True)),
                ('sub4', models.CharField(blank=True, max_length=20, null=True)),
                ('grade4', models.CharField(blank=True, max_length=20, null=True)),
                ('sub5', models.CharField(blank=True, max_length=20, null=True)),
                ('grade5', models.CharField(blank=True, max_length=20, null=True)),
                ('sub6', models.CharField(blank=True, max_length=20, null=True)),
                ('grade6', models.CharField(blank=True, max_length=20, null=True)),
                ('sub7', models.CharField(blank=True, max_length=20, null=True)),
                ('grade7', models.CharField(blank=True, max_length=20, null=True)),
                ('sub1_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade1_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub2_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade2_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub3_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade3', models.CharField(blank=True, max_length=20, null=True)),
                ('sub4_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade4_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub5_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade5_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub6_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade6_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sub7_2', models.CharField(blank=True, max_length=20, null=True)),
                ('grade7_2', models.CharField(blank=True, max_length=20, null=True)),
                ('submitted', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='institution', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.Region')),
            ],
        ),
        migrations.CreateModel(
            name='ExamRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='images/exam/exam_profile_img')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('telephone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=200, null=True)),
                ('religion', models.CharField(blank=True, max_length=200, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=200, null=True)),
                ('maiden_name', models.CharField(blank=True, max_length=200, null=True)),
                ('senatorial_district', models.CharField(blank=True, max_length=200, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('qualification1', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification2', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification3', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification4', models.CharField(blank=True, max_length=200, null=True)),
                ('prof_qualification1', models.CharField(blank=True, max_length=200, null=True)),
                ('prof_qualification2', models.CharField(blank=True, max_length=200, null=True)),
                ('prof_qualification3', models.CharField(blank=True, max_length=200, null=True)),
                ('prof_qualification4', models.CharField(blank=True, max_length=200, null=True)),
                ('institution_attended1', models.CharField(blank=True, max_length=200, null=True)),
                ('institution_attended2', models.CharField(blank=True, max_length=200, null=True)),
                ('institution_attended3', models.CharField(blank=True, max_length=200, null=True)),
                ('institution_attended4', models.CharField(blank=True, max_length=200, null=True)),
                ('hod_name', models.CharField(blank=True, max_length=200, null=True)),
                ('hod_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('hod_email', models.CharField(blank=True, max_length=100, null=True)),
                ('employment_status', models.BooleanField(blank=True, null=True)),
                ('present_position', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('office_name', models.CharField(blank=True, max_length=100, null=True)),
                ('offfice_address', models.CharField(blank=True, max_length=100, null=True)),
                ('sector', models.CharField(blank=True, max_length=100, null=True)),
                ('office_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('office_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('referee_name1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_address1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_phone1', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_name2', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_address2', models.CharField(blank=True, max_length=200, null=True)),
                ('referee_phone2', models.CharField(blank=True, max_length=200, null=True)),
                ('mode_of_payment', models.CharField(blank=True, max_length=200, null=True)),
                ('cadre', models.CharField(blank=True, max_length=200, null=True)),
                ('waec_result', models.ImageField(blank=True, null=True, upload_to='images/exam_sector/waec_result')),
                ('dental_school_result', models.ImageField(blank=True, null=True, upload_to='images/exam_sector/dental_result')),
                ('dental_school_testimonial', models.ImageField(blank=True, null=True, upload_to='images/exam_sector/dental_testimonial')),
                ('lga_of_birth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lga_of_birth', to='schPortal.LGA')),
                ('lga_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lga_state', to='schPortal.LGA')),
                ('office_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_country', to='cities_light.Country')),
                ('office_lga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_lga', to='schPortal.LGA')),
                ('office_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_state', to='cities_light.Region')),
                ('residential_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.Country')),
                ('residential_lga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schPortal.LGA')),
                ('residential_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residential_state', to='cities_light.Region')),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='school', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.Region')),
                ('state_of_birth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='state_of_birth', to='cities_light.Region')),
                ('state_of_origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='state_of_origin', to='cities_light.Region')),
            ],
        ),
    ]
