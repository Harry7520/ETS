from django.urls import path
from ETS_app.views import *

urlpatterns =[
    path('c_home/', C_home, name="c_home"),
    path('m_dashboard/', M_dashboard, name="m_dashboard"),
    path('t_home/', T_home , name="c_home"),
    path('m_service/add/', M_service_add,),
    path('m_service/list/', M_service_list,),
    path('search_by/',search_by),
    path('search_by1/',search_by1),
    path('search_by2/',search_by2),
    path('search_by3/',search_by3),
    path('search_by4/',search_by4),
    path('search_by5/',search_by5),
    path('search_by6/',search_by6),
    path('search_by7/',search_by7),
    path('search_by8/',search_by8),
    path('m_service/detail/<int:post_id>/',M_service_detail),
    path('m_service/delete/<int:post_id>/',M_service_delete),
    path('m_service/edit/<int:post_id>/',M_service_edit),
    path('m_customer/list/',M_customer_list),
    path('m_technician/list/',M_technician_list),
    path('m_technician/register/list/',M_technician_register_list),
    path('m_technician/detail/<int:post_id>/',M_technician_detail),
    path('m_technician/delete/<str:post_e>/',M_technician_delete),
    path('m_technician/register/delete/<str:post_e>/',M_technician_register_delete),
    path('m_technician/employee/<int:id>/',M_technician_employee),
    path('m_employee/list/',M_employee_list),
    path('m_employee/register/list/',M_employee_register_list),
    path('m_employee/delete/<str:post_e>/',M_employee_delete),
    path('m_employee/register/delete/<str:post_e>/',M_employee_register_delete),
    path('m_employee/employee/<int:id>/',M_employee_employee),
    path('m_service/category/',M_service_category),
    path('m_service/category/delete/<int:post_id>/',M_service_category_delete),
    path('m_technician/occupation/',M_technician_occupation),
    path('m_technician/occupation/delete/<int:post_id>/',M_technician_occupation_delete),
    path('m_order/list',M_order_list),
    path('m_order/detail/<int:post_id>/',M_order_detail),
    path('m_order/delete/<int:post_id>/',M_order_delete),
    path('m_technician/review/',M_technician_review),
    path('m_customer/review/',M_customer_review),
    path('m_review/detail/<int:id>/',M_review_detail),
    path('m_review/delete/<int:id>/',M_review_delete),
    path('c_service/category/view/', C_service_category_view, name="service_category_view"),
    path('c_service/category/<str:ser>/', C_service_category),
    path('c_technician/',C_technician),
    path('c_profile/edit/<int:id>/', C_profile_edit),
    path('c_account/delete/<str:post_e>/',C_account_delete),
    path('c_technician/select/<int:post_id>/', C_technician_select),
    path('c_order/create/<int:post_id>/<int:t_id>/',C_order_create),
    path('c_order/list/<str:post_e>/',C_order_list),
    path('c_order/detail/<int:post_id>/',C_order_detail),
    path('c_order/delete/<int:id>/',C_order_delete),
    path('c_review/create/',C_review_create),
    path('t_technician/',T_technician),
    path('t_review/create/',T_review_create),
    path('t_profile/edit/<int:id>/', T_profile_edit),
    path('t_order/list/<str:post_e>/',T_order_list),
    path('t_order/detail/<int:post_id>/',T_order_detail),
    path('t_order/delete/<int:id>/',T_order_delete),
    path('t_order/approve/<int:id>/',T_order_approve),
    path('t_order/reject/<int:id>/',T_order_reject),
    path('t_order/finish/<int:id>/',T_order_finish),
]