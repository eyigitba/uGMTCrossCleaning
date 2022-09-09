# uGMTCrossCleaning

This is a simple recipe to re-emulate uGMT from its unpacked inputs for utilizing custom OMTF/EMTF cross cleaning (ghost busting) parameters.

# Simple instructions for making ntuples

To produce ntuples using the example PSET file:

```
cmsrel CMSSW_12_4_8
cd CMSSW_12_4_8/src
cmsenv
git cms-init
voms-proxy-init --voms cms --valid 24:00:00

git cms-addpkg L1Trigger/Configuration

sed -i '60i from L1Trigger.L1TMuon.fakeGmtParams_cff import *' L1Trigger/Configuration/python/SimL1Emulator_cff.py

git clone git@github.com:eyigitba/EMTFTools.git

scram b -j8

git clone git@github.com:eyigitba/uGMTCrossCleaning.git
cp uGMTCrossCleaning/emtfNtuple_reEmul_extreme.py ./

cmsRun emtfNtuple_reEmul_extreme.py

```

This will create an "EMTFNtuple" with re-emulated L1 muons, unpacked L1 muons, and RECO muons.


# More advanced instructions

If you want to just take the changes to the uGMT and re-emulate it within your framework, you can do the following.

The main changes to implement are as follows:
(note: I tested this in 12_4_8, but it should work on all releases from past 2 years at least.)

```
git cms-addpkg L1Trigger/Configuration

sed -i '60i from L1Trigger.L1TMuon.fakeGmtParams_cff import *' L1Trigger/Configuration/python/SimL1Emulator_cff.py

scram b -j8

```


This enables using the values in `fakeGmtParams_cff` instead of fetching them from LUTs.

Then in any PSET file you can add the following lines for different cross cleaning parameters and make your favorite ntuple.

```
# Get uGMT emulator
process.load('L1Trigger.L1TMuon.simGmtStage2Digis_cfi')
process.gmt_step = cms.Path(process.simGmtStage2Digis)
process.calo_sum_step = cms.Path(process.simGmtCaloSumDigis)

# Set uGMT emulator to use unpacked inputs. simGmtCaloSumDigis doesn't matter, we're just setting it to prevent crashes.
process.simGmtStage2Digis.barrelTFInput = cms.InputTag("gmtStage2Digis","BMTF")
process.simGmtStage2Digis.forwardTFInput = cms.InputTag("gmtStage2Digis","EMTF")
process.simGmtStage2Digis.overlapTFInput = cms.InputTag("gmtStage2Digis","OMTF")
process.simGmtCaloSumDigis.triggerTowerInput = cms.InputTag("caloStage2Digis", "MP")

# Run 3 firmware version is required to replicate P5 behaviour
process.gmtParams.fwVersion = cms.uint32(0x7000000)
```

There are 4 different options that we tried. These lines also should be added to the PSET file. Only use one of them :)

Names and values are taken from: http://cds.cern.ch/record/2315346/files/CERN-THESIS-2018-033.pdf (page 124)

Aggressive: This is the way it works right now at P5. 
```
# OMTF/EMTF Cross-cleaning parameters. This is "aggressive"
process.gmtParams.FOPosMatchQualLUTMaxDR  = cms.double(0.075)
process.gmtParams.FOPosMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfPhi         = cms.double(3)

process.gmtParams.FONegMatchQualLUTMaxDR        = cms.double(0.075)
process.gmtParams.FONegMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FONegMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FONegMatchQualLUTfPhi         = cms.double(3)
```

Baseline: More rate reduction than aggressive
```
# OMTF/EMTF Cross-cleaning parameters. This is "baseline"
process.gmtParams.FOPosMatchQualLUTMaxDR  = cms.double(0.1)
process.gmtParams.FOPosMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfPhi         = cms.double(1)

process.gmtParams.FONegMatchQualLUTMaxDR        = cms.double(0.1)
process.gmtParams.FONegMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FONegMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FONegMatchQualLUTfPhi         = cms.double(1)
```

Conservative: More rate reduction than baseline
```
# OMTF/EMTF Cross-cleaning parameters. This is "conservative"
process.gmtParams.FOPosMatchQualLUTMaxDR  = cms.double(0.2)
process.gmtParams.FOPosMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfPhi         = cms.double(2)

process.gmtParams.FONegMatchQualLUTMaxDR        = cms.double(0.2)
process.gmtParams.FONegMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FONegMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FONegMatchQualLUTfPhi         = cms.double(2)
```

Extreme: Custom values we chose for this test. Should be more or less similar to conservative/baseline
```
# OMTF/EMTF Cross-cleaning parameters. This is "extreme"
process.gmtParams.FOPosMatchQualLUTMaxDR  = cms.double(0.075)
process.gmtParams.FOPosMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfPhi         = cms.double(0.5)

process.gmtParams.FONegMatchQualLUTMaxDR        = cms.double(0.075)
process.gmtParams.FONegMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FONegMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FONegMatchQualLUTfPhi         = cms.double(0.5)
```


