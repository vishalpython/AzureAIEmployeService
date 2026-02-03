from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'Employee'


    def ready(self):
        import Employee.signals
