# Generated by Django 5.1.2 on 2024-10-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('kategori', models.CharField(choices=[('kerajinan_tangan', 'Kerajinan Tangan'), ('makanan_minuman', 'Makanan/Minuman'), ('pakaian', 'Pakaian'), ('lain_lain', 'Lain-lain')], max_length=50)),
                ('harga', models.IntegerField()),
                ('toko', models.CharField(max_length=255)),
                ('alamat', models.CharField(max_length=255)),
                ('deskripsi', models.TextField()),
                ('gambar', models.CharField(blank=True, max_length=255, null=True)),
                ('gambar_file', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
