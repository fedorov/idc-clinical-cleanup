from clinical_forms_util import clinical_forms_util
import pandas as pd
import unittest
from pathlib import Path
import os
import json


class TestFormReader(unittest.TestCase):

    def setUp(self):
        super().setUp()
        file_path = Path(__file__)
        self._test_dir = file_path.parent.parent.joinpath(
            'data',
            'test_files'
        )

    @staticmethod
    def _get_item_by_key(dict, key, value):
        item = [i for i in dict if i[key]==value][0]
        return item

    def test_init(self):
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
    
    def test_parse_row(self):
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
        one_row = parser.get_dataframe("AI").iloc[0]
        ref_json = {'form_element_number': '1', 'variable_name': 'Aie1', 'variable_label': 'TIME POINT OF IMAGES BEING REVIEWED', 'data_type': 'List', 'values': [{'option_code': '10', 'option_description': 'Week 64'}]}
        assert(parser._parse_entry_from_row(one_row) == ref_json)

    def test_parse(self):        
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
        parser.parse_dictionaries()

        for name in parser.get_dictionary_names():
            form_desc = parser.get_dictionary_desc(name)
            if form_desc is None:
                print(f"Description is blank for {name}")
            assert(form_desc is not None)

    def test_parse_AI(self):
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
        parser.parse_dictionary("AI")

        A1_dict = parser.get_dictionary("AI")
        print(A1_dict)
        assert(len(A1_dict) == 9)

        # confirm size of list is as expected
        Aie1 = [i for i in A1_dict if i["variable_name"]=="Aie1"][0]
        assert(len(Aie1["values"])==7)
        #clinical_forms_util.process_clinical_dict("test", df)

    def test_parse_all(self):
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
        parser.parse_dictionaries()

    def test_print_AI(self):
        parser = clinical_forms_util.DictionaryReader(os.path.join(self._test_dir, "ACRIN_6677 Data Dictionary.xlsx"))
        AI_dict = parser.parse_dictionary("AI")

        print("---")
        #AI_dict = parser.get_dictionary("AI")
        print(json.dumps(AI_dict, indent=2))

        print("---")
        AI_df = parser.get_dataframe("AI")
        print(AI_df)
        
