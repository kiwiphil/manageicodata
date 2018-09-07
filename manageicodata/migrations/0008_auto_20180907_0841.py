# Generated by Django 2.0.7 on 2018-09-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageicodata', '0007_ico_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icoinstance',
            name='available_tokens',
            field=models.DecimalField(decimal_places=0, help_text='The number of tokens available for sale to the public.', max_digits=14),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='comments',
            field=models.TextField(blank=True, default='', help_text='Report any anomalies and/or ask questions.', max_length=400),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='core_investors',
            field=models.DecimalField(decimal_places=4, help_text='something informative.', max_digits=5),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='cost_of_sales',
            field=models.DecimalField(decimal_places=4, help_text='something informative.', max_digits=5),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='externals',
            field=models.DecimalField(decimal_places=4, help_text='something informative.', max_digits=5),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='hard_cap',
            field=models.DecimalField(decimal_places=0, help_text='The maximum number of tokens to be sold for this ICO.', max_digits=14),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='highest_mentioned_price',
            field=models.DecimalField(decimal_places=6, help_text='Highest price a token sold for during ICO.', max_digits=12),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='lowest_mentioned_price',
            field=models.DecimalField(decimal_places=6, help_text='Lowest price a token sold for during ICO.', max_digits=12),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='public',
            field=models.DecimalField(decimal_places=4, help_text='something informative.', max_digits=5),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='soft_cap',
            field=models.DecimalField(decimal_places=0, help_text='The minimum number of tokens to be sold if ICO will go ahead.', max_digits=14),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='total_tokens',
            field=models.DecimalField(decimal_places=0, help_text='The total number of tokens in this ICO', max_digits=14),
        ),
        migrations.AlterField(
            model_name='icoinstance',
            name='working_capital',
            field=models.DecimalField(decimal_places=4, help_text='something informative.', max_digits=5),
        ),
    ]