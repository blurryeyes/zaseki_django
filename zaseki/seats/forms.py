# from dataclasses import fields
from django import forms

from .models import Layout, Seat


class LayoutForm(forms.ModelForm):
    class Meta:
        model = Layout
        fields = ['layout_name', 'layout_width', 'layout_height',
                  'seat_width', 'seat_height', 'font_size', 'opacity',
                  'non_sitting_seat_color', 'sitting_seat_color', 'notice', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        # form.as_tableのときにコロンを表示させない
        # https://www.maytisk.com/django-form-no-colon/