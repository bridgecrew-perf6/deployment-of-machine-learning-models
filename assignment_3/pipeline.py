from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import preprocessors as pp
import config


titanic_pipe = Pipeline(steps=[
    # complete with the list of steps from the preprocessors file
    # and the list of variables from the config
    ('categorical_imputer', pp.CategoricalImputer(
        variables=config.CATEGORICAL_VARS)),

    ('missing indicator', pp.MissingIndicator(
        variables=config.NUMERICAL_VARS)),

    ('numerical_imputer', pp.NumericalImputer(
        variables=config.NUMERICAL_VARS)),

    ('cabin_variable', pp.ExtractFirstLetter(variables=config.CABIN)),

    ('rare_label_encoder', pp.RareLabelCategoricalEncoder(
        tol=0.05, variables=config.CATEGORICAL_VARS)),

    ('categorical_encoder', pp.CategoricalEncoder(
        variables=config.CATEGORICAL_VARS)),

    ('scaler', StandardScaler()),

    ('Linear_model', LogisticRegression(C=0.0005, random_state=0))
]
)
