from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayBeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_one', models.DateTimeField(default=django.utils.timezone.now)),
                ('mark_two', models.DateTimeField(null=True)),
                ('mark_three', models.DateTimeField(null=True)),
                ('mark_four', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Point',
        ),
        migrations.AddField(
            model_name='daybeat',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.daypoint'),
        ),
    ]
