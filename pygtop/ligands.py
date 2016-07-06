"""Contains ligand-specific objects and functions."""

from collections import Counter
from . import gtop
from . import pdb
from .interactions import Interaction, get_interaction_by_id
from .exceptions import NoSuchLigandError
from .shared import DatabaseLink, strip_html

def get_ligand_by_id(ligand_id):
    """Returns a Ligand object of the ligand with the given ID.

    :param int ligand_id: The GtoP ID of the Ligand desired.
    :rtype: :py:class:`Ligand`
    :raises: :class:`.NoSuchLigandError` if no such ligand exists in the database"""

    if not isinstance(ligand_id, int):
        raise TypeError("ligand_id must be int, not '%s'" % str(ligand_id))
    json_data = gtop.get_json_from_gtop("ligands/%i" % ligand_id)
    if json_data:
        return Ligand(json_data)
    else:
        raise NoSuchLigandError("There is no ligand with ID %i" % ligand_id)


def get_all_ligands():
    """Returns a list of all ligands in the Guide to PHARMACOLOGY database. This
    can take a few seconds.

    :returns: list of :py:class:`Ligand` objects"""

    json_data = gtop.get_json_from_gtop("ligands")
    return [Ligand(l) for l in json_data]


def get_ligands_by(criteria):
    """Get all ligands which specify the criteria dictionary.

    :param dict criteria: A dictionary of `field=value` pairs. See the\
     `GtoP ligand web services page <http://www.guidetopharmacology.org/\
     webServices.jsp#ligands>`_ for key/value pairs which can be supplied.
    :returns: list of :py:class:`Ligand` objects."""

    if not isinstance(criteria, dict):
        raise TypeError("criteria must be dict, not '%s'" % str(criteria))

    search_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    json_data = gtop.get_json_from_gtop("ligands?%s" % search_string)
    if json_data:
        return [Ligand(l) for l in json_data]
    else:
        return []


def get_ligand_by_name(name):
    """Returns the ligand which matches the name given.

    :param str name: The name of the ligand to search for. Note that synonyms \
    will not be searched.
    :rtype: :py:class:`Ligand`
    :raises:  :class:`.NoSuchLigandError` if no such ligand exists in the database."""

    if not isinstance(name, str):
        raise TypeError("name must be str, not '%s'" % str(name))
    ligands = get_ligands_by({"name": name})
    if ligands:
        return ligands[0]
    else:
        raise NoSuchLigandError("There is no ligand with name %s" % name)



def get_ligands_by_smiles(smiles, search_type="exact", cutoff=0.8):
    """Search for ligands by SMILES string.

    :param str smiles: The SMILES string to search with.
    :param str search_type: The type of search. Viable options are ``"exact"``, \
    ``"substructure"`` or ``"similarity"``.
    :param float cutoff: If performing a similarity search, this is the cutoff \
    used for similarity. The default is 0.8 and the maximum is 1.
    :returns: list of :py:class:`Ligand` objects."""

    if not isinstance(smiles, str):
        raise TypeError("smiles must be str, not '%s'" % str(smiles))
    if not isinstance(search_type, str):
        raise TypeError("search_type must be str, not '%s'" % str(search_type))
    if search_type not in ["exact", "substructure", "similarity"]:
        raise ValueError("'%s' is not a valud search type" % search_type)
    if not isinstance(cutoff, int) and not isinstance(cutoff, float):
        raise TypeError("cutoff must be numeric, not '%s'" % str(cutoff))
    if not 0 <= cutoff <= 1:
        raise ValueError("cutoff must be between 0 and 1, not %s" % (str(cutoff)))

    query = "ligands/%s?smiles=%s%s" % (
     search_type,
     smiles,
     ("&similarityGt=%i" % (cutoff * 100)) if search_type == "similarity" else ""
    )
    json_data = gtop.get_json_from_gtop(query)
    if json_data:
        return [Ligand(l) for l in json_data]
    else:
        return []



class Ligand:

    def __init__(self, json_data):
        self.json_data = json_data
        self._ligand_id = json_data["ligandId"]
        self._name = json_data["name"]
        self._abbreviation = json_data["abbreviation"] if json_data["abbreviation"] else None
        self._inn = json_data["inn"]
        self._ligand_type = json_data["type"]
        self._species = json_data["species"]
        self._radioactive = json_data["radioactive"]
        self._labelled = json_data["labelled"]
        self._approved = json_data["approved"]
        self._withdrawn = json_data["withdrawn"]
        self._approval_source = json_data["approvalSource"]
        self._subunit_ids = json_data["subunitIds"]
        self._complex_ids = json_data["complexIds"]
        self._prodrug_ids = json_data["prodrugIds"]
        self._active_drug_ids = json_data["activeDrugIds"]


    def __repr__(self):
        return "<Ligand %i (%s)>" % (self._ligand_id, self._name)


    def ligand_id(self):
        return self._ligand_id


    @strip_html
    def name(self):
        return self._name


    @strip_html
    def abbreviation(self):
        return self._abbreviation


    @strip_html
    def inn(self):
        return self._inn


    def ligand_type(self):
        return self._ligand_type


    def species(self):
        return self._species


    def radioactive(self):
        return self._radioactive


    def labelled(self):
        return self._labelled


    def approved(self):
        return self._approved


    def withdrawn(self):
        return self._withdrawn


    @strip_html
    def approval_source(self):
        return self._approval_source


    def subunit_ids(self):
        return self._subunit_ids


    def subunits(self):
        return [get_ligand_by_id(id_) for id_ in self._subunit_ids]


    def complex_ids(self):
        return self._complex_ids


    def complexes(self):
        return [get_ligand_by_id(id_) for id_ in self._complex_ids]


    def prodrug_ids(self):
        return self._prodrug_ids


    def prodrugs(self):
        return [get_ligand_by_id(id_) for id_ in self._prodrug_ids]


    def active_drug_ids(self):
        return self._active_drug_ids


    def active_drugs(self):
        return [get_ligand_by_id(id_) for id_ in self._active_drug_ids]


    def iupac_name(self):
        return self._get_structure_json().get("iupacName")


    def smiles(self):
        return self._get_structure_json().get("smiles")


    def inchi(self):
        return self._get_structure_json().get("inchi")


    def inchi_key(self):
        return self._get_structure_json().get("inchiKey")


    def one_letter_sequence(self):
        return self._get_structure_json().get("oneLetterSeq")


    def three_letter_sequence(self):
        return self._get_structure_json().get("threeLetterSeq")


    def post_translational_modifications(self):
        return self._get_structure_json().get("postTranslationalModifications")


    def chemical_modifications(self):
        return self._get_structure_json().get("chemicalModifications")


    def hydrogen_bond_acceptors(self):
        return self._get_molecular_json().get("hydrogenBondAcceptors")


    def hydrogen_bond_donors(self):
        return self._get_molecular_json().get("hydrogenBondDonors")


    def rotatable_bonds(self):
        return self._get_molecular_json().get("rotatableBonds")


    def topological_polar_surface_area(self):
        return self._get_molecular_json().get("topologicalPolarSurfaceArea")


    def molecular_weight(self):
        return self._get_molecular_json().get("molecularWeight")


    def log_p(self):
        return self._get_molecular_json().get("logP")


    def lipinski_rules_broken(self):
        return self._get_molecular_json().get("lipinskisRuleOfFive")


    @strip_html
    def synonyms(self):
        return [synonym["name"] for synonym in self._get_synonym_json()]


    def general_comments(self):
        return self._get_comments_json().get("comments")


    def bioactivity_comments(self):
        return self._get_molecular_json().get("bioactivityComments")


    def clinical_use_comments(self):
        return self._get_molecular_json().get("clinicalUse")


    def mechanism_of_action_comments(self):
        return self._get_molecular_json().get("mechanismOfAction")


    def absorption_and_distribution_comments(self):
        return self._get_molecular_json().get("absorptionAndDistribution")


    def metabolism_comments(self):
        return self._get_molecular_json().get("metabolism")


    def elimination_comments(self):
        return self._get_molecular_json().get("elimination")


    def population_pharmacokinetics_comments(self):
        return self._get_molecular_json().get("populationPharmacokinetics")


    def organ_function_impairments_comments(self):
        return self._get_molecular_json().get("organFunctionImpairment")


    def mutations_and_pathophysiology_comments(self):
        return self._get_molecular_json().get("mutationsAndPathophysiology")


    def database_links(self):
        return [DatabaseLink(link_json) for link_json in self._get_database_json()]


    def interactions(self):
        return [Interaction(interaction_json) for interaction_json in self._get_interactions_json()]


    get_interaction_by_id = get_interaction_by_id
    """Returns an Interaction object of a given ID belonging to the ligand.

    :param int interaction_id: The interactions's ID.
    :rtype: :py:class:`.Interaction`
    :raises: :class:`.NoSuchInteractionError`: if no such interaction exists in the database."""


    def targets(self):
        """Returns a list of all targets which this ligand interacts with.

        :returns: list of :py:class:`.Target` objects"""

        targets = []
        for interaction in self.interactions():
            target = interaction.target()
            if target not in targets:
                targets.append(target)
        return targets


    @pdb.ask_about_molecupy
    def gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this ligand.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        pdbs = []
        for interaction in self.interactions():
            for pdb in interaction.gtop_pdbs():
                if pdb not in pdbs:
                    pdbs.append(pdb)
        return pdbs


    @pdb.ask_about_molecupy
    def smiles_pdbs(self, search_type="exact"):
        """Queries the RSCB PDB database with the ligand's SMILES string.

        :param str search_type: The type of search to run - whether exact matches\
        only should be returned.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.smiles():
            xml = pdb.query_rcsb("smilesQuery", {
             "smiles": self.smiles(),
             "search_type": search_type
            })
            if xml:
                ligand_elements = list(xml[0])
                return [element.attrib["structureId"] for element in ligand_elements]
            else:
                return []
        else:
            return []


    @pdb.ask_about_molecupy
    def inchi_pdbs(self):
        """Queries the RSCB PDB database with the ligand's InChI string.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.inchi():
            results = pdb.query_rcsb_advanced("ChemCompDescriptorQuery", {
             "descriptor": self.inchi(),
             "descriptorType": "InChI"
            })
            return results if results else []
        else:
            return []


    @pdb.ask_about_molecupy
    def name_pdbs(self, comparator="equals"):
        """Queries the RSCB PDB database with the ligand's name.

        :param str comparator: The type of search to run - whether exact matches\
        only should be returned, or substrings etc.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        results = pdb.query_rcsb_advanced("ChemCompNameQuery", {
         "comparator": comparator.title(),
         "name": self.name(),
         "polymericType": "Any"
        })
        return results if results else []


    @pdb.ask_about_molecupy
    def sequence_pdbs(self):
        """Queries the RSCB PDB database with the ligand's amino acid sequence,\
        if that ligand is a peptide.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.one_letter_sequence():
            results = pdb.query_rcsb_advanced("SequenceQuery", {
             "sequence": self.one_letter_sequence(),
             "eCutOff": "0.01",
             "searchTool": "blast",
             "sequenceIdentityCutoff": "100"
            })
            return results if results else []
        else:
            return []


    @pdb.ask_about_molecupy
    def all_external_pdbs(self):
        """Queries the RSCB PDB database by all parameters.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.smiles_pdbs() +
         self.inchi_pdbs() +
         self.name_pdbs() +
         self.sequence_pdbs()
        ))


    @pdb.ask_about_molecupy
    def all_pdbs(self):
        """Get a list of PDB codes using all means available - annotated and
        external.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.gtop_pdbs() +
         self.all_external_pdbs()
        ))


    def find_in_pdb_by_smiles(self, molecupy_pdb):
        if self.smiles():
            formula = Counter([char.upper() for char in self.smiles()
             if char.isalpha() and char.upper() != "H"])
            for molecule in molecupy_pdb.model.small_molecules:
                if molecule.get_formula() == formula:
                    return molecule


    def find_in_pdb_by_name(self, molecupy_pdb):
        if self.name():
            for molecule in molecupy_pdb.model.small_molecules:
                molecule_name = molecupy_pdb.data_file.het_names.get(molecule.molecule_name)
                if molecule_name and self.name().lower() == molecule_name.lower():
                    return molecule


    def find_in_pdb_by_mass(self, molecupy_pdb):
        if self.molecular_weight():
            molecules = sorted(
             list(molecupy_pdb.model.small_molecules),
             key=lambda k: abs(k.get_mass() - self.molecular_weight())
            )
            if molecules and -40 < (molecules[0].get_mass() - self.molecular_weight()) < 40:
                return molecules[0]


    def find_in_pdb_by_peptide_string(self, molecupy_pdb):
        if self.one_letter_sequence():
            for chain in molecupy_pdb.model.chains:
                if self.one_letter_sequence() in chain.get_sequence_string() and 0.9 <= (
                 len(self.one_letter_sequence()) / len(chain.get_sequence_string())
                ) <= 1:
                    return chain


    def _get_structure_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/structure" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_molecular_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/molecularProperties" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_synonym_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/synonyms" % self._ligand_id
        )
        return json_object if json_object else []


    def _get_comments_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/comments" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_database_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/databaseLinks" % self._ligand_id
        )
        return json_object if json_object else []


    def _get_interactions_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/interactions" % self._ligand_id
        )
        return json_object if json_object else []
