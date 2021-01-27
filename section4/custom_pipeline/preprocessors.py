from itertools import groupby
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score


class Pipeline:

    def __init__(self, target, categorical_to_impute, year_variable,
                 numerical_to_impute, numerical_log, categorical_encode,
                 features, test_size=0.1, random_state=0,
                 rare_percentage=0.01, ref_variable='YrSold'):

        # data sets
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        # engineering parameters (to be learn from data)
        self.imputing_dict = {}
        self.frequent_category_dict = {}
        self.encoding_dict = {}

        # models
        self.scaler = MinMaxScaler()
        self.model = Lasso(alpha=0.005, random_state=random_state)

        # groups of variables to engineer
        self.target = target
        self.year_variable = year_variable
        self.categorical_to_impute = categorical_to_impute
        self.numerical_to_impute = numerical_to_impute
        self.numerical_log = numerical_log
        self.categorical_encode = categorical_encode
        self.features = features

        # more parameters
        self.test_size = test_size
        self.random_state = random_state
        self.percentage = rare_percentage
        self.rev_variable = ref_variable

    # ======================== functions to learn parameters from train set

    def find_imputation_replacements(self):
        '''find value to be used from imputation'''
        for variable in self.numerical_to_impute:
            replacement = self.X_train[variable].mode()[0]
            self.imputing_dict[variable] = replacement

        return self

    def find_frequent_categories(self):
        '''find list of frequent categories in categorical variables'''

        for variable in self.categorical_encode:
            percentage = self.X_train.groupby(
                variable)[self.target].count() / len(self.X_train)
            self.frequent_category_dict[variable] = percentage[percentage >
                                                               self.percentage].index

        return self

    def find_categorical_mappings(self):
        ''' create category to integer mappings for categorical encoding'''

        for variable in self.categorical_encode:
            ordered_labels = self.X_train.groupby(
                [variable])[self.target].mean().sort_values().index

            ordinal_labels = {k: i for i, k in enumerate(ordered_labels, 0)}

            self.encoding_dict[variable] = ordinal_labels

        return self

    # ==================== functions to transform data

    def capture_elapsed_years(self, df):
        ''' capture time difference between variable and reference variable'''

        df = df.copy()
        df[self.year_variable] = df[self.year_variable] - df[self.ref_variable]

        return df

    def remove_rare_labels(self, df):
        ''' group infrequent labels in group Rare'''
        df = df.copy()

        for variable in self.categorical_encode:
            df[variable] = np.where(df[variable].isin(
                self.frequent_category_dict[variable]), df[variable], 'Rare')

        return df

    def encode_categorical_variables(self, df):
        ''' replace categories by numbers in categorical variables'''

        df = df.copy()

        for variable in self.categorical_encode:
            df[variable] = df[variable].map(
                self.frequent_category_dict[variable])

        return df