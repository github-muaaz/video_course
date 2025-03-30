#!/usr/bin/env python
import os
import sys
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_course.settings')

    try:
        from django.core.management import execute_from_command_line
        from django.contrib.auth import get_user_model

        django.setup()
        User = get_user_model()

        # Auto-create superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@example.com", "Admin@123")
            print("Superuser created successfully!")

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
