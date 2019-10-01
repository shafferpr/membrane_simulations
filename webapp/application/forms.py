from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, InputRequired




class StructuresForm(FlaskForm):
    label = StringField('label', validators=[DataRequired()])
    npores = IntegerField('nPores',validators=[Optional()], filters=[lambda x : 15 if x is None else x])
    boxSize = FloatField('boxSize',validators=[Optional()], filters=[lambda x : 50 if x is None else x])
    lowerC = FloatField('lowerC', validators=[Optional()], filters=[lambda x : 15 if x is None else x])
    upperC = FloatField('upperC', validators=[Optional()], filters=[lambda x : 35 if x is None else x])
    poreSizeCeiling = FloatField('poreSizeCeiling', validators=[Optional()], filters=[lambda x : 5 if x is None else x])
    poreSizeFloor = FloatField('poreSizeFloor', validators=[Optional()], filters=[lambda x : 0.5 if x is None else x])
