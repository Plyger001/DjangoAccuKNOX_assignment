import threading
from django.dispatch import receiver, Signal

# Defining a custom signal
my_signal = Signal()

# Defining a receiver function for the signal
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
    print(f"Signal handler thread: {threading.current_thread().name}")

# Sending the signal
print(f"Caller thread: {threading.current_thread().name}")
my_signal.send(sender=None)
