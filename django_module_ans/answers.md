## Django signals*

**Question 1**: Are Django signals executed synchronously or asynchronusly?

Django signals are executed synchronously by default. 

This means that when a signal is sent,the code that triggered the signal will wait for the singal handlers to finish executing before continuing i.e the signal's reciever is acalled immidiately when the signal house is sent.

```python
# 
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


<!--It defines a custom signal my_signal,a receiver function my_signal_handler, and sends the signal.Here's a breakdown:
```
1. Import necessary modules.
2. Define a custom signal my_signal using Signal().
3. Define a receiver function my_signal_handler using @receiver decorator.
4. Inside my_signal_handler:
    - Print a start message.
    - Simulate a long-running task with time.sleep(5).
    - Print a finish message.
5. Send the signal using my_signal.send(sender=None).

Output:
Sending signal...
Signal handler started
# (5-second pause)
Signal handler finished
Signal sent

This code demonstrates synchronous signal handling.The signal sending process waits for the receiver function to finish before continuing.To make it asynchronous, use Celery -->
--------------------------------------------------------------------------------

**Question 2**:  Do Django signals run in the same thread as the caller?

Yes, Django signals run in the same thread as the caller unless explicitly configured.

In Django,signals are implemented using a publisher-subscriber pattern.When a signal is sent, it is dispatched to all connected receivers (functions) in the same thread.This means that the code executing the signal-sending code and the code handling the signal (i.e.the receiver functions) run sequentially in the same thread.

```python
#
import threading
from django.dispatch import receiver, Signal

# Define a custom signal
my_signal = Signal()

# Define a receiver function for the signal
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
    print(f"Signal handler thread: {threading.current_thread().name}")

# Sending the signal
print(f"Caller thread: {threading.current_thread().name}")
my_signal.send(sender=None)


<!-- Here's a breakdown:
1. Import necessary modules.
```
import threading
from django.dispatch import receiver, Signal

2. Defining a custom signal.
   python
my_signal = Signal()

1. Defining a receiver function for the signal.
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
print(f"Signal handler thread: {threading.current_thread().name}")

4. Sending the signal.
   python
print(f"Caller thread: {threading.current_thread().name}")
my_signal.send(sender=None)


Output
Caller thread: MainThread
Signal handler thread: MainThread

This confirms that the signal handler (my_signal_handler) runs in the same thread (MainThread) as the caller.-->
----------------------------------------------------------------------------------

**Question 3**: By default do Django signals run in the same database transaction as the caller?

Yes, Django signals run in the same database transaction as the caller unless otherwise specified.

Django's signal framework is tightly integrated with the ORM (Object-Relational Mapping) system.When a signal is sent,it is dispatched within the same database transaction as the code that triggered the signal.This means if a signal is triggered during a transaction,the changes are rolled back if the transaction fails.

```python
#
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


<!-- Here's a breakdown of the code:
```

Section 1: Importing Modules
from django.db import transaction
from django.dispatch import receiver, Signal
from myapp.models import MyModel

- Import necessary modules:
    - transaction: For database transaction management.
    - receiver and Signal: For defining and connecting signal handlers.
    - MyModel: A Django model for demonstration.

Section 2: Defining a Custom Signal
my_signal = Signal()

- Create a custom signal instance named my_signal.

Section 3: Defining a Signal Receiver
@receiver(my_signal)
def my_signal_handler(sender, **kwargs):
    print("Signal handler is modifying the database")
    MyModel.objects.create(name="Signal entry")
- Decorate my_signal_handler with @receiver to connect it to my_signal.
- The receiver function:
    - Prints a message indicating database modification.
    - Creates a new MyModel instance.


Section 4: Simulating a Transaction
try:
    with transaction.atomic():
        print("Starting transaction")
        my_signal.send(sender=None)
        raise Exception("Something went wrong")
except Exception as e:
    print(f"Exception: {e}")
- Simulate a transaction using transaction.atomic().
- Within the transaction:
    - Send my_signal, triggering the receiver function.
    - Raise an exception to simulate an error.


Section 5: Verifying Transaction Rollback
print(f"Entries in MyModel: {MyModel.objects.count()}")
- Check the number of MyModel instances after the transaction.


Expected Output
1. Starting transaction
2. Signal handler is modifying the database
3. Exception: Something went wrong
4. Entries in MyModel: 0


Key Takeaways
- The signal handler modifies the database within the transaction.
- The transaction rolls back due to the raised exception.
- Changes made by the signal handler are reverted, ensuring database consistency.

This code demonstrates how Django signals integrate with database transactions, ensuring atomicity and consistency.-->
----------------------------------------------------------------------------------


class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

# Example usage
rect = Rectangle(10, 5)

# Iterating over the Rectangle instance
for dimension in rect:
    print(dimension)