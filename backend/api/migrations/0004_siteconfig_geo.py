from django.db import migrations, models


class Migration(migrations.Migration):
    """新增 SiteConfig 地理坐标字段，支撑本地 SEO / GEO 结构化数据"""

    dependencies = [
        ('api', '0003_certificate_milestone_articlelike'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='纬度'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='经度'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='address_region',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='所在省份'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='address_locality',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='所在城市/区'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='邮政编码'),
        ),
    ]
