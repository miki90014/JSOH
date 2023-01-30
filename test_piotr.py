import json
import os

import pytest
from Model.example_data import avg, sorter, load_unfilled_protocols, filter_list


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 1, 1, 1], 1),
        ([], 0),
        ([5.5, 5.5, 0, 5.5, 0], 5.5),
        ([0, 0, 0, 0, 0], 0),
        ([1, 2, 3], 2),
        ([5.5, 5, 4, 3.5], 4.5)
    ]
)
def test_avg(numbers, expected):
    assert avg(numbers) == expected


@pytest.fixture()
def protocols():
    return load_unfilled_protocols(os.getcwd() + '\\TestFiles')


def test_load_unfilled_protocols(protocols):
    assert len(protocols) == 1
    assert protocols['02']['Nr protokołu'] == '02'


@pytest.mark.parametrize(
    "mark, expected",
    [
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'wzorowa'
            }}], 5),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'dostateczna'
            }}], 2),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'inna'
            }}], 0),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': ''
            }}], 0),
    ]
)
def test_sorter(mark, expected):
    assert sorter(mark) == expected


@pytest.mark.parametrize(
    'dict_to_filter, filter_by, expected',
    [
        ({
            1: {
                'Semestr': 'Lato 2022/2023'
            },
            2: {
                'Semestr': 'Lato 2022/2023'
            },
            3: {
                'Semestr': 'Zima 2022/2023'
            }
        }, 'Lato 2022/2023', {
                                1: {
                                    'Semestr': 'Lato 2022/2023'
                                },
                                2: {
                                    'Semestr': 'Lato 2022/2023'
                                }}),

        ({
            1: {
                'Semestr': 'Lato 2022/2023'
            },
            2: {
                'Semestr': 'Lato 2022/2023'
            },
            3: {
                'Semestr': 'Zima 2022/2023'
            }
        }, 'Zima 2022/2023', {
                                3: {
                                    'Semestr': 'Zima 2022/2023'
                                }}),

        ({}, 'Zima 2022/2023', {}),

        ({
            1: {
                'Semestr': 'Lato 2022/2023'
            },
            2: {
                'Semestr': 'Lato 2022/2023'
            },
            3: {
                'Semestr': 'Zima 2022/2023'
            }
        }, 'Inne', {})
    ]
)
def test_filter_list(dict_to_filter, filter_by, expected):
    assert filter_list(dict_to_filter, filter_by) == expected
