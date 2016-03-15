Overview
--------

Ligands
~~~~~~~
The simplest way to create a ligand is via its GtoP ID:

    >>> import pygtop
    >>> my_drug = pygtop.get_ligand_by_id(5239)
    >>> my_drug.name
    'paracetamol'
    >>> my_drug.ligand_type
    'Synthetic organic'

Properties other than the most basic ones must be requested separately, as they
require their own HTTP request:

    >>> my_drug.request_molecular_properties()
    >>> my_drug.rotatable_bonds
    2
    >>> my_drug.molecular_weight
    151.0633286
    >>> my_drug.request_structural_properties()
    >>> my_drug.smiles
    'CC(=O)Nc1ccc(cc1)O'

Ligands can also be accessed by name, or at random:

    >>> pygtop.get_ligand_by_name('caffeine')
    <'caffeine' Ligand (Natural product)>
    >>> pygtop.get_random_ligand()
    <'3,5-dihydroxybenzoic acid' Ligand (Synthetic organic)>
    >>> pygtop.get_random_ligand(ligand_type='antibody')
    <'blinatumomab' Ligand (Antibody)>

You can get a list of ligands by either requesting all ligands, or providing a
query:

    >>> all_ligands = pygtop.get_all_ligands()
    >>> len(all_ligands) # There are 8,328 ligands as of March 2016
    8328
    >>> all_ligands[0]
    <'10,10-difluoro TXA<sub>2</sub>' Ligand (Synthetic organic)>
    >>> query = {"type": "Approved", "molWeightGt": 50, "molWeightLt": 200}
    >>> ligands = pygtop.get_ligands_by(query) # Get approved ligands between 50 and 200 Da
    >>> len(ligands)
    104