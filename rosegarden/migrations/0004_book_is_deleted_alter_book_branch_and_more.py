# Generated by Django 4.1.1 on 2022-10-06 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rosegarden', '0003_alter_branchuserprofile_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rosegarden.branch'),
        ),
        migrations.AlterField(
            model_name='book',
            name='is_biography_or_memoir',
            field=models.BooleanField(default=False),
        ),
    ]