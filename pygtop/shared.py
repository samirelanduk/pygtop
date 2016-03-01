class DatabaseLink:

    def __init__(self, json_data):
        self.json_data = json_data

        self.accession = json_data["accession"]
        self.database = json_data["database"]
        self.url = json_data["url"]
        self.species = None if json_data["species"] == "None" else json_data["species"]


    def __repr__(self):
        return "<%s link (%s)%s>" % (
         self.database,
         self.accession,
         " for " + self.species if self.species else ""
        )


class Precursor:

    def __init__(self, json_data):
        self.json_data = json_data

        self.precursor_id = json_data["precursorId"]
        self.gene_symbol = json_data["geneSymbol"]
        self.gene_name = json_data["geneName"]
        self.official_gene_id = json_data["officialGeneId"]
        self.protein_name = json_data["proteinName"]
        self.species = json_data["species"]
        self.synonyms = [s["name"] for s in json_data["synonyms"]]


    def __repr__(self):
        return "<Precursor %i (%s)>" % (self.precursor_id, self.protein_name)
