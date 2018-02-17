from django.utils.text import slugify
from datetime import date, datetime
from django.utils import timezone
from django.db import models
from cities.models import City, Subregion, Region, PostalCode
from versatileimagefield.fields import VersatileImageField
from django.core.files.storage import FileSystemStorage

Ps = FileSystemStorage(location='media/maps/districts/')


class dx_City(models.Model):
    city_name = models.OneToOneField(City, primary_key=True, on_delete=models.PROTECT)
    state_leg_districts = models.ManyToManyField('dx_District')
    population = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True,
                            null=True)

    def __unicode__(self):
        return u'%s' % (self.city_name)

    def save(self, **kwargs):
        if not self.slug:
            new_slug = "MN {0}".format(self.city_name)
            self.slug = slugify(unicode(new_slug))
        super(dx_City, self).save()

    class Meta:
        ordering = ['city_name',]
        verbose_name = 'DigiCity'
        verbose_name_plural = 'DigiCities'


class dx_County(models.Model):
    county_name = models.OneToOneField(Subregion, primary_key=True, on_delete=models.PROTECT)
    state_leg_districts = models.ManyToManyField('dx_District')
    population = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True,
                            null=True)

    def __unicode__(self):
        return u'%s' % (self.county_name)

    def save(self, **kwargs):
        if not self.slug:
            new_slug = "MN {0}".format(self.county_name)
            self.slug = slugify(unicode(new_slug))
        super(dx_County, self).save()

    class Meta:
        ordering = ['county_name']
        verbose_name = 'DigiCounty'
        verbose_name_plural = 'DigiCounties'


class dx_State(models.Model):
    state_name = models.OneToOneField(Region, primary_key=True, on_delete=models.PROTECT)

    def __unicode__(self):
        return u'%s' % (self.state_name)

    class Meta:
        ordering = ['state_name']
        verbose_name = 'dx_State'
        verbose_name_plural = 'dx_States'


class dx_PostalCode(models.Model):
    zip_code = models.OneToOneField(PostalCode, primary_key=True, on_delete=models.PROTECT)
    state_leg_districts = models.ManyToManyField('dx_District')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True,
                            null=True)

    def __unicode__(self):
        return u'%s' % (self.zip_code)

    def save(self, **kwargs):
        if not self.slug:
            new_slug = "MN {0}".format(self.zip_code)
            self.slug = slugify(unicode(new_slug))
        super(dx_PostalCode, self).save()

    class Meta:
        ordering = ['zip_code']
        verbose_name = 'dx_PostalCode'
        verbose_name_plural = 'dx_PostalCodes'


class dx_District(models.Model):
    number = models.CharField(max_length=3)
    district_type = models.CharField(max_length=32)
    map_image = VersatileImageField(storage=Ps, blank=True, null=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True,
                            null=True)
    city = models.ForeignKey(dx_City,
                              blank=True,
                              null=True,
                              on_delete=models.PROTECT)
    county = models.ForeignKey(dx_County,
                               blank=True,
                               null=True,
                               on_delete=models.PROTECT)
    state = models.ForeignKey(dx_State,
                              blank=True,
                              null=True,
                              on_delete=models.PROTECT)
    notes = models.TextField(blank=True,
                               null=True)
    # country = models.ForeignKey('Country', to_field='slug', blank=True, null=True)

    def __unicode__(self):
        return u'%s %s' % (self.district_type, self.number)

    def name(self):
        return u'%s %s' % (self.district_type, self.number)

    def get_absolute_url(self):
        return u'/district/%s' % (self.slug)

    def save(self, **kwargs):
        if not self.slug:
            if self.state:
                new_slug = "{0} {1} {2}".format(self.state, self.district_type, self.number)
                self.slug = slugify(unicode(new_slug))
            if self.county:
                new_slug = "{0} {1} {2}".format(self.county, self.district_type, self.number)
                self.slug = slugify(unicode(new_slug))
            if self.city:
                new_slug = "{0} {1} {2}".format(self.city, self.district_type, self.number)
                self.slug = slugify(unicode(new_slug))
        super(dx_District, self).save()

    class Meta:
        ordering = ['district_type', 'number']
        verbose_name = 'Legislative District'
        verbose_name_plural = 'Legislative Districts'

