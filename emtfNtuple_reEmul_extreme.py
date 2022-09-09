# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1Ntuple -s RAW2DIGI --python_filename=mc.py -n 303 --no_output --era=Run3 --mc --conditions=123X_mcRun3_2021_realistic_v11 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulMCFromRAWSimHcalTP --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMUGEN_MC --filein=/store/mc/Run3Summer21DRPremix/SingleNeutrino_Pt-2To20-gun/GEN-SIM-DIGI-RAW/SNB_120X_mcRun3_2021_realistic_v6-v2/2540000/e7186f9d-8dfb-480f-bcba-ead981805f87.root --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('RAW2DIGI',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(

'/store/data/Run2022C/Muon/RAW-RECO/ZMu-PromptReco-v1/000/357/479/00000/008d591c-314f-401c-90eb-eea22a82ba8b.root'
  ),

)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('l1Ntuple nevts:303'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun3_v9', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)

process.load('L1Trigger.L1TMuon.simGmtStage2Digis_cfi')
process.gmt_step = cms.Path(process.simGmtStage2Digis)
process.calo_sum_step = cms.Path(process.simGmtCaloSumDigis)

process.load('EMTFTools.EMTFNtuple.EMTFNtupleMaker_cfi')
process.TFileService = cms.Service('TFileService', fileName = cms.string("EMTFNtuple.root"))

process.ntuple_step = cms.Path(process.EMTFNtuple)

# Schedule definition
# process.schedule = cms.Schedule(process.raw2digi_step, process.emtf_step, process.endjob_step)
process.schedule = cms.Schedule(process.raw2digi_step, process.calo_sum_step, process.gmt_step, process.endjob_step, process.ntuple_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# End of customisation functions
process.simGmtStage2Digis.barrelTFInput = cms.InputTag("gmtStage2Digis","BMTF")
process.simGmtStage2Digis.forwardTFInput = cms.InputTag("gmtStage2Digis","EMTF")
process.simGmtStage2Digis.overlapTFInput = cms.InputTag("gmtStage2Digis","OMTF")
process.simGmtCaloSumDigis.triggerTowerInput = cms.InputTag("caloStage2Digis", "MP")


# Run 3 firmware version is required to replicate P5 behaviour
process.gmtParams.fwVersion = cms.uint32(0x7000000)

# OMTF/EMTF Cross-cleaning parameters. This is "extreme"
process.gmtParams.FOPosMatchQualLUTMaxDR  = cms.double(0.075)
process.gmtParams.FOPosMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FOPosMatchQualLUTfPhi         = cms.double(0.5)

process.gmtParams.FONegMatchQualLUTMaxDR        = cms.double(0.075)
process.gmtParams.FONegMatchQualLUTfEta         = cms.double(1)
process.gmtParams.FONegMatchQualLUTfEtaCoarse   = cms.double(1)
process.gmtParams.FONegMatchQualLUTfPhi         = cms.double(0.5)

# Settings to disable EMTF related collections and enable GMT collections for this example ntuple
process.EMTFNtuple.useEMTFTracks = False
process.EMTFNtuple.useEMTFUnpTracks = False
process.EMTFNtuple.useGMTMuons = True
process.EMTFNtuple.useGMTUnpMuons = True
process.EMTFNtuple.useGMTMuons = True
process.EMTFNtuple.useRecoMuons = True
process.EMTFNtuple.isReco = True


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
