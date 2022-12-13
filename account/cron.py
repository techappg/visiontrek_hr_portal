from hr.models import Punch



def my_scedule():
    a = Punch.objects.filter(punch_out='')
    a.punch_out = None
    