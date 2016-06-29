from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.ligands import Ligand

class LigandTest(TestCase):

    def setUp(self):
        self.ligand_json = {
         "ligandId": 1,
         "name": "flesinoxan",
         "abbreviation": "flexo",
         "inn": "flesinoxan",
         "type": "Synthetic organic",
         "species": None,
         "radioactive": False,
         "labelled": True,
         "approved": True,
         "withdrawn": False,
         "approvalSource": "FDA (1997)",
         "subunitIds": [2, 3],
         "complexIds": [5],
         "prodrugIds": [7],
         "activeDrugIds": [9, 10]
        }



class LigandCreationTests(LigandTest):

    def test_can_create_ligand(self):
        ligand = Ligand(self.ligand_json)
        self.assertEqual(ligand.json_data, self.ligand_json)
        self.assertEqual(ligand._ligand_id, 1)
        self.assertEqual(ligand._name, "flesinoxan")
        self.assertEqual(ligand._abbreviation, "flexo")
        self.assertEqual(ligand._inn, "flesinoxan")
        self.assertEqual(ligand._ligand_type, "Synthetic organic")
        self.assertEqual(ligand._species, None)
        self.assertEqual(ligand._radioactive, False)
        self.assertEqual(ligand._labelled, True)
        self.assertEqual(ligand._approved, True)
        self.assertEqual(ligand._withdrawn, False)
        self.assertEqual(ligand._approval_source, "FDA (1997)")
        self.assertEqual(ligand._subunit_ids, [2, 3])
        self.assertEqual(ligand._complex_ids, [5])
        self.assertEqual(ligand._prodrug_ids, [7])
        self.assertEqual(ligand._active_drug_ids, [9, 10])


    def test_missing_abbreviation_is_none(self):
        self.ligand_json["abbreviation"] = ""
        ligand = Ligand(self.ligand_json)
        self.assertEqual(ligand._abbreviation, None)


    def test_ligand_repr(self):
        ligand = Ligand(self.ligand_json)
        self.assertEqual(str(ligand), "<Ligand 1 (flesinoxan)>")



class LigandPropertyTests(LigandTest):

    def test_basic_property_methods(self):
        ligand = Ligand(self.ligand_json)
        self.assertIs(ligand._ligand_id, ligand.ligand_id())
        self.assertIs(ligand._name, ligand.name())
        self.assertIs(ligand._abbreviation, ligand.abbreviation())
        self.assertIs(ligand._inn, ligand.inn())
        self.assertIs(ligand._ligand_type, ligand.ligand_type())
        self.assertIs(ligand._species, ligand.species())
        self.assertIs(ligand._radioactive, ligand.radioactive())
        self.assertIs(ligand._labelled, ligand.labelled())
        self.assertIs(ligand._approved, ligand.approved())
        self.assertIs(ligand._withdrawn, ligand.withdrawn())
        self.assertIs(ligand._approval_source, ligand.approval_source())
        self.assertIs(ligand._subunit_ids, ligand.subunit_ids())
        self.assertIs(ligand._complex_ids, ligand.complex_ids())
        self.assertIs(ligand._prodrug_ids, ligand.prodrug_ids())
        self.assertIs(ligand._active_drug_ids, ligand.active_drug_ids())


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_structural_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = {
         "iupacName": "2,3-dihydro-1,4-benzodioxin",
         "smiles": "OC[C@H]1COc2c(O1)cccc2N1CCN(CC1)CCNC(=O)c1ccc(cc1)F",
         "inchi": "InChI=1S/C22H26FN3O4/c23-17-6-4-16(5-7-17)22(28)24-8-9-25-10",
         "inchiKey": "NYSDRDDQELAVKP-SFHVURJKSA-N",
         "oneLetterSeq": "ILK",
         "threeLetterSeq": "Ile-Leu-Lys",
         "postTranslationalModifications": "Glycosylation",
         "chemicalModifications": "Methylation"
        }
        ligand = Ligand(self.ligand_json)

        self.assertEqual(ligand.iupac_name(), "2,3-dihydro-1,4-benzodioxin")
        self.assertEqual(
         ligand.smiles(),
         "OC[C@H]1COc2c(O1)cccc2N1CCN(CC1)CCNC(=O)c1ccc(cc1)F"
        )
        self.assertEqual(
         ligand.inchi(),
         "InChI=1S/C22H26FN3O4/c23-17-6-4-16(5-7-17)22(28)24-8-9-25-10"
        )
        self.assertEqual(ligand.inchi_key(), "NYSDRDDQELAVKP-SFHVURJKSA-N")
        self.assertEqual(ligand.one_letter_sequence(), "ILK")
        self.assertEqual(ligand.three_letter_sequence(), "Ile-Leu-Lys")
        self.assertEqual(
         ligand.post_translational_modifications(),
         "Glycosylation"
        )
        self.assertEqual(ligand.chemical_modifications(), "Methylation")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_structural_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        ligand = Ligand(self.ligand_json)
        self.assertIs(ligand.iupac_name(), None)
        self.assertIs(ligand.smiles(), None)
        self.assertIs(ligand.inchi(), None)
        self.assertIs(ligand.inchi_key(), None)
        self.assertIs(ligand.one_letter_sequence(), None)
        self.assertIs(ligand.three_letter_sequence(), None)
        self.assertIs(ligand.post_translational_modifications(), None)
        self.assertIs(ligand.chemical_modifications(), None)

'''import unittest
from unittest.mock import patch
import molecupy
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.ligands import *
from pygtop.exceptions import *




    def check_ligand_molecular_properties(self, ligand):
        if ligand.hydrogen_bond_acceptors:
            self.assertIsInstance(ligand.hydrogen_bond_acceptors, int)
        if ligand.hydrogen_bond_donors:
            self.assertIsInstance(ligand.hydrogen_bond_donors, int)
        if ligand.rotatable_bonds:
            self.assertIsInstance(ligand.rotatable_bonds, int)
        if ligand.topological_polar_surface_area:
            self.assertIsInstance(ligand.topological_polar_surface_area, float)
        if ligand.molecular_weight:
            self.assertIsInstance(ligand.molecular_weight, float)
        if ligand.log_p:
            self.assertIsInstance(ligand.log_p, float)
        if ligand.lipinksi_rules_broken:
            self.assertIsInstance(ligand.lipinksi_rules_broken, int)


    def check_ligand_database_properties(self, ligand):
        self.assertIsInstance(ligand.database_links, list)
        for link in ligand.database_links:
            self.assertIsInstance(link, pygtop.DatabaseLink)
            if link.accession: self.assertIsInstance(link.accession, string)
            if link.database: self.assertIsInstance(link.database, string)
            if link.url: self.assertIsInstance(link.url, string)
            if link.species: self.assertIsInstance(link.species, string)


    def check_ligand_synonym_properties(self, ligand):
        self.assertIsInstance(ligand.synonyms, list)
        for synonym in ligand.synonyms:
            self.assertIsInstance(synonym, string)
            self.assertGreater(len(synonym), 0)


    def check_ligand_comment_properties(self, ligand):
        self.assertIsInstance(ligand.general_comments, string)
        self.assertIsInstance(ligand.bioactivity_comments, string)
        self.assertIsInstance(ligand.clinical_use_comments, string)
        self.assertIsInstance(ligand.mechanism_of_action_comments, string)
        self.assertIsInstance(ligand.absorption_and_distribution_comments, string)
        self.assertIsInstance(ligand.metabolism_comments, string)
        self.assertIsInstance(ligand.elimination_comments, string)
        self.assertIsInstance(ligand.population_pharmacokinetics_comments, string)
        self.assertIsInstance(ligand.organ_function_impairments_comments, string)
        self.assertIsInstance(ligand.mutations_and_pathophysiology_comments, string)


    def check_ligand_precursor_properties(self, ligand):
        self.assertIsInstance(ligand.precursors, list)
        for precursor in ligand.precursors:
            self.assertIsInstance(precursor, pygtop.Precursor)
            self.assertIsInstance(precursor.precursor_id, int)
            self.assertIsInstance(precursor.gene_symbol, string)
            self.assertIsInstance(precursor.gene_name, string)
            self.assertIsInstance(precursor.official_gene_id, string)
            self.assertIsInstance(precursor.protein_name, string)
            self.assertIsInstance(precursor.species, string)
            self.assertIsInstance(precursor.synonyms, list)
            for synonym in precursor.synonyms:
                self.assertIsInstance(synonym, string)
                self.assertGreater(len(synonym), 0)



class SingleLigands(LigandTest):

    def test_can_get_single_ligand(self):
        ligand = get_ligand_by_id(1)
        self.assertIsInstance(ligand, Ligand)
        if sys.version_info[0] == 2:
            self.assertRegexpMatches(ligand.__repr__(), r'<.+>')
        else:
            self.assertRegex(ligand.__repr__(), r'<.+>')


    def test_invalid_ligand_exception(self):
        self.assertRaises(NoSuchLigandError, lambda: get_ligand_by_id(0))


    def test_basic_ligand_properties(self):
        ligand = get_ligand_by_id(4890)
        self.check_ligand_basic_properties(ligand)


    def test_structural_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_structural_properties()
        self.check_ligand_structural_properties(ligand)


    def test_invalid_attribute_access(self):
        ligand = get_ligand_by_id(4890)
        self.assertRaises(PropertyNotRequestedYetError, lambda: ligand.smiles)
        self.assertRaises(AttributeError, lambda: ligand.xxx)
        ligand.request_structural_properties()
        self.assertIsInstance(ligand.smiles, string)
        self.assertRaises(AttributeError, lambda: ligand.xxx)


    def test_molecular_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_molecular_properties()
        self.check_ligand_molecular_properties(ligand)


    def test_database_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_database_properties()
        self.check_ligand_database_properties(ligand)


    def test_synonym_properties(self):
        ligand = get_ligand_by_id(1)
        ligand.request_synonym_properties()
        self.check_ligand_synonym_properties(ligand)


    def test_comment_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_comment_properties()
        self.check_ligand_comment_properties(ligand)


    def test_precursor_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_precursor_properties()
        self.check_ligand_precursor_properties(ligand)


    def test_all_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_all_properties()
        self.check_ligand_structural_properties(ligand)
        self.check_ligand_molecular_properties(ligand)
        self.check_ligand_database_properties(ligand)
        self.check_ligand_synonym_properties(ligand)
        self.check_ligand_comment_properties(ligand)
        self.check_ligand_precursor_properties(ligand)


    def test_can_get_subunits(self):
        ligand = get_ligand_by_id(1158)
        self.check_ligand_basic_properties(ligand)
        subunits = ligand.get_subunits()
        self.assertGreater(len(subunits), 0)
        for subunit in subunits:
            self.assertIsInstance(subunit, Ligand)


    def test_can_get_complexes(self):
        ligand = get_ligand_by_id(5537)
        self.check_ligand_basic_properties(ligand)
        complexes = ligand.get_complexes()
        self.assertGreater(len(complexes), 0)
        for complex in complexes:
            self.assertIsInstance(complex, Ligand)


    def test_can_get_prodrugs(self):
        ligand = get_ligand_by_id(7258)
        self.check_ligand_basic_properties(ligand)
        prodrugs = ligand.get_prodrugs()
        self.assertGreater(len(prodrugs), 0)
        for prodrug in prodrugs:
            self.assertIsInstance(prodrug, Ligand)


    def test_can_get_active_drugs(self):
        ligand = get_ligand_by_id(96)
        self.check_ligand_basic_properties(ligand)
        active_drugs = ligand.get_active_drugs()
        self.assertGreater(len(active_drugs), 0)
        for active_drug in active_drugs:
            self.assertIsInstance(active_drug, Ligand)



class MultiLigands(LigandTest):

    def test_can_get_all_ligands(self):
        ligands = get_all_ligands()
        self.assertIsInstance(ligands, list)
        self.assertGreater(len(ligands), 5000)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    def test_can_get_ligand_by_name(self):
        ligand = pygtop.get_ligand_by_name("APIGENIN")
        self.assertIsInstance(ligand, Ligand)
        self.assertRaises(
         NoSuchLigandError,
         lambda: pygtop.get_ligand_by_name("paracetamoxyfrusebendroneomycin")
        )


    def test_can_search_ligands(self):
        criteria = {
         "type": "Approved",
         "molWeightGt": 50,
         "molWeightLt": 200
        }
        ligands = pygtop.get_ligands_by(criteria)
        self.assertIsInstance(ligands, list)
        self.assertGreaterEqual(len(ligands), 104)


    def test_can_get_random_ligand(self):
        ligand = pygtop.get_random_ligand()
        self.assertIsInstance(ligand, Ligand)
        ligand = pygtop.get_random_ligand(ligand_type="peptide")
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.ligand_type.lower(), "peptide")
        self.assertRaises(
         NoSuchTypeError,
         lambda: pygtop.get_random_ligand(ligand_type="xxx")
        )


    def test_can_search_ligand_by_exact_smiles(self):
        ligands = pygtop.get_ligands_by_smiles(
         "CC(CN(C)C)CN1c2ccccc2Sc2ccccc12"
        )
        self.assertIsInstance(ligands, list)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)
        self.assertEqual(
         pygtop.get_ligands_by_smiles(
          "NNNNNNNNNNNNNNNNN"
         ),
         []
        )


    def test_can_search_ligand_by_smiles_substructure(self):
        ligands = pygtop.get_ligands_by_smiles(
         "CC(CN(C)C)CN1c2ccccc2Sc2ccccc12",
         search_type="substructure"
        )
        self.assertIsInstance(ligands, list)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)
        self.assertEqual(
         pygtop.get_ligands_by_smiles(
          "NNNNNNNNNNNNNNNNN",
          search_type="substructure"
         ),
         []
        )


    def test_can_search_ligand_by_smiles_similarity(self):
        ligands = pygtop.get_ligands_by_smiles(
         "CC(CN(C)C)CN1c2ccccc2Sc2ccccc12",
         search_type="similarity",
         cutoff=0.6
        )
        self.assertIsInstance(ligands, list)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)
        self.assertEqual(
         pygtop.get_ligands_by_smiles(
          "NNNNNNNNNNNNNNNNN",
          search_type="similarity",
          cutoff=0.6
         ),
         []
        )


class LigandPdbs(unittest.TestCase):

    def test_ligand_can_get_gtop_pdbs(self):
        ligand = get_ligand_by_id(121)
        self.assertEqual(
         ligand.get_gtop_pdbs(),
         ["4IAQ"]
        )
        ligand = get_ligand_by_id(1)
        self.assertEqual(
         ligand.get_gtop_pdbs(),
         []
        )


    def test_ligand_can_find_pdbs_by_smiles(self):
        ligand = get_ligand_by_name("paracetamol")
        smiles_pdbs = ligand.find_pdbs_by_smiles()
        self.assertIsInstance(smiles_pdbs, list)
        self.assertGreaterEqual(len(smiles_pdbs), 1)


    def test_ligand_can_find_pdbs_by_inchi(self):
        ligand = get_ligand_by_name("paracetamol")
        inchi_pdbs = ligand.find_pdbs_by_inchi()
        self.assertIsInstance(inchi_pdbs, list)
        self.assertGreaterEqual(len(inchi_pdbs), 1)


    def test_ligand_can_find_pdbs_by_name(self):
        ligand = get_ligand_by_name("ergotamine")
        name_pdbs = ligand.find_pdbs_by_name()
        self.assertIsInstance(name_pdbs, list)
        self.assertGreaterEqual(len(name_pdbs), 1)


    def test_ligand_can_find_pdbs_by_sequence(self):
        ligand = get_ligand_by_name("ergotamine")
        name_pdbs = ligand.find_pdbs_by_name()
        self.assertIsInstance(name_pdbs, list)
        self.assertGreaterEqual(len(name_pdbs), 1)


    def test_ligand_can_find_all_external_pdbs(self):
        ligand = get_ligand_by_name("ergotamine")
        external_pdbs = ligand.find_all_external_pdbs()
        self.assertIsInstance(external_pdbs, list)
        self.assertGreaterEqual(len(external_pdbs), 1)


    def test_ligand_can_find_all_pdbs(self):
        ligand = get_ligand_by_id(3802)
        sequence_pdbs = ligand.find_pdbs_by_sequence()
        self.assertIsInstance(sequence_pdbs, list)
        self.assertGreaterEqual(len(sequence_pdbs), 1)


class LigandInMolecupyTests(unittest.TestCase):

    def setUp(self):
        self.ligand = get_ligand_by_name("dihydroergotamine")
        self.pdb = molecupy.get_pdb_remotely("4IAQ")


    def test_can_identify_ligand_based_on_smiles(self):
        het = self.ligand.find_in_pdb_by_smiles(self.pdb)
        self.assertEqual(het.molecule_name, "2GM")


    def test_can_identify_ligand_based_on_name(self):
        het = self.ligand.find_in_pdb_by_name(self.pdb)
        self.assertEqual(het.molecule_name, "2GM")


    def test_can_identify_ligand_based_on_mass(self):
        het = self.ligand.find_in_pdb_by_mass(self.pdb)
        self.assertEqual(het.molecule_name, "2GM")


    def test_can_identify_ligand_based_on_mass(self):
        self.ligand.request_structural_properties()
        self.ligand.one_letter_sequence = "HKLHQLQDS"
        pdb = molecupy.get_pdb_remotely("2YJA")
        chain = self.ligand.find_in_pdb_by_peptide_string(pdb)
        self.assertEqual(chain.chain_id, "A")


if __name__ == "__main__":
    unittest.main()'''
