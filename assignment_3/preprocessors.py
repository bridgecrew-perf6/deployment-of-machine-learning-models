import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


# Add binary variable to indicate missing values
class MissingIndicator(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # to accommodate sklearn pipeline functionality
        return self

    def transform(self, X):
        # add indicator
        X = X.copy()

        for var in self.variables:
            X[var + '_NA'] = np.where(X[var].isnull(), 1, 0)

        return X

# categorical missing value imputer


class CategoricalImputer(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # we need the fit statement to accommodate the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()

        X[self.variables] = X[self.variables].fillna('Missing')

        return X


# Numerical missing value imputer
class NumericalImputer(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # persist mode in a dictionary
        self.imputer_dict_ = {}
        for var in self.variables:
            self.imputer_dict_[var] = X[var].mode()[0]

        return self

    def transform(self, X):

        X = X.copy()

        for var in self.variables:
            X[var].fillna(self.imputer_dict_[var], inplace=True)

        return X


# Extract first letter from string variable
class ExtractFirstLetter(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()

        for variable in self.variables:
            X[variable] = X[variable].str[0]

        return X

# frequent label categorical encoder


class RareLabelCategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, tol=0.05, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

        self.tol = tol

    def fit(self, X, y=None):

        # persist frequent labels in dictionary
        self.encoder_dict_ = {}

        for variable in self.variables:
            prop = X[variable].value_counts() / len(X)
            self.encoder_dict_[variable] = prop[prop >=
                                                self.tol].index.tolist()
        return self

    def transform(self, X):
        X = X.copy()

        for variable in self.variables:
            X[variable] = np.where(X[variable].isin(
                self.encoder_dict_[variable]), X[variable], 'Rare')

        return X


# string to numbers categorical encoder
class CategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):

        # HINT: persist the dummy variables found in train set
        self.dummies = pd.get_dummies(
            X[self.variables], drop_first=True).columns

        return self

    def transform(self, X):
        # encode labels
        X = X.copy()
        # get dummies
        X = pd.concat(
            [X, pd.get_dummies(X[self.variables], drop_first=True)], axis=1)

        # drop original variables

        X.drop(labels=self.variables, axis=1, inplace=True)

        # add missing dummies if any

        missing_vars = [var for var in self.dummies if var not in X.columns]

        if missing_vars:
            for var in missing_vars:
                X[var] = 0

        return X