# Generated manually for token fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='activity_type',
            field=models.CharField(choices=[('login', 'User Login'), ('logout', 'User Logout'), ('profile_update', 'Profile Update'), ('password_change', 'Password Change'), ('password_reset', 'Password Reset'), ('password_reset_request', 'Password Reset Request'), ('email_verification', 'Email Verification'), ('account_deletion', 'Account Deletion'), ('registration', 'User Registration'), ('2fa_enabled', 'Two-Factor Authentication Enabled'), ('2fa_disabled', 'Two-Factor Authentication Disabled')], max_length=25),
        ),
        migrations.CreateModel(
            name='TOTPDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
            ],
            options={
                'verbose_name': 'TOTP Device',
                'verbose_name_plural': 'TOTP Devices',
            },
        ),
    ]