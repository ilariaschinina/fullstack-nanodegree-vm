from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalogapp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Dumb user
user1 = User(email = "ilaria.schinina@gmail.com", token = None)

session.add(user1)
session.commit()

#Python section
category1 = Category(name = "Python", user = user1)

session.add(category1)
session.commit()

item1 = Item(title = "Learning Python", author= "Mark Lutz", description = "Get a comprehensive, in-depth introduction to the core Python language with this hands-on book. Based on author Mark Lutz’s popular training course, this updated fifth edition will help you quickly write efficient, high-quality code with Python. It’s an ideal way to begin, whether you’re new to programming or a professional developer versed in other languages.", category = category1)

session.add(item1)
session.commit()

item2 = Item(title = "Python Tricks: The Book", author= "Dan Bader", description = "With Python Tricks: The Book you’ll discover Python’s best practices and the power of beautiful & Pythonic code with simple examples and a step-by-step narrative.", category = category1)

session.add(item2)
session.commit()

item3 = Item(title = "Python Deep Learning", author= "Ivan Vasilev", description = "With the surge in artificial intelligence in applications catering to both business and consumer needs, deep learning is more important than ever for meeting current and future market demands. With this book, you'll explore deep learning, and learn how to put machine learning to use in your projects.", category = category1)

session.add(item3)
session.commit()

item4 = Item(title = "Python 3 Object-Oriented Programming", author= "Dusty Phillips", description = "This third edition of Python 3 Object-Oriented Programming fully explains classes, data encapsulation, and exceptions with an emphasis on when you can use each principle to develop well-designed software.", category = category1)

session.add(item4)
session.commit()

item5 = Item(title = "Machine Learning with Python", author= "Daniel Géron", description = "This book is going to help you understand the different approaches of machine learning and neural networks. It will guide you through the steps you need to build a machine learning model.", category = category1)

session.add(item5)
session.commit()



#JavaScript section
category2 = Category(name = "JavaScript", user = user1)

session.add(category2)
session.commit()

item6 = Item(title = "JavaScript and JQuery: Interactive Front-End Web Development", author= "Jon Duckett", description = "This full-color book adopts a visual approach to teaching JavaScript & jQuery, showing you how to make web pages more interactive and interfaces more intuitive through the use of inspiring code examples, infographics, and photography.", category = category2)

session.add(item6)
session.commit()

item7 = Item(title = "You Don't Know JS: Up and Going", author= "Kyle Simpson", description = "With the You Don’t Know JS book series, you’ll get a more complete understanding of JavaScript, including trickier parts of the language that many experienced JavaScript programmers simply avoid.", category = category2)

session.add(item7)
session.commit()

item8 = Item(title = "Eloquent JavaScript", author= "Marijn Haverbeke", description = "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.", category = category2)

session.add(item8)
session.commit()

item9 = Item(title = "JavaScript for impatient programmers", author= "Dr. Axel Rauschmayer", description = "This book makes JavaScript less challenging to learn for newcomers, by offering a modern view that is as consistent as possible.", category = category2)

session.add(item9)
session.commit()

item10 = Item(title = "JavaScript: The Definitive Guide", author= "JavaScript: The Definitive Guide", description = "Since 1996, JavaScript: The Definitive Guide has been the bible for JavaScript programmers―a programmer's guide and comprehensive reference to the core language and to the client-side JavaScript APIs defined by web browsers.", category = category2)

session.add(item10)
session.commit()

# Kotlin section
category3 = Category(name = "Kotlin", user = user1)

session.add(category3)
session.commit()

item11 = Item(title = "The Joy of Kotlin", author= "Pierre-Yves Saumont", description = "The Joy of Kotlin teaches you practical techniques to improve abstraction and design, to write comprehensible code, and to build maintainable bug-free applications.", category = category3)

session.add(item11)
session.commit()

item12 = Item(title = "Kotlin for Android Developers", author= "Antonio Leiva", description = "Recommended by both Google and Jetbrains, this book will guide through the process of learning all the new features that Java was missing, in an easy and fun way.", category = category3)

session.add(item12)
session.commit()

item13 = Item(title = "Programming Kotlin", author= "Venkat Subramaniam", description = "Learn to use the many features of this highly concise, fluent, elegant, and expressive statically typed language with easy-to-understand examples.", category = category3)

session.add(item13)
session.commit()

item14 = Item(title = "Hands-On Microservices with Kotlin", author= "Juan Antonio Medina Iglesias", description = "This book guides the reader in designing and implementing services, and producing production-ready, testable, lean code that's shorter and simpler than a traditional Java implementation.", category = category3)

session.add(item14)
session.commit()

item15 = Item(title = "Hands-on Design Patterns with Kotlin", author= "Alexey Soshin", description = "The mission of this book is to ease the adoption of design patterns in Kotlin and provide good practices for programmers.", category = category3)

session.add(item15)
session.commit()

# Go section
category4 = Category(name = "Go", user = user1)

session.add(category4)
session.commit()

item16 = Item(title = "Head First Go", author= "Jay McGavren", description = "Go makes it easy to build software that’s simple, reliable, and efficient. Andthis book makes it easy for programmers like you to get started.", category = category4)

session.add(item16)
session.commit()

item17 = Item(title = "Introducing Go: A Developer Resource", author= "Caleb Doxsey", description = "Perfect for beginners familiar with programming basics, this hands-on guide provides an easy introduction to Go, the general-purpose programming language from Google.", category = category4)

session.add(item17)
session.commit()

item18 = Item(title = "GO: GO Programming Language for Beginners", author= "GO Publishing", description = "This book is designed for software programmers with a need to understand the Go programming language from scratch.", category = category4)

session.add(item18)
session.commit()

item19 = Item(title = "Mastering Go", author= "Mihalis Tsoukalos", description = "Offering a compendium of Go, the book begins with an account of how Go has been implemented. You'll also benefit from an in-depth account of concurrency and systems and network programming imperative for modern-day native cloud development through the course of the book.", category = category4)

session.add(item19)
session.commit()

item20 = Item(title = "Hands-On GUI Application Development in Go", author= "Andrew Williams", description = "This guide to programming GUIs with Go 1.11 explores the various toolkits available, including UI, Walk, Shiny, and Fyne.", category = category4)

session.add(item20)
session.commit()


print("Done! Items added!")