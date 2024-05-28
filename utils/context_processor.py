from ETS_app.models import Customer,Technician,Main

def customer(request):
    try:
        c_user = Customer.objects.get(email=request.user.email)
        return {'c_user':c_user}
    except Exception:
        return {'c_user':None}
    
def technician(request):
    try:
        t_user = Technician.objects.get(email=request.user.email)
        return {'t_user':t_user}
    except Exception:
        return {'t_user':None}

def main(request):
    try:
        m_user = Main.objects.get(email=request.user.email)
        return {'m_user':m_user}
    except Exception:
        return {'m_user':None}
    