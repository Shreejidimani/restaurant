from django.db import models

# Create your models here.
class ItemList(models.Model):
    Category_name = models.CharField(max_length=15)

    def __str__(self):
        return self.Category_name
    

class Items(models.Model):
    Item_name = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    Price = models.IntegerField()
    Category = models.ForeignKey(ItemList, related_name='items', on_delete=models.CASCADE)  # Adjusted related_name
    Image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.Item_name

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as necessary

    def __str__(self):
        return self.name
class AboutUs(models.Model):
    Description = models.TextField(blank=False)

class Feedback(models.Model):
    User_name = models.CharField(max_length=15)  # Field name should be User_name
    Description = models.TextField(blank=False)   # Field name should be Description
    Rating = models.IntegerField()                 # Field name should be Rating
    Image = models.ImageField(upload_to='items/', blank=True)  # Field name should be Image

    def __str__(self):
        return self.User_name
    

class BookTable(models.Model):
    name = models.CharField(max_length=15)  # ✅ Changed from "Name" to "name"
    phone_number = models.IntegerField()  # ✅ Changed from "Phone_number" to "phone_number"
    email = models.EmailField()  # ✅ Changed from "Email" to "email"
    total_person = models.IntegerField()  # ✅ Changed from "Total_person" to "total_person"
    booking_date = models.DateField()  # ✅ Changed from "Booking_date" to "booking_date"

    def __str__(self):
        return f"{self.name} - {self.booking_date}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Order Received'),
        ('preparing', 'Preparing'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
    ]

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    address = models.TextField()
    quantity = models.PositiveIntegerField()
    payment_option = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    upi_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='received')  # Set the default to 'received'

    def __str__(self):
        return f"Order by {self.user_name} for {self.item.Item_name}"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')