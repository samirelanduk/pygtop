from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.interactions import Interaction
from pygtop.ligands import Ligand
from pygtop.targets import Target
import pygtop.exceptions as exceptions
import xml.etree.ElementTree as ElementTree

class InteractionTest(TestCase):

    def setUp(self):
        self.interaction_json = {
         "interactionId": 79397,
         "targetId": 1,
         "ligandAsTargetId": 0,
         "targetSpecies": "Human",
         "primaryTarget": False,
         "targetBindingSite": "",
         "ligandId": 7191,
         "ligandContext": "",
         "endogenous": False,
         "type": "Agonist",
         "action": "Agonist",
         "actionComment": "",
         "selectivity": "None",
         "concentrationRange": "-",
         "affinity": "7.2",
         "affinityType": "pKi",
         "originalAffinity": "6x10<sup>-8</sup>",
         "originalAffinityType": "Ki",
         "originalAffinityRelation": "",
         "assayDescription": "",
         "assayConditions": "",
         "useDependent": False,
         "voltageDependent": False,
         "voltage": "-",
         "physiologicalVoltage": False,
         "conciseView": False,
         "dataPoints": [],
         "refs": []
        }

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

        self.target_json = {
         "targetId": 1,
         "name": "5-HT<sub>1A</sub> receptor",
         "abbreviation": "5-HT",
         "systematicName": None,
         "type": "GPCR",
         "familyIds": [1],
         "subunitIds": [2, 3],
         "complexIds": [4]
        }


        self.pdb_json = [
         {
          "targetId" : 2,
          "ligandId" : 121,
          "endogenous" : False,
          "pdbCode" : "4IAQ",
          "description" : "Crystal structure of the chimeric protein of 5-HT1B-BRIL in complex with dihydroergotamine",
          "resolution" : 2.8,
          "species" : "Human",
          "refs" : []
         }, {
          "targetId" : 2,
          "ligandId" : 149,
          "endogenous" : False,
          "pdbCode" : "4IAR",
          "description" : "Crystal structure of the chimeric protein of 5-HT1B-BRIL in complex with ergotamine",
          "resolution" : 2.7,
          "species" : "Human",
          "refs" : []
         }, {
          "targetId" : 2,
          "ligandId" : 149,
          "endogenous" : False,
          "pdbCode" : "4xxx",
          "description" : "Crystal structure of the chimeric protein of 5-HT1B-BRIL in complex with ergotamine",
          "resolution" : 2.7,
          "species" : "Rat",
          "refs" : []
         }
        ]





class InteractionCreationTests(InteractionTest):

    def test_can_create_interaction(self):
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction.json_data, self.interaction_json)
        self.assertEqual(interaction._interaction_id, 79397)
        self.assertEqual(interaction._ligand_id, 7191)
        self.assertEqual(interaction._target_id, 1)
        self.assertEqual(interaction._species, "Human")
        self.assertEqual(interaction._primary_target, False)
        self.assertEqual(interaction._endogenous, False)
        self.assertEqual(interaction._interaction_type, "Agonist")
        self.assertEqual(interaction._action, "Agonist")
        self.assertEqual(interaction._affinity_low, 7.2)
        self.assertEqual(interaction._affinity_high, 7.2)
        self.assertEqual(interaction._affinity_type, "pKi")


    def test_can_process_affinity_range(self):
        self.interaction_json["affinity"] = "9.4 &ndash; 10.3"
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction._affinity_low, 9.4)
        self.assertEqual(interaction._affinity_high, 10.3)


    def test_can_process_affinity_range_with_median(self):
        self.interaction_json["affinity"] = "7.7 &ndash; 9.0 (median: 8.6)"
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction._affinity_low, 7.7)
        self.assertEqual(interaction._affinity_high, 9.0)


    def test_interaction_repr(self):
        interaction = Interaction(self.interaction_json)
        self.assertEqual(str(interaction), "<Interaction (7191 --> Human 1)>")



class InteractionPropertyTests(InteractionTest):

    def test_basic_property_methods(self):
        interaction = Interaction(self.interaction_json)
        self.assertIs(interaction._interaction_id, interaction.interaction_id())
        self.assertIs(interaction._ligand_id, interaction.ligand_id())
        self.assertIs(interaction._target_id, interaction.target_id())
        self.assertIs(interaction._species, interaction.species())
        self.assertIs(interaction._primary_target, interaction.primary_target())
        self.assertIs(interaction._endogenous, interaction.endogenous())
        self.assertIs(interaction._interaction_type, interaction.interaction_type())
        self.assertIs(interaction._action, interaction.action())
        self.assertIs(interaction._affinity_low, interaction.affinity_low())
        self.assertIs(interaction._affinity_high, interaction.affinity_high())
        self.assertIs(interaction._affinity_type, interaction.affinity_type())


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_ligand(self, mock_json_retriever):
        mock_json_retriever.return_value = self.ligand_json
        interaction = Interaction(self.interaction_json)
        ligand = interaction.ligand()
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.ligand_id(), self.ligand_json["ligandId"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_ligand_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction.ligand(), None)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        interaction = Interaction(self.interaction_json)
        target = interaction.target()
        self.assertIsInstance(target, Target)
        self.assertEqual(target.target_id(), self.target_json["targetId"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction.target(), None)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_gtop_pdbs(self, mock_json_retriever):
        mock_json_retriever.return_value = self.pdb_json
        self.interaction_json["ligandId"] = 149
        interaction = Interaction(self.interaction_json)
        pdbs = interaction.gtop_pdbs()
        self.assertEqual(pdbs, ["4IAR"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_gtop_pdbs_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction.gtop_pdbs(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_all_external_pdbs(self, mock_xml_retriever, mock_simple_retriever, mock_json_retriever):
        mock_simple_retriever.return_value = ElementTree.fromstring('''<?xml version='1.0' standalone='no' ?>
<smilesQueryResult smiles="NC(=O)C1=CC=CC=C1" search_type="4">
<ligandInfo>
<ligand structureId="2XG3" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
<ligand structureId="3A1I" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
</ligandInfo>
</smilesQueryResult>''')
        mock_xml_retriever.side_effect = [["1xxx", "3A1I"], ["4IAR"], ["2xxx"], ["4IAR", "3xxx"]]
        mock_json_retriever.side_effect = [
         self.ligand_json, # Create ligand
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has smiles
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use smiles
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has inchi
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use inchi
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has peptide code
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use peptide code
         self.target_json, # Make target
         [{"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"}]
        ]
        interaction = Interaction(self.interaction_json)
        pdbs = interaction.all_external_pdbs()
        self.assertEqual(pdbs, ["4IAR"])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_all_pdbs(self, mock_xml_retriever, mock_simple_retriever, mock_json_retriever):
        mock_simple_retriever.return_value = ElementTree.fromstring('''<?xml version='1.0' standalone='no' ?>
<smilesQueryResult smiles="NC(=O)C1=CC=CC=C1" search_type="4">
<ligandInfo>
<ligand structureId="2XG3" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
<ligand structureId="3A1I" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
</ligandInfo>
</smilesQueryResult>''')
        mock_xml_retriever.side_effect = [["1xxx", "3A1I"], ["4IAR"], ["2xxx"], ["3A1I", "3xxx"]]
        mock_json_retriever.side_effect = [
         self.ligand_json, # Create ligand
         [self.interaction_json],
         self.pdb_json,
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has smiles
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use smiles
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has inchi
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use inchi
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Check has peptide code
         {"smiles": "CCC", "inchi": "CCC", "oneLetterSeq": "CCC"}, # Use peptide code
         self.target_json, # Make target
         self.pdb_json,
         [{"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"}]
        ]
        interaction = Interaction(self.interaction_json)
        pdbs = interaction.all_pdbs()
        self.assertEqual(len(pdbs), 2)
        for code in ["3A1I", "4IAR"]:
            self.assertIn(code, pdbs)


'''import unittest
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.interactions import *
from pygtop.ligands import *
from pygtop.targets import *
from pygtop.gtop import *
from pygtop.exceptions import *

string = str

class InteractionTest(unittest.TestCase):

    def check_interaction_properties(self, interaction):
        str(interaction)
        self.assertIsInstance(interaction, Interaction)
        self.assertIsInstance(interaction.interaction_id, int)
        self.assertIsInstance(interaction._ligand_id, int)
        self.assertIsInstance(interaction._target_id, int)
        self.assertIsInstance(interaction.species, string)
        if interaction.affinity_value: self.assertIsInstance(
         interaction.affinity_range, tuple
        )
        for val in interaction.affinity_range:
            self.assertIsInstance(val, float)
        if interaction.affinity_value:
            self.assertIsInstance(interaction.affinity_value, float)
        if interaction.affinity_value:
            self.assertIsInstance(interaction.affinity_type, string)
        self.assertIsInstance(interaction.type, string)
        self.assertIsInstance(interaction.action, string)
        self.assertIsInstance(interaction.ligand_primary_target, bool)
        self.assertIsInstance(interaction.is_voltage_dependent, bool)
        if interaction.voltage_value:
            self.assertIsInstance(interaction.voltage_value, float)
        else:
            self.assertEqual(interaction.voltage_value, None)
        self.assertIsInstance(interaction.references, list)
        for ref in interaction.references:
            self.assertIsInstance(ref, string)
            self.assertEqual(ref[0], "(")


    def test_can_make_interaction(self):
        interaction_json = get_json_from_gtop("/targets/485/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)
        interaction_json = get_json_from_gtop("/targets/64/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)
        interaction_json = get_json_from_gtop("/targets/381/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)


    def test_interaction_can_get_ligand(self):
        interaction_json = get_json_from_gtop("/targets/1/interactions")[0]
        interaction = Interaction(interaction_json)
        ligand = interaction.get_ligand()
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.name, "frovatriptan")

        interaction._ligand_id = 0
        self.assertEqual(None, interaction.get_ligand())


    def test_interaction_can_get_target(self):
        interaction_json = get_json_from_gtop("/targets/1/interactions")[0]
        interaction = Interaction(interaction_json)
        target = interaction.get_target()
        self.assertIsInstance(target, Target)
        self.assertEqual(target.name, "5-HT<sub>1A</sub> receptor")

        species_target = interaction.get_species_target()
        self.assertIsInstance(species_target, SpeciesTarget)
        self.assertEqual(species_target.target.name, "5-HT<sub>1A</sub> receptor")

        interaction._target_id = 0
        self.assertEqual(None, interaction.get_target())


    def test_ligand_can_get_interactions(self):
        ligand = get_ligand_by_id(1)
        interactions = ligand.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._ligand_id, ligand.ligand_id)


    def test_ligand_can_get_specific_interaction(self):
        ligand = get_ligand_by_id(1)
        interaction = ligand.get_interaction_by_id(1)
        self.assertEqual(interaction.interaction_id, 1)
        self.assertRaises(
         NoSuchInteractionError,
         lambda: ligand.get_interaction_by_id(2)
        )


    def test_ligand_can_get_targets(self):
        ligand = get_ligand_by_id(1)
        targets = ligand.get_targets()
        self.assertGreater(len(targets), 0)
        for target in targets:
            self.assertIsInstance(target, Target)


    def test_ligand_can_get_species_targets(self):
        ligand = get_ligand_by_id(1)
        targets = ligand.get_species_targets()
        self.assertGreater(len(targets), 0)
        for target in targets:
            self.assertIsInstance(target, SpeciesTarget)


    def test_target_can_get_interactions(self):
        target = get_target_by_id(1)
        interactions = target.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._target_id, target.target_id)


    def test_target_can_get_specific_interaction(self):
        target = get_target_by_id(1)
        interaction = target.get_interaction_by_id(1)
        self.assertEqual(interaction.interaction_id, 1)
        self.assertRaises(
         NoSuchInteractionError,
         lambda: target.get_interaction_by_id(0)
        )


    def test_species_target_can_get_interactions(self):
        target = SpeciesTarget(1, "human")
        interactions = target.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._target_id, target.target_id)
            self.assertEqual(interaction.species.lower(), target.species.lower())


    def test_target_can_get_ligands(self):
        target = get_target_by_id(1)
        ligands = target.get_ligands()
        self.assertGreater(len(ligands), 0)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    def test_interactions_between(self):
        ligand = get_ligand_by_id(1)
        target = get_target_by_id(1)
        mutual = get_interactions_between(ligand, target)
        self.assertEqual(len(mutual), 1)



class InteractionPdbs(unittest.TestCase):

    def test_interaction_can_get_gtop_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        self.assertEqual(
         interaction.get_gtop_pdbs(),
         ["4IAQ"]
        )
        interaction = get_target_by_id(2).get_interaction_by_id(79398)
        self.assertEqual(
         interaction.get_gtop_pdbs(),
         []
        )


    def test_interaction_can_find_all_external_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        external_pdbs = interaction.find_all_external_pdbs()
        self.assertIsInstance(external_pdbs, list)
        self.assertGreaterEqual(len(external_pdbs), 1)


    def test_interaction_can_find_all_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        pdbs = interaction.find_all_pdbs()
        self.assertIsInstance(pdbs, list)
        self.assertGreaterEqual(len(pdbs), 1)






if __name__ == "__main__":
    unittest.main()'''
