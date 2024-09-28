import time
from django.dispatch import receiver, Signal

# Defining a custom signal
my_signal = Signal()

# Defining a receiver function for the signal
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
    print("Signal handler started")
    time.sleep(5)  # Simulate a long-running task
    print("Signal handler finished")

# Sending the signal
print("Sending signal...")
my_signal.send(sender=None)
print("Signal sent")
