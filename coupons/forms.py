from django import forms


# форма для ввода кода купона
class CouponApplyForm(forms.Form):
    code = forms.CharField()