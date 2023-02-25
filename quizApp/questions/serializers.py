from rest_framework import serializers
from .models import MCQ, Textual

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = '__all__' #['question_text','image','total_options','option1','option2','option3','option4','correct_option_number']

class TextualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textual
        fields = '__all__' #['question_text','image','answer_text']