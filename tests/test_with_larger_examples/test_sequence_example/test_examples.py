import pytest
from pillowtalk import *

# TODO: test when where returns [] or None or [None]
# TODO: test update() (or autoupdate?)

@pytest.fixture
def folder_json():
    return {'count'                                                                             : 59,
 'created_at'                                                                        : '2013-10-01T20:07:18+00:00',
 'description'                                                                       : '', 'id': 'lib_pP6d50rJn1',
 'modified_at'                                                                       : '2017-01-20T21:57:55.991758+00:00',
 'name'                                                                              : 'Plasmids',
 'owner'                                                                             : 'ent_A7BlnCcJTU',
 'permissions'                                                                       : {'admin'     : True,
                                                                                        'appendable': True,
                                                                                        'owner'     : False,
                                                                                        'readable'  : True,
                                                                                        'writable'  : True},
 'sequences'                                                                         : [
     {'id': 'seq_Nv6wYspV', 'name': 'FAR1-mut-87aa-TP'}, {'id': 'seq_0FmHFzJe', 'name': 'pMODT4-pGAL1-attB1-GAVNY'},
     {'id': 'seq_usn0K27s', 'name': 'pMODU6-pGALZ4-BleoMX'},
     {'id': 'seq_Na2oNxzs', 'name': 'pMODU6-pGALZ4-FAR1-mut-87aa'},
     {'id': 'seq_AyQ7ToIn', 'name': 'pBR322 (Sample Sequence)'},
     {'id': 'seq_QuWMpfRK', 'name': 'pMODT4-pGAL1-attB1-GVNY'}, {'id': 'seq_K5hwGNwg', 'name': 'pMODU6-pGAL1-BleoMX'},
     {'id': 'seq_2rKmILGU', 'name': 'pMODU6-pGAL1-NatMX'}, {'id': 'seq_5HcRWKi8', 'name': 'pMODU6-pGALZ4-P1G1-HygMX'},
     {'id': 'seq_tMz0Xv3g', 'name': 'pMODU6-pGAL1-FAR1-L1-IAA17T2'},
     {'id': 'seq_k0MuYdIM', 'name': 'pMODU6-pGAL1-IAA17T2-FAR1'},
     {'id': 'seq_fkFjzKkb', 'name': 'v63_pGP8zGAL-STE5(-)RING-SNC2 C-term'},
     {'id': 'seq_WQ0wqb9f', 'name': 'pMODU6-pGALZ4-iaaH'}, {'id': 'seq_hhI5TTbO', 'name': 'pMODU6-pGAL1-FAR1-IAA17T2'},
     {'id': 'seq_beOWphBv', 'name': 'pMODKan-HO-pACT1-ZEV4'},
     {'id': 'seq_QteKmJdS', 'name': 'pGPT4-pGAL1-GAVNY_mutated_library'},
     {'id': 'seq_w2IZPFzd', 'name': 'pMODOK-pACT1-GAVNY'}, {'id': 'seq_AgQ1w9ak', 'name': 'pLAB2'},
     {'id': 'seq_kKtPZ1Rs', 'name': 'pMODT4-pGAL1-P1G1-GAVNY'}, {'id': 'seq_4ccBmI1j', 'name': 'pGPU6-pGAL1-AFB2'},
     {'id': 'seq_wHiaXdFM', 'name': 'pGPT4-pGAL1-G(m)AVNY'}, {'id': 'seq_QGfqobtP', 'name': 'pGPT4-pGAL1-AVNY'},
     {'id': 'seq_VazadBJw', 'name': 'pGPT4-pGAL1-GAVNY'}, {'id': 'seq_Qc6f2Kii', 'name': 'pMOD4G-NLS_dCas9_VP64'},
     {'id': 'seq_SGfG2YeB', 'name': 'pMODU6-pGALZ4-HygMX'}, {'id': 'seq_i0Yl6uzk', 'name': 'pMODH8-pGPD-TIR1_DM'},
     {'id': 'seq_ri07UntS', 'name': 'pMODU6-pGPD-EYFP'}, {'id': 'seq_F4tEc0XU', 'name': 'pMODU6-pGALZ4-STE5(-)RING'},
     {'id': 'seq_qihkmlW4', 'name': 'pMODU6-pGAL1-AlphaFactor'},
     {'id': 'seq_2MFFshfl', 'name': 'pYMOD2Kmx_pGAL1-HYG_ZEV4-cassette'},
     {'id': 'seq_bw3XWuZU', 'name': 'pMODT4-pGALZ4-AVNY'}, {'id': 'seq_D1iAdKMz', 'name': 'pGPL5G-pGAL1-URA3'},
     {'id': 'seq_rzQGBzv2', 'name': 'pGP5G-ccdB'}, {'id': 'seq_9ph0SnJV', 'name': 'AmpR-T4-pGAL1-GAL4DBD-L1'},
     {'id': 'seq_PKJNfuZA', 'name': 'pGPH8-pGAL1-GAVNY_v2'}, {'id': 'seq_m42PVReQ', 'name': 'pMODT4-pGALZ4-Z4AVNY'},
     {'id': 'seq_5bmPzcKN', 'name': 'pMODU6-pGALZ4-NatMX'}, {'id': 'seq_mfMW58Dd', 'name': 'pGPL5G-pGALZ4-URA3'},
     {'id': 'seq_l5VHTc8Z', 'name': 'pGPU6-pGAL1-TIR1_DM'}, {'id': 'seq_tFGIIL0C', 'name': 'pMODU6-pGAL1-FAR1'},
     {'id': 'seq_y9xdtVx7', 'name': 'pMODKan-HO-pACT1GEV'}, {'id': 'seq_t77GYXRB', 'name': 'pGPT4-pGAL1-EGFP'},
     {'id': 'seq_TWAJLtvz', 'name': 'pMODU6-pGAL1-P1G1-HygMX'}, {'id': 'seq_ztl4dnOW', 'name': 'pLAB1'},
     {'id': 'seq_TsTM0B8q', 'name': 'pMOD4-pGAL1Z3(P3)-MF(AL'}, {'id': 'seq_UbsucV1t', 'name': 'pMODU6-pGAL1-HygMX'},
     {'id': 'seq_7O7ThYSI', 'name': 'pMODU6-pGALZ4-Z4AVNY'}, {'id': 'seq_iGdjEEx4', 'name': 'pGPT4-pGAL1-P1G1-GEV'},
     {'id': 'seq_2xGw2yCj', 'name': 'pGPH8-pGAL1-GAVNY'}, {'id': 'seq_okitCPyx', 'name': 'pGPT4-pGAL1-GAVNY(VP64)'},
     {'id': 'seq_rwDoRd9Q', 'name': 'pMODU6-pGALZ4-FAR1'},
     {'id': 'seq_f4GgnFdY', 'name': 'pGPT4-pGAL1-GAVNY_seq_verified'},
     {'id': 'seq_5AXMlSvB', 'name': 'pYMOD2Kmx_pGAL1-HYG_pGAL1-iaah'},
     {'id': 'seq_6VN5FDpP', 'name': 'pMODOK-pACT1-GAVN'}, {'id': 'seq_etTsAfD4', 'name': 'pGPU6-pGALZ4-eYFP'},
     {'id': 'seq_IyZI9bEh', 'name': 'pMODU6-pGAL1-FAR1-L1-IAA17T1_opt'}, {'id': 'seq_7yXay7Ep', 'name': 'pGP8G-TIR1-Y'},
     {'id': 'seq_GuqSGBXY', 'name': 'pGPT4-pGAL1-GAVNY(VP64) new design'},
     {'id': 'seq_vA5dxrqd', 'name': 'pMODU6-pGALZ4-AlphaFactor'}], 'type'            : 'ALL'}

def test_folder(folder_json):
    class MyBase(MarshpillowBase):

        def find(self, *args, **kwargs):
            pass

        def where(self, *args, **kwargs):
            pass

    @add_schema
    class Folder(MyBase):
        items = {}

        FIELDS = ["id", "name"]
        RELATIONSHIPS = [
            Many("sequences", "where Folder.id <> Sequence.folder")
        ]

    @add_schema
    class Sequence(MyBase):
        items = {}

        FIELDS = ["id", "name", "bases"]
        RELATIONSHIPS = [
            One("folder", "find Sequence.folder <> Folder.id"),
        ]

    f = Folder.load(folder_json)
    assert len(f.sequences) > 1