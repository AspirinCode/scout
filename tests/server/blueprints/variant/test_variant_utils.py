from scout.server.blueprints.variant.utils import (
    predictions,
    frequencies,
    is_affected,
    evaluation,
    transcript_str,
    frequency,
    end_position,
    add_panel_specific_gene_info,
    update_transcripts_information,
    clinsig_human,
)


def test_clinsig_human():
    ## GIVEN a variant with clinsig info
    var_obj = {
        "clnsig": [
            {
                "value": "Likely benign",
                "accession": 335067,
                "revstat": "criteria_provided, single submitter",
            }
        ]
    }
    ## WHEN getting the clinsig
    clinsigs = clinsig_human(var_obj)
    ## THEN assert there where no objects returned
    clinsig_obj = next(clinsigs)
    assert clinsig_obj["human"] == "Likely benign"
    assert (
        clinsig_obj["link"] == "https://www.ncbi.nlm.nih.gov/clinvar/variation/335067"
    )


def test_clinsig_human_no_accession():
    ## GIVEN a variant with clinsig info wothout accession number
    var_obj = {
        "clnsig": [
            {"value": "Likely benign", "revstat": "criteria_provided, single submitter"}
        ]
    }
    ## WHEN getting the clinsig
    clinsigs = clinsig_human(var_obj)
    ## THEN assert there where no objects returned since we skip those wothout accession
    i = 0
    for i, obj in enumerate(clinsigs, 1):
        pass
    assert i == 0


def test_clinsig_human_no_clnsig():
    ## GIVEN a variant with clinsig info
    var_obj = {}
    ## WHEN getting the clinsig
    clinsigs = clinsig_human(var_obj)
    ## THEN assert there where no objects returned
    i = 0
    for i, obj in enumerate(clinsigs, 1):
        pass
    assert i == 0


def test_update_transcripts_information_disease_associated():
    ## GIVEN a variants gene with info about disease associated tx
    variant_gene = {
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "disease_associated_no_version": ["NM_001193301"],
        "transcripts": [
            {
                "transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "protein_id": "ENSP00000347117",
                "sift_prediction": "unknown",
                "polyphen_prediction": "unknown",
                "swiss_prot": "Q9H3S1",
                "biotype": "protein_coding",
                "functional_annotations": ["intron_variant"],
                "region_annotations": ["intronic"],
                "intron": "10/14",
                "strand": "+",
                "coding_sequence_name": "c.1135-4554G>A",
                "is_canonical": False,
            }
        ],
    }
    assert variant_gene["transcripts"][0].get("is_disease_associated") is None

    hgnc_gene = {
        "_id": {"$oid": "5c8112e701f54818d3cbc04a"},
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "ensembl_id": "ENSG00000196189",
        "chromosome": "1",
        "start": 156117157,
        "end": 156147543,
        "length": 30386,
        "description": "semaphorin 4A",
        "aliases": ["SEMA4A", "SEMAB", "CORD10", "SemB", "FLJ12287"],
        "primary_transcripts": ["NM_022367"],
        "inheritance_models": ["AD", "AR"],
        "entrez_id": 64218,
        "omim_id": 607292,
        "ucsc_id": "uc001fnl.4",
        "uniprot_ids": ["Q9H3S1"],
        "vega_id": "OTTHUMG00000014042",
        "pli_score": 0.615371620982326,
        "incomplete_penetrance": False,
        "build": "37",
        "transcripts": [
            {
                "_id": {"$oid": "5c81130601f54818d3cc0514"},
                "ensembl_transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "chrom": "1",
                "start": 156119810,
                "end": 156147535,
                "is_primary": True,
                "refseq_id": "NM_001193301",
                "refseq_identifiers": ["NM_001193301"],
                "build": "37",
                "length": 27725,
            }
        ],
    }

    variant_obj = {}
    ## WHEN updating the transcripts information
    update_transcripts_information(
        variant_gene, hgnc_gene, variant_obj, genome_build=None
    )
    ## THEN assert that the tx on variant gene has is disease associated
    assert variant_gene["transcripts"][0].get("is_disease_associated") is True


def test_update_transcripts_information_refseq_id():
    ## GIVEN a variants gene with no primary transcript
    variant_gene = {
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "transcripts": [
            {
                "transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "protein_id": "ENSP00000347117",
                "sift_prediction": "unknown",
                "polyphen_prediction": "unknown",
                "swiss_prot": "Q9H3S1",
                "biotype": "protein_coding",
                "functional_annotations": ["intron_variant"],
                "region_annotations": ["intronic"],
                "intron": "10/14",
                "strand": "+",
                "coding_sequence_name": "c.1135-4554G>A",
                "is_canonical": False,
            }
        ],
    }
    assert variant_gene["transcripts"][0].get("refseq_id") is None

    hgnc_gene = {
        "_id": {"$oid": "5c8112e701f54818d3cbc04a"},
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "ensembl_id": "ENSG00000196189",
        "chromosome": "1",
        "start": 156117157,
        "end": 156147543,
        "length": 30386,
        "description": "semaphorin 4A",
        "aliases": ["SEMA4A", "SEMAB", "CORD10", "SemB", "FLJ12287"],
        "primary_transcripts": ["NM_022367"],
        "inheritance_models": ["AD", "AR"],
        "entrez_id": 64218,
        "omim_id": 607292,
        "ucsc_id": "uc001fnl.4",
        "uniprot_ids": ["Q9H3S1"],
        "vega_id": "OTTHUMG00000014042",
        "pli_score": 0.615371620982326,
        "incomplete_penetrance": False,
        "build": "37",
        "transcripts": [
            {
                "_id": {"$oid": "5c81130601f54818d3cc0514"},
                "ensembl_transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "chrom": "1",
                "start": 156119810,
                "end": 156147535,
                "is_primary": True,
                "refseq_id": "NM_001193301",
                "refseq_identifiers": ["NM_001193301"],
                "build": "37",
                "length": 27725,
            }
        ],
    }

    variant_obj = {}
    ## WHEN updating the transcripts information
    update_transcripts_information(
        variant_gene, hgnc_gene, variant_obj, genome_build=None
    )
    ## THEN assert that the tx on variant gene has been given a ref seq id
    assert variant_gene["transcripts"][0].get("refseq_id") == "NM_001193301"
    ## THEN assert that the variant obj has refseq ids
    assert variant_obj["has_refseq"] is True
    ## THEN assert that the list of primary transcripts has been added
    assert len(variant_gene["primary_transcripts"]) == 1


def test_update_transcripts_information_refseq_id():
    ## GIVEN a variants gene with no primary transcript
    variant_gene = {
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "transcripts": [
            {
                "transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "protein_id": "ENSP00000347117",
                "sift_prediction": "unknown",
                "polyphen_prediction": "unknown",
                "swiss_prot": "Q9H3S1",
                "biotype": "protein_coding",
                "functional_annotations": ["intron_variant"],
                "region_annotations": ["intronic"],
                "intron": "10/14",
                "strand": "+",
                "coding_sequence_name": "c.1135-4554G>A",
                "is_canonical": False,
            }
        ],
    }
    assert variant_gene["transcripts"][0].get("refseq_id") is None

    hgnc_gene = {
        "_id": {"$oid": "5c8112e701f54818d3cbc04a"},
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "ensembl_id": "ENSG00000196189",
        "chromosome": "1",
        "start": 156117157,
        "end": 156147543,
        "length": 30386,
        "description": "semaphorin 4A",
        "aliases": ["SEMA4A", "SEMAB", "CORD10", "SemB", "FLJ12287"],
        "primary_transcripts": ["NM_022367"],
        "inheritance_models": ["AD", "AR"],
        "entrez_id": 64218,
        "omim_id": 607292,
        "ucsc_id": "uc001fnl.4",
        "uniprot_ids": ["Q9H3S1"],
        "vega_id": "OTTHUMG00000014042",
        "pli_score": 0.615371620982326,
        "incomplete_penetrance": False,
        "build": "37",
        "transcripts": [
            {
                "_id": {"$oid": "5c81130601f54818d3cc0514"},
                "ensembl_transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "chrom": "1",
                "start": 156119810,
                "end": 156147535,
                "is_primary": True,
                "refseq_id": "NM_001193301",
                "refseq_identifiers": ["NM_001193301"],
                "build": "37",
                "length": 27725,
            }
        ],
    }

    variant_obj = {}
    ## WHEN updating the transcripts information
    update_transcripts_information(
        variant_gene, hgnc_gene, variant_obj, genome_build=None
    )
    ## THEN assert that the tx on variant gene has been given a ref seq id
    assert variant_gene["transcripts"][0].get("refseq_id") == "NM_001193301"
    ## THEN assert that the variant obj has refseq ids
    assert variant_obj["has_refseq"] is True
    ## THEN assert that the list of primary transcripts has been added
    assert len(variant_gene["primary_transcripts"]) == 1


def test_update_transcripts_information_is_primary():
    ## GIVEN a variants gene with no primary transcript
    variant_gene = {
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "transcripts": [
            {
                "transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "protein_id": "ENSP00000347117",
                "sift_prediction": "unknown",
                "polyphen_prediction": "unknown",
                "swiss_prot": "Q9H3S1",
                "biotype": "protein_coding",
                "functional_annotations": ["intron_variant"],
                "region_annotations": ["intronic"],
                "intron": "10/14",
                "strand": "+",
                "coding_sequence_name": "c.1135-4554G>A",
                "is_canonical": False,
            }
        ],
    }
    assert variant_gene["transcripts"][0].get("is_primary") is None

    hgnc_gene = {
        "_id": {"$oid": "5c8112e701f54818d3cbc04a"},
        "hgnc_id": 10729,
        "hgnc_symbol": "SEMA4A",
        "ensembl_id": "ENSG00000196189",
        "chromosome": "1",
        "start": 156117157,
        "end": 156147543,
        "length": 30386,
        "description": "semaphorin 4A",
        "aliases": ["SEMA4A", "SEMAB", "CORD10", "SemB", "FLJ12287"],
        "primary_transcripts": ["NM_022367"],
        "inheritance_models": ["AD", "AR"],
        "entrez_id": 64218,
        "omim_id": 607292,
        "ucsc_id": "uc001fnl.4",
        "uniprot_ids": ["Q9H3S1"],
        "vega_id": "OTTHUMG00000014042",
        "pli_score": 0.615371620982326,
        "incomplete_penetrance": False,
        "build": "37",
        "transcripts": [
            {
                "_id": {"$oid": "5c81130601f54818d3cc0514"},
                "ensembl_transcript_id": "ENST00000355014",
                "hgnc_id": 10729,
                "chrom": "1",
                "start": 156119810,
                "end": 156147535,
                "is_primary": True,
                "refseq_id": "NM_001193301",
                "refseq_identifiers": ["NM_001193301"],
                "build": "37",
                "length": 27725,
            }
        ],
    }

    variant_obj = {}
    ## WHEN updating the transcripts information
    update_transcripts_information(
        variant_gene, hgnc_gene, variant_obj, genome_build=None
    )
    ## THEN assert that the tx on variant gene has been labeled primary transcript
    assert variant_gene["transcripts"][0].get("is_primary") is True


def test_update_transcripts_information(hgnc_gene, variant_gene):
    ## GIVEN a hgnc gene, a variant gene and a variant object
    variant_obj = {}
    assert "primary_transcripts" not in variant_gene
    ## WHEN updating the transcript information for the variant gene
    update_transcripts_information(variant_gene, hgnc_gene, variant_obj)
    ## THEN assert the function has completed without errors
    assert "primary_transcripts" in variant_gene


def test_add_panel_specific_gene_info_disease_tx():
    ## GIVEN some panel genes and a gene object
    panel_info = [
        {"hgnc_id": 100, "symbol": "AAA", "disease_associated_transcripts": ["NM001.1"]}
    ]
    ## WHEN parsing the info
    panel_info = add_panel_specific_gene_info(panel_info)
    ## THEN assert no info is returned
    assert panel_info.get("mosaicism") is False
    assert panel_info.get("disease_associated_no_version") == set(["NM001"])
    assert panel_info.get("disease_associated_transcripts") == ["NM001.1"]


def test_add_panel_specific_gene_info_mosaic():
    ## GIVEN some panel genes and a gene object
    panel_info = [{"hgnc_id": 100, "symbol": "AAA", "mosaicism": True}]
    ## WHEN parsing the info
    panel_info = add_panel_specific_gene_info(panel_info)
    ## THEN assert no info is returned
    assert panel_info["mosaicism"] is True


def test_add_panel_specific_gene_info_empty():
    ## GIVEN some panel genes and a gene object
    panel_info = []
    ## WHEN fetching the panel specific info
    panel_info = add_panel_specific_gene_info(panel_info)
    ## THEN assert no info is returned
    for entry in panel_info:
        assert not panel_info[entry]


def test_add_panel_specific_gene_info():
    ## GIVEN some panel genes and a gene object
    panel_info = [{"hgnc_id": 100, "symbol": "AAA"}]
    ## WHEN parsing the info
    panel_info = add_panel_specific_gene_info(panel_info)
    ## THEN assert no info is returned
    for entry in panel_info:
        assert not panel_info[entry]


def test_end_position_old_indel():
    ## GIVEN a small indel
    var = {"alternative": "TCTC", "reference": "AGAG", "position": 100}
    ## WHEN getting the end position
    end = end_position(var)
    ## THEN assert that the end position is 10 bases
    assert end == 103


def test_end_position_indel():
    ## GIVEN a single nucleotide variant
    var = {"alternative": "TCTCTCTCACA", "reference": "t", "position": 100}
    ## WHEN getting the end position
    end = end_position(var)
    ## THEN assert that the end position is 10 bases
    assert end == 110


def test_end_position_snv():
    ## GIVEN a single nucleotide variant
    var = {"alternative": "A", "reference": "C", "position": 100}
    ## WHEN getting the end position
    end = end_position(var)
    ## THEN assert that the end position is correct
    assert end == 100


def test_frequency_rare():
    ## GIVEN a variant which is uncommon gnomad frequency
    var = {"gnomad_frequency": 0.001}
    ## WHEN converting frequencies to string
    freq_str = frequency(var)
    ## THEN assert that the variant is common
    assert freq_str == "rare"


def test_frequency_uncommon():
    ## GIVEN a variant which is uncommon gnomad frequency
    var = {"gnomad_frequency": 0.03}
    ## WHEN converting frequencies to string
    freq_str = frequency(var)
    ## THEN assert that the variant is common
    assert freq_str == "uncommon"


def test_frequency_common():
    ## GIVEN a variant with a common gnomad frequency
    var = {"gnomad_frequency": 0.5}
    ## WHEN converting frequencies to string
    freq_str = frequency(var)
    ## THEN assert that the variant is common
    assert freq_str == "common"


def test_tx_str():
    ## GIVEN a transcript object with an exon change and a gene name
    gene_name = "NCDN"
    tx_obj = {
        "exon": "8/8",
        "refseq_id": "NM_001014839",
        "coding_sequence_name": "c.*156C>T",
    }
    ## WHEN Converting the information to a string for the template
    change_str = transcript_str(tx_obj, gene_name)

    ## THEN assert the string is on expected format
    assert change_str == "NCDN:NM_001014839:exon8:c.*156C>T:NA"


def test_evaluation(real_variant_database):
    ## GIVEN a populated database
    store = real_variant_database
    var = store.variant_collection.find_one()
    user = store.user_collection.find_one()
    institute = store.institute_collection.find_one()
    case = store.case_collection.find_one()
    link = "a link"
    classification = "pathogenic"

    ## WHEN adding an evaluation to the database
    store.submit_evaluation(
        var, user, institute, case, link, classification=classification
    )

    eval_obj = store.acmg_collection.find_one()
    assert eval_obj["institute_id"] == institute["_id"]
    assert "institute" not in eval_obj

    updated_eval = evaluation(store, eval_obj)
    ## THEN assert that the correct information was added to display evaluation
    assert updated_eval["institute"] == institute


def test_is_affected_healthy():
    ## GIVEN a variant and a case
    case_obj = {"individuals": [{"individual_id": "1", "phenotype": 1}]}
    variant_obj = {"samples": [{"sample_id": "1"}]}
    ## WHEN converting affection status to string
    is_affected(variant_obj, case_obj)
    ## THEN assert that affection status is healthy
    updated_sample = variant_obj["samples"][0]
    assert "is_affected" in updated_sample
    assert updated_sample["is_affected"] == False


def test_is_affected_affected():
    ## GIVEN a variant and a case
    case_obj = {"individuals": [{"individual_id": "1", "phenotype": 2}]}
    variant_obj = {"samples": [{"sample_id": "1"}]}
    ## WHEN converting affection status to string
    is_affected(variant_obj, case_obj)
    ## THEN assert that affection status is healthy
    updated_sample = variant_obj["samples"][0]
    assert updated_sample["is_affected"] == True


def test_gene_predictions_no_info():
    ## GIVEN a empty list of genes
    genes = []

    ## WHEN parsing the gene predictions
    res = predictions(genes)
    ## THEN assert the result is not filled
    assert res == {
        "sift_predictions": [],
        "polyphen_predictions": [],
        "region_annotations": [],
        "functional_annotations": [],
    }


def test_gene_predictions_one_gene():
    ## GIVEN a empty list of genes
    gene = {
        "sift_prediction": "deleterious",
        "polyphen_prediction": "probably_damaging",
        "region_annotation": "exonic",
        "functional_annotation": "missense_variant",
    }
    genes = [gene]

    ## WHEN parsing the gene predictions
    res = predictions(genes)
    ## THEN assert the result is not filled
    assert res == {
        "sift_predictions": ["deleterious"],
        "polyphen_predictions": ["probably_damaging"],
        "region_annotations": ["exonic"],
        "functional_annotations": ["missense_variant"],
    }


def test_gene_predictions_one_gene_no_sift():
    ## GIVEN a empty list of genes
    gene = {
        "hgnc_symbol": "AAA",
        "polyphen_prediction": "probably_damaging",
        "region_annotation": "exonic",
        "functional_annotation": "missense_variant",
    }
    genes = [gene]

    ## WHEN parsing the gene predictions
    res = predictions(genes)
    ## THEN assert the result is not filled
    assert res == {
        "sift_predictions": ["-"],
        "polyphen_predictions": ["probably_damaging"],
        "region_annotations": ["exonic"],
        "functional_annotations": ["missense_variant"],
    }


def test_gene_predictions_two_genes():
    ## GIVEN a empty list of genes
    gene = {
        "hgnc_symbol": "AAA",
        "sift_prediction": "deleterious",
        "polyphen_prediction": "probably_damaging",
        "region_annotation": "exonic",
        "functional_annotation": "missense_variant",
    }
    gene2 = {
        "hgnc_symbol": "BBB",
        "sift_prediction": "tolerated",
        "polyphen_prediction": "unknown",
        "region_annotation": "exonic",
        "functional_annotation": "synonymous_variant",
    }
    genes = [gene, gene2]

    ## WHEN parsing the gene predictions
    res = predictions(genes)
    ## THEN assert the result is not filled
    assert set(res["sift_predictions"]) == set(["AAA:deleterious", "BBB:tolerated"])


def test_sv_frequencies_empty():
    ## GIVEN a variant object with gnomad annotation
    var = {"category":"sv"}
    ## WHEN parsing the sv frequencies
    freq = frequencies(var)
    ## THEN assert the correct tuple is returned
    assert len(freq) == 1
    assert freq[0] == ("GnomAD", var.get("gnomad_frequency", "NA"), None)


def test_sv_frequencies_gnomad():
    ## GIVEN a variant object with gnomad annotation
    var = {"gnomad_frequency": 0.01, "category":"sv"}
    ## WHEN parsing the sv frequencies
    freq = frequencies(var)
    ## THEN assert the correct tuple is returned
    assert len(freq) == 1
    assert freq[0] == ("GnomAD", var.get("gnomad_frequency"), None)


def test_sv_frequencies_gnomad_exac():
    ## GIVEN a variant object with gnomad annotation
    var = {"exac_frequency": 0.01, "category":"sv"}
    ## WHEN parsing the sv frequencies
    freq = frequencies(var)
    ## THEN assert the correct tuple is returned
    assert len(freq) == 1
    assert freq[0] == ("GnomAD", var.get("exac_frequency"), None)


def test_sv_frequencies_all():
    ## GIVEN a variant object with gnomad annotation
    var = {
        "gnomad_frequency": 0.02,
        "clingen_cgh_benign": 0.02,
        "clingen_cgh_pathogenic": 0.02,
        "clingen_ngi": 0.02,
        "clingen_mip": 0.02,
        "swegen": 0.02,
        "decipher": 0.02,
        "thousand_genomes_frequency": 0.02,
        "category":"sv"
    }
    ## WHEN parsing the sv frequencies
    freq = frequencies(var)
    ## THEN assert the correct tuple is returned
    assert len(freq) == 8
    for annotation in freq:
        assert annotation[1] == 0.02
