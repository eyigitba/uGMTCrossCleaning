# HLT instructions with re-emulated GMT

Starting from a clean working area:
```
cmsrel CMSSW_12_4_8
cd CMSSW_12_4_8/src
cmsenv
git cms-init
voms-proxy-init --voms cms --valid 24:00:00

git cms-addpkg L1Trigger/Configuration
git cms-addpkg Configuration/StandardSequences

sed -i '60i from L1Trigger.L1TMuon.fakeGmtParams_cff import *' L1Trigger/Configuration/python/SimL1Emulator_cff.py

git clone git@github.com:eyigitba/uGMTCrossCleaning.git
cp uGMTCrossCleaning/HLTInstructions/SimL1EmulatorRepack_Full_cff.py ./Configuration/StandardSequences/python/

scram b -j8

cp uGMTCrossCleaning/HLTInstructions/hlt_uGMT_full.py ./

cmsRun hlt_uGMT_full.py
```

The PSET file `hlt_uGMT_full.py` is a modified version of the file obtained by the command below:
```
hltGetConfiguration /dev/CMSSW_12_4_0/GRun --globaltag 124X_dataRun3_HLT_v4 --data --unprescale --output minimal --max-events 1000 --l1-emulator Full --l1 L1Menu_Collisions2022_v1_3_0-d1_xml --input root://eoscms.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STORM/RAW/Run2022B_HLTPhysics0_run355558/cd851cf4-0fca-4d76-b80e-1d33e1371929.root  --eras Run3 > hlt_uGMT.py
```

The main idea is to start from `hltGetConfiguration --l1-emulator Full` and modify `SimL1EmulatorRepack_Full_cff` to add uGMT unpacking, switch uGMT emulator inputs to unpacked inputs, and finally add uGMT cross cleaning options in the PSET file.

If you prefer to modify the files yourself instead of using my copies, you can find the changes below.

##### `SimL1EmulatorRepack_Full_cff.py`
```
# line 77
import EventFilter.L1TRawToDigi.gmtStage2Digis_cfi
unpackGmtStage2 = EventFilter.L1TRawToDigi.gmtStage2Digis_cfi.gmtStage2Digis.clone(
    InputLabel = cms.InputTag( 'rawDataCollector', processName=cms.InputTag.skipCurrentProcess()))

## GMT
simGmtStage2Digis.barrelTFInput = cms.InputTag("unpackGmtStage2","BMTF")
simGmtStage2Digis.forwardTFInput = cms.InputTag("unpackGmtStage2","EMTF")
simGmtStage2Digis.overlapTFInput = cms.InputTag("unpackGmtStage2","OMTF")

# replace the line below with line 162 in origin file
stage2L1Trigger.toReplaceWith(SimL1EmulatorTask, cms.Task(unpackEcal,unpackHcal,unpackCSC,unpackDT,unpackRPC,unpackRPCTwinMux,unpackTwinMux,unpackOmtf,unpackEmtf,unpackCsctf,unpackBmtf, unpackGmtStage2
```

##### `hlt_uGMT_full.py`
```
## line 81408 and below L1REPACK definition
# Run 3 firmware version is required to replicate P5 behaviour
process.gmtParams.fwVersion = cms.uint32(0x7000000)

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

