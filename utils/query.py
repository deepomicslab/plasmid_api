from phage.models import phage
from phage_protein.models import phage_protein_NCBI, phage_protein_PhagesDB, phage_protein_GPD, phage_protein_MGV, phage_protein_TemPhD, phage_protein_GVD
from phage_protein.serializers import phage_protein_GPD_Serializer, phage_protein_GVD_Serializer, phage_protein_MGV_Serializer, phage_protein_NCBI_Serializer, phage_protein_PhagesDB_Serializer, phage_protein_TemPhD_Serializer

def findphageprotein(phageid):
    """
    Find phage protein in database
    """
    phages = phage.objects.get(Acession_ID=phageid)
    if phages.Data_Sets.id <= 5:
        proteins = phage_protein_NCBI.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_NCBI_Serializer(proteins, many=True)
    elif phages.Data_Sets.id == 6:
        proteins = phage_protein_PhagesDB.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_PhagesDB_Serializer(proteins, many=True)
    elif phages.Data_Sets.id == 7:
        proteins = phage_protein_GPD.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_GPD_Serializer(proteins, many=True)
    elif phages.Data_Sets.id == 8:
        proteins = phage_protein_GVD.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_GVD_Serializer(proteins, many=True)
    elif phages.Data_Sets.id == 9:
        proteins = phage_protein_MGV.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_MGV_Serializer(proteins, many=True)
    elif phages.Data_Sets.id == 10:
        proteins = phage_protein_TemPhD.objects.filter(
            Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_protein_TemPhD_Serializer(proteins, many=True)
    return serializer.data
