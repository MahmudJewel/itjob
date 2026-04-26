from enum import Enum as PythonEnum

class UserRole(str, PythonEnum):
    USER = "user"
    ADMIN = "admin"
    EDITOR = "editor"

class QuestionType(str, PythonEnum):
    MCQ = "mcq"
    DESCRIPTIVE = "descriptive"
    TRUE_FALSE = "true_false"

