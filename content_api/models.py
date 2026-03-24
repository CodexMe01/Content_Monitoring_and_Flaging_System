from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ContentItem(models.Model):
    title = models.CharField(max_length=512)
    source = models.CharField(max_length=255)
    body = models.TextField()
    last_updated = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Flag(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
    ]

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='flags')
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='flags')
    score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['keyword', 'content_item'], name='unique_flag')
        ]

    def __str__(self):
        return f"Flag: {self.keyword.name} in {self.content_item.title[:20]} (Score: {self.score}, Status: {self.status})"
