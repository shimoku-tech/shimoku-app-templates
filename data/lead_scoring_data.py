import pandas as pd
import numpy as np
import random

from typing import Dict

# for splitting the data
from sklearn.model_selection import train_test_split

# for model building
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer


def get_data(leads_data_path: str) -> Dict:
    # This data has been extracted from https://www.kaggle.com/datasets/ashydv/leads-dataset?resource=download
    leads = pd.read_csv(leads_data_path)

    # The data is just for demo purposes, so it hasn't been cleaned nor preprocessed much
    for col in leads.columns:
        if leads[col].dtype in ['object', 'datetime64[ns]']:
            leads[col] = leads[col].fillna(leads[col].mode()[0])
        elif leads[col].dtype in ['int64', 'float64', 'int32', 'float32']:
            leads[col] = leads[col].fillna(leads[col].mean())

    df_train, df_test = train_test_split(leads, test_size=0.2)

    y_train = df_train.Converted.values

    del df_train['Converted']
    del df_test['Converted']

    train_dic = df_train.to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    dv.fit(train_dic)

    X_train = dv.transform(train_dic)
    model = LogisticRegression(solver='liblinear')
    model.fit(X_train, y_train)

    test_dic = df_test.to_dict(orient='records')
    X_test = dv.transform(test_dic)
    test_prediction = model.predict_proba(X_test)[:, 1]

    #------------------ PREDICTION TABLE ------------------#
    binary_prediction_table = pd.DataFrame({
        'Lead ID': df_test['Lead Number'].values,
        'Probability': [round(100 * p, 2) for p in test_prediction],
        'Lead Scoring': ['High' if v > 0.75 else 'Medium' if v > 0.5 else 'Low' for v in test_prediction],
        # Get random set of two column names
        'Positive Impact Factors': [df_test.columns[np.random.randint(0, len(df_test.columns))] + ', ' +
                                    df_test.columns[np.random.randint(0, len(df_test.columns))]
                                    for i in range(len(test_prediction))],
        'Negative Impact Factors': [df_test.columns[np.random.randint(0, len(df_test.columns))] + ', ' +
                                    df_test.columns[np.random.randint(0, len(df_test.columns))]
                                    for i in range(len(test_prediction))],
    })

    #---------------- FEATURE IMPORTANCE -----------------#
    feature_importance = pd.DataFrame({
        'Feature': dv.feature_names_,
        'Importance (%)': model.coef_[0]
    })

    #----------------- GENERAL INDICATORS -----------------#
    total_occurrences = len(binary_prediction_table)
    high_conversion_occurrences = len(binary_prediction_table[binary_prediction_table['Lead Scoring'] == 'High'])
    moderate_conversion_occurrences = len(binary_prediction_table[binary_prediction_table['Lead Scoring'] == 'Medium'])
    low_conversion_occurrences = len(binary_prediction_table[binary_prediction_table['Lead Scoring'] == 'Low'])

    high_conversion = high_conversion_occurrences / total_occurrences
    moderate_conversion = moderate_conversion_occurrences / total_occurrences
    low_conversion = low_conversion_occurrences / total_occurrences

    prediction_indicators = [
        {
            'description': f"{100 * high_conversion:.2f}% of total {total_occurrences}",
            'title': 'High conversion (#)',
            'value': int(total_occurrences * high_conversion),
            'color': 'success',
            "target_path": 'www.shimoku.com',
        },
        {
            'description': '% of leads that will purchase within 120 days. Time saved: 80%',
            'title': 'High conversion expected',
            'value': '85%',
            'color': 'success',
            'variant': 'contained',
            "target_path": 'www.shimoku.com',
        },
        {
            'description': f"{100 * moderate_conversion:.2f}% of total {total_occurrences}",
            'title': 'Moderate conversion (#)',
            'value': int(total_occurrences * moderate_conversion),
            'color': 'warning',
            "target_path": 'www.shimoku.com',
        },
        {
            'description': '% of leads that will purchase within 120 days. Time saved: 70%',
            'title': 'Medium conversion expected',
            'value': '40%',
            'color': 'warning',
            'variant': 'contained',
            "target_path": 'www.shimoku.com',
        },
        {
            "description": f"{100 * low_conversion:.2f}% of total {total_occurrences}",
            "title": 'Low conversion (#)',
            "value": int(total_occurrences * low_conversion),
            "color": 'error',
        },
        {
            'description': '% of leads that will purchase within 120 days.',
            'title': 'Low conversion expected',
            'value': '5%',
            'color': 'error',
            'variant': 'contained',
        },
    ]

    #-------------- NEXT BEST PRODUCT INDICATORS --------------#
    product_recommendation_indicators = [
        {
            "color": "warning",
            "backgroundImage": "https://cdn-mx.comparabien.com/s3fs-public/styles/blog_full/public/field/image/seguro%20de%20auto.png?itok=be2ewUsJ",
            "variant": "outlined", "description": "", "title": "Autos (# prospects)",
            "align": "left", "value": int(len(test_prediction) * 0.4)
        },
        {
            "color": "warning", "backgroundImage": "https://cotizator.com/wp-content/uploads/2020/06/imagen.png",
            "variant": "outlined", "description": "", "title": "New life (# prospects)",
            "align": "left", "value": int(len(test_prediction) * 0.3)
        },
        {
            "color": "warning",
            "backgroundImage": "https://s3.amazonaws.com/s3.timetoast.com/public/uploads/photos/11439948/SALUD-P%C3%9ABLICA-Y-GESTI%C3%93N-SANITARIA.jpg",
            "variant": "outlined", "description": "", "title": "Health (# prospects)",
            "align": "left", "value": int(len(test_prediction) * 0.2)
        }
    ]

    #----------------- NEXT BEST PRODUCT TABLE -----------------#
    product_recommendation_table = binary_prediction_table[['Lead ID', 'Probability', 'Lead Scoring']].copy(deep=True)

    product_recommendation_table['Next Best Product'] = \
        [f"{['Autos', 'New life', 'Health', 'House'][np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1])]} " \
         f"({random.randint(1, 100)}%)"
         for i in range(len(product_recommendation_table))]

    #--------------------- RETURN THE DATA ---------------------#
    return {
        'binary_prediction_table': binary_prediction_table,
        'feature_importance': feature_importance,
        'total_occurrences': total_occurrences,
        'high_conversion_occurrences': high_conversion_occurrences,
        'moderate_conversion_occurrences': moderate_conversion_occurrences,
        'low_conversion_occurrences': low_conversion_occurrences,
        'high_conversion': high_conversion,
        'moderate_conversion': moderate_conversion,
        'low_conversion': low_conversion,
        'prediction_indicators': prediction_indicators,
        'product_recommendation_indicators': product_recommendation_indicators,
        'product_recommendation_table': product_recommendation_table,
    }
