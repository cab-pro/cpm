from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from decimal import Decimal


class Account(models.Model):
    """ Defines a customer account
    """
    name = models.CharField(max_length=128)
    billing_address = models.CharField(max_length=1024)
    billing_phone = models.CharField(max_length=32)
    billing_email = models.EmailField(max_length=256)
    contact_name = models.CharField(max_length=128)
    discount = models.DecimalField(max_digits=3, decimal_places=2)

    def __repr__(self):
        return f'<Account name: {self.name}>'

    def __str__(self):
        return f'Account name: {self.name}'


class Material(models.Model):
    """ Applied to Project/Cabinet via Specification
    """
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    thickness = models.DecimalField(max_digits=4, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)
    sheet_cost = models.DecimalField(max_digits=6, decimal_places=2)
    waste_factor = models.DecimalField(max_digits=3, decimal_places=2)
    markup = models.DecimalField(max_digits=3, decimal_places=2)
    date_updated = models.DateTimeField(
        default=datetime.now,
        blank=True
    )

    @property
    def sq_ft_cost(self):
        sq_ft = ((self.width / 12) * (self.length / 12))
        before_markup = self.sheet_cost / sq_ft
        after_markup = before_markup + (before_markup * self.markup)
        return after_markup

    def __repr__(self):
        return f'<Material: {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Hardware(models.Model):
    """ Applied to Project/Cabinet via Specification
    """
    name = models.CharField(max_length=128)
    cost_per = models.DecimalField(max_digits=6, decimal_places=2)
    UNIT_TYPE_CHOICES = [
        ('each', 'Each'),
        ('pair', 'Pair'),
        ('set', 'Set')
    ]
    unit_type = models.CharField(
        choices=UNIT_TYPE_CHOICES,
        max_length=16
    )
    markup = models.DecimalField(max_digits=3, decimal_places=2)

    def __repr__(self):
        return f'<Hardware: {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Labor(models.Model):
    """ Correlates items to labor required, for invoice calculations
    """
    item_name = models.CharField(max_length=128)
    minutes = models.IntegerField()
    units = models.CharField(max_length=32)

    def __repr__(self):
        return f'<Labor: {self.item_name}>'

    def __str__(self):
        return f'{self.item_name}'


class Project(models.Model):
    """ Defines a Project within an Account
    """
    name = models.CharField(max_length=128)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    physical_address = models.CharField(max_length=1024)
    site_contact = models.CharField(max_length=128)
    contact_phone = models.CharField(max_length=32)
    contact_email = models.EmailField(max_length=256)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __repr__(self):
        return f'<Project name: {self.name}>'

    def __str__(self):
        return f'Project: {self.name}'


class Room(models.Model):
    """ Defines a Project within an Account
    """
    name = models.CharField(max_length=128)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    @property
    def drawer_count(self):
        cabinets = Cabinet.objects.filter(room=self)
        count = 0
        for cab in cabinets:
            count += cab.drawers.count()
        return count

    def __repr__(self):
        return f'<Room name: {self.name} in {self.project.name}>'

    def __str__(self):
        return f'Room name: {self.name} in {self.project.name}'


class Specification(models.Model):
    """ Defines a default Specification within a Project
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    interior_material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interior_specifications'
    )
    exterior_material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exterior_specifications'
    )
    name = models.CharField(max_length=128)
    CONSTRUCTION_CHOICES = [
        ('Frameless', 'Frameless'),
        ('Faceframe Overlay', 'Faceframe Overlay'),
        ('Faceframe Inset', 'Faceframe Inset')
    ]
    construction = models.CharField(
        choices=CONSTRUCTION_CHOICES,
        default='frameless',
        max_length=32
    )
    CATALOG_CHOICES = [
        ('Laminate', 'Laminate'),
        ('Wood Slab', 'Wood Slab'),
        ('Wood 5-Piece', 'Wood 5-Piece'),
        ('Thermofoil', 'Thermofoil')
    ]
    catalog = models.CharField(
        choices=CATALOG_CHOICES,
        default='laminate',
        max_length=32
    )
    FINISH_LEVEL_CHOICES = [
        ('Unfinished', 'Unfinished'),
        ('Sand & Prep Only', 'Sand & Prep Only'),
        ('Clear', 'Clear'),
        ('Stain', 'Stain'),
        ('Stain & Glaze', 'Stain & Glaze'),
        ('Stain & Distress', 'Stain & Distress'),
        ('Stain, Glaze & Distress', 'Stain, Glaze & Distress'),
        ('Paint', 'Paint'),
        ('Paint & Glaze', 'Paint & Glaze'),
        ('Paint & Distress', 'Paint & Distress'),
        ('Paint, Glaze & Distress', 'Paint, Glaze & Distress')
    ]
    finish_level = models.CharField(
        choices=FINISH_LEVEL_CHOICES,
        default='Unfinished',
        max_length=125
    )

    def __repr__(self):
        return f'<Specification name: {self.name}>'

    def __str__(self):
        return f'Project: {self.project.name} | Specification: {self.name}'


class Cabinet(models.Model):
    """ Defines a Cabinet within a Project
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='cabinets'
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cabinets'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='cabinets'
    )
    cabinet_number = models.IntegerField()
    width = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    depth = models.DecimalField(max_digits=6, decimal_places=2)
    number_of_doors = models.IntegerField()
    number_of_shelves = models.IntegerField()
    finished_interior = models.BooleanField(default=False)
    finished_left_end = models.BooleanField(default=False)
    finished_right_end = models.BooleanField(default=False)
    finished_top = models.BooleanField(default=False)
    finished_bottom = models.BooleanField(default=False)

    @property
    def price(self):
        vertical = self.height * self.depth / 144
        horizontal = self.width * self.depth / 144
        int_waste = Decimal.from_float(1.2)
        ext_waste = Decimal.from_float(1.2)
        int_sq_ft_cost = self.specification.interior_material.sq_ft_cost * int_waste
        ext_sq_ft_cost = self.specification.exterior_material.sq_ft_cost * ext_waste

        left_side = vertical * ext_sq_ft_cost if self.finished_left_end else vertical * int_sq_ft_cost
        right_side = vertical * ext_sq_ft_cost if self.finished_right_end else vertical * int_sq_ft_cost
        top = horizontal * ext_sq_ft_cost if self.finished_top else horizontal * int_sq_ft_cost
        bottom = horizontal * ext_sq_ft_cost if self.finished_bottom else horizontal * int_sq_ft_cost

        if self.finished_interior:
            left_side = vertical * ext_sq_ft_cost
            right_side = vertical * ext_sq_ft_cost
            top = horizontal * ext_sq_ft_cost
            bottom = horizontal * ext_sq_ft_cost
            back = self.width * self.height / 144 * ext_sq_ft_cost
            shelves = horizontal * ext_sq_ft_cost
        else:
            shelves = horizontal * int_sq_ft_cost
            back = self.width * self.height / 144 * int_sq_ft_cost

        case_material = left_side + right_side + top + bottom + back + (self.number_of_shelves * shelves)

        return case_material

    def __repr__(self):
        return f'<Cabinet project: {str(self.project.id)} | Room: {self.room.name} | Cab No: {self.cabinet_number} >'

    def __str__(self):
        return f'Cabinet for project: {str(self.project.id)} | Room: {self.room.name} | Cab No: {self.cabinet_number}'


class Drawer(models.Model):
    """ Drawers for Cabinets
    """
    cabinet = models.ForeignKey(
        Cabinet,
        on_delete=models.CASCADE,
        related_name='drawers'
    )
    height = models.DecimalField(max_digits=6, decimal_places=2)
    material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        related_name='drawer_material'
    )

    def __repr__(self):
        return f'<Drawer for Cab No: {self.cabinet.cabinet_number} in {self.cabinet.project.name}>'

    def __str__(self):
        return f'Drawer for Cab No: {self.cabinet.cabinet_number} in {self.cabinet.project.name}'
