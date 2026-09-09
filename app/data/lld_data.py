from typing import Dict, Any, List

LLD_CHAPTERS: Dict[str, Any] = {
    "solid": {
        "title": "SOLID Design Principles",
        "content": """
### Single Responsibility Principle (SRP)
> A class should have one, and only one, reason to change.
- **Bad**: A `User` class that handles database saving, validation, AND email notification sending.
- **Good**: Separate into `User` (entity), `UserRepository` (persistence), and `EmailService` (notification).

### Open/Closed Principle (OCP)
> Software entities should be open for extension, but closed for modification.
- **Bad**: Using a massive switch statement on a shape class to calculate area. Adding a new shape requires changing this class.
- **Good**: Define a `Shape` abstract base class with an `area()` method. Derive `Circle`, `Rectangle`, etc., implementing `area()`.

### Liskov Substitution Principle (LSP)
> Subtypes must be substitutable for their base types without altering correctness.
- **Classic Violation**: `Ostrich` inherits from `Bird`. If `Bird` has a method `fly()`, calling it on `Ostrich` throws an exception, violating LSP.
- **Good**: Split behaviors. Have `Bird` and a subclass `FlyingBird` with the `fly()` method, or use composition.

### Interface Segregation Principle (ISP)
> Clients should not be forced to depend on methods they do not use.
- **Bad**: An interface `Worker` containing `work()` and `eat()`. A robot worker class has to implement `eat()`, which it doesn't do.
- **Good**: Split into `Workable` and `Feedable` interfaces.

### Dependency Inversion Principle (DIP)
> High-level modules should not depend on low-level modules. Both should depend on abstractions.
- **Bad**: An `OrderProcessor` class instantiating a concrete `SqliteDatabase` inside its constructor.
- **Good**: `OrderProcessor` receives a `IDatabase` interface via constructor injection.
""",
        "code_example": {
            "bad": """class Report:
    def __init__(self, content):
        self.content = content
        
    def generate_pdf(self):
        # Generates PDF
        pass
        
    def save_to_db(self):
        # Database logic
        pass""",
            "good": """class Report:
    def __init__(self, content):
        self.content = content

class PDFReportGenerator:
    def generate(self, report: Report):
        # PDF generation only
        pass

class ReportRepository:
    def save(self, report: Report):
        # Save to database only
        pass"""
        }
    },
    "patterns": {
        "title": "Gang of Four (GoF) Design Patterns",
        "content": """
### Strategy Pattern (Behavioral)
Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.
- **Example**: Payment options (Credit Card, PayPal, Crypto). `PaymentContext` accepts a `PaymentStrategy` interface.

### Factory Method Pattern (Creational)
Defines an interface for creating an object, but lets subclasses decide which class to instantiate.
- **Example**: A logistics app. Creator class `Logistics` declares `createTransport()`. Subclasses `RoadLogistics` and `SeaLogistics` instantiate `Truck` and `Ship`.

### Observer Pattern (Behavioral)
Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.
- **Example**: Event streaming, chat apps, newsletter subscriptions.

### Decorator Pattern (Structural)
Attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.
- **Example**: Coffee customizers (Milk, Sugar, Whip) wrapping a base `Coffee` class.
"""
    }
}

LLD_QUIZZES: Dict[str, Any] = {
    "solid_quiz": {
        "title": "SOLID Principles Assessment",
        "questions": [
            {
                "id": "q1",
                "question": "A class 'Invoice' has methods: 'calculateTotal()', 'printInvoice()', and 'saveToDatabase()'. Which SOLID principle does this violate?",
                "options": [
                    "Open/Closed Principle",
                    "Single Responsibility Principle",
                    "Liskov Substitution Principle",
                    "Interface Segregation Principle"
                ],
                "correct_option": 1,
                "explanation": "The Single Responsibility Principle (SRP) states that a class should have only one reason to change. The Invoice class has three reasons to change: total calculation logic, print formatting, and database storage schema."
            },
            {
                "id": "q2",
                "question": "If you modify a base class method 'fly()' to throw an 'UnsupportedOperationException' in a subclass 'Penguin', which principle is violated?",
                "options": [
                    "Liskov Substitution Principle",
                    "Dependency Inversion Principle",
                    "Open/Closed Principle",
                    "Interface Segregation Principle"
                ],
                "correct_option": 0,
                "explanation": "Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program. Throwing a runtime exception for a base class capability violates this."
            },
            {
                "id": "q3",
                "question": "In a notification manager, passing 'EmailService' and 'SmsService' directly into the constructor of 'NotificationDispatcher' instead of passing a 'NotificationProvider' interface violates which principle?",
                "options": [
                    "Interface Segregation Principle",
                    "Dependency Inversion Principle",
                    "Single Responsibility Principle",
                    "Open/Closed Principle"
                ],
                "correct_option": 1,
                "explanation": "Dependency Inversion Principle (DIP) states that high-level modules should depend on abstractions (interfaces) rather than concrete implementations. Passing concrete classes directly violates DIP."
            }
        ]
    },
    "patterns_quiz": {
        "title": "Design Patterns Assessment",
        "questions": [
            {
                "id": "q4",
                "question": "Which design pattern is best suited when you need to add behaviors or decorators to an object dynamically at runtime without subclassing?",
                "options": [
                    "Factory Pattern",
                    "Decorator Pattern",
                    "Strategy Pattern",
                    "Observer Pattern"
                ],
                "correct_option": 1,
                "explanation": "The Decorator Pattern attaches additional responsibilities to an object dynamically at runtime, wrapping the original object."
            },
            {
                "id": "q5",
                "question": "You want to design a Payment Processor that can switch between Stripe, PayPal, and Adyen algorithms at runtime based on user preference. Which pattern is most appropriate?",
                "options": [
                    "Factory Method Pattern",
                    "Observer Pattern",
                    "Strategy Pattern",
                    "Adapter Pattern"
                ],
                "correct_option": 2,
                "explanation": "The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. This fits the requirement of swapping payment algorithms dynamically."
            }
        ]
    }
}
