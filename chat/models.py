from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_input} | Bot: {self.bot_response}"


class PolicyDocument(models.Model):
    uri = models.URLField()

    def __str__(self):
        return f"Policy Document URI: {self.uri}"
    
    
class Letter(models.Model):
    LETTER_TYPES = [
        ('cover', 'Cover Letter'),
        ('recommendation', 'Recommendation Letter'),
        ('formal', 'Formal Letter'),
        ('informal', 'Informal Letter'),
    ]
    
    letter_type = models.CharField(max_length=20, choices=LETTER_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='letter_templates/')  # Path where the PDF is stored
    
    def __str__(self):
        return self.title
