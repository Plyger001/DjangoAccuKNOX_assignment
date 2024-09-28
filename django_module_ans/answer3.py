from django.db import transaction
from django.dispatch import receiver, Signal
from myapp.models import MyModel

# Define a custom signal
my_signal = Signal()

# Define a receiver function for the signal
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
    print("Signal handler is modifying the database")
    # Modify the database
    MyModel.objects.create(name="Signal entry")

# Simulate a transaction
try:
    with transaction.atomic():
        print("Starting transaction")
        my_signal.send(sender=None)
        raise Exception("Something went wrong")
except Exception as e:
    print(f"Exception: {e}")

# Check if changes were saved (they should not be because of the rollback)
print(f"Entries in MyModel: {MyModel.objects.count()}")
