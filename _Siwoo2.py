import PyPN
import matplotlib.pyplot as plt
from PyPN.takeTime import *
import numpy as np
import os
from pprint import pprint
import sys

# ------------------------------------------------------------------------------
# ------------------------------- SCRIPT CONTROL -------------------------------
# ------------------------------------------------------------------------------

calculationFlag = False # run simulation or load latest bundle with this parameters (not all taken into account for identification)
electricalStimulusOn = True


# ------------------------------------------------------------------------------
# --------------------------------- DEFINITION ---------------------------------
# ------------------------------------------------------------------------------

# ----------------------------- simulation params ---------------------------

tStop=30
timeRes=0.0025

# ----------------------------- bundle params -------------------------------

# set length of bundle and number of axons
lengthOfBundle = 80000 # 20000 # 400000
numberOfAxons = 1

# set the diameter distribution or fixed value
# see http://docs.scipy.org/doc/numpy/reference/routines.random.html
# 5.7, 7.3, 8.7, 10., 11.5, 12.8, 14., 15., 16.
myelinatedDiam =  0.7 # {'distName' : 'normal', 'params' : (1.0, 0.7)} # (2.0, 0.7)
unmyelinatedDiam = 0.4 # {'distName' : 'normal', 'params' : (0.7, 0.3)}

# axon definitions
myelinatedParameters = {'fiberD': myelinatedDiam}
unmyelinatedParameters = {'fiberD': unmyelinatedDiam}

# bundle guide
segmentLengthAxon = 30
bundleGuide = PyPN.createGeometry.get_bundle_guide_straight(lengthOfBundle, segmentLengthAxon)

# ----------------------------- stimulation params ---------------------------

# parameters of signals for stimulation
rectangularSignalParams = {'amplitude': .5,  # Pulse amplitude (mA)
                           'frequency': 20.,  # Frequency of the pulse (kHz)
                           'dutyCycle': 0.5,  # Percentage stimulus is ON for one period (t_ON = duty_cyle*1/f)
                           'stimDur': 0.05,  # Stimulus duration (ms)
                           'waveform': 'MONOPHASIC',  # Type of waveform either "MONOPHASIC" or "BIPHASIC" symmetric
                           'delay': 2.,  # ms
                           # 'invert': True,
                           # 'timeRes': timeRes,
                           }


intraParameters = {'stimulusSignal': PyPN.signalGeneration.rectangular(**rectangularSignalParams)}

# ----------------------------- recording params -------------------------------

recordingParametersNew = {'bundleGuide': bundleGuide,
                          'radius': 200,
                          'positionAlongBundle': 3000,
                          'numberOfPoles': 2,
                          'poleDistance': 1000,
                        }

LFPMech1 = PyPN.Extracellular.precomputedFEM(bundleGuide)
LFPMech2 = PyPN.Extracellular.homogeneous(sigma=1)
LFPMech3 = PyPN.Extracellular.precomputedFEM(bundleGuide, fieldName='corkRecording')

electrodePos = PyPN.createGeometry.circular_electrode(**recordingParametersNew)

electrodePos2 = np.ones((2,3,2))
electrodePos2[0,:,0] = [7000, -219, 0]
electrodePos2[0,:,1] = [12000, -219, 0]
electrodePos2[1,:,0] = [7010, -219, 0]
electrodePos2[1,:,1] = [12010, -219, 0]

modularRecMech1 = PyPN.RecordingMechanism(electrodePos, LFPMech1)
modularRecMech2 = PyPN.RecordingMechanism(electrodePos, LFPMech2)
modularRecMech3 = PyPN.RecordingMechanism(electrodePos2, LFPMech3)


# ------------------------------------------------------------------------------
# ---------------------------------- CALCULATION -------------------------------
# ------------------------------------------------------------------------------


if calculationFlag:

    for randomComponent in np.arange(0, 0.1, 0.1):

        # set all properties of the bundle
        bundleParameters = {'radius': 300,  # 150, #um Radius of the bundle (typically 0.5-1.5mm)
                            'length': lengthOfBundle,  # um Axon length
                            # 'randomDirectionComponent': .9,
                            # 'bundleGuide': bundleGuide,

                            'numberOfAxons': numberOfAxons,  # Number of axons in the bundle
                            'pMyel': 0.,  # Percentage of myelinated fiber type A
                            'pUnmyel': 1.,  # Percentage of unmyelinated fiber type C
                            'paramsMyel': myelinatedParameters,  # parameters for fiber type A
                            'paramsUnmyel': unmyelinatedParameters,  # parameters for fiber type C

                            'tStop': tStop,
                            'timeRes': 0.0025, #'variable', #

                            # 'saveI':True,
                            # 'saveV': False,
                            'saveLocation': '/media/carl/4ECC-1C44/PyPN/',

                            'numberOfSavedSegments': 50,
                            # number of segments of which the membrane potential is saved to disk
                            }

        # create the bundle with all properties of axons and recording setup
        bundle = PyPN.Bundle(**bundleParameters)

        # spiking through a single electrical stimulation
        if electricalStimulusOn:
            bundle.add_excitation_mechanism(PyPN.StimIntra(**intraParameters))

        # bundle.add_recording_mechanism(PyPN.FEMRecCuff2D(**recordingParameters))
        # bundle.add_recording_mechanism(PyPN.RecCuff2D(**recordingParameters))
        # bundle.add_recording_mechanism(PyPN.FEMRecCuff2D(**recordingParametersBip))
        # bundle.add_recording_mechanism(PyPN.RecCuff2D(**recordingParametersBip))

        bundle.add_recording_mechanism(modularRecMech1)
        bundle.add_recording_mechanism(modularRecMech2)
        bundle.add_recording_mechanism(modularRecMech3)

        # PyPN.plot.geometry_definition(bundle)
        # plt.show()

        # run the simulation
        bundle.simulate()

        t, v = bundle.get_voltage_from_file_one_axon(0)
        plt.plot(t,v[:,30])
        plt.show()

        # # get SFAP
        # time, CAP = bundle.get_CAP_from_file()
        # plt.plot(time, CAP)

        # save the bundle to disk
        PyPN.save_bundle(bundle)
else:

    # try to open a bundle with the parameters set above
    # bundle = PyPN.open_recent_bundle(bundleParameters)
    # bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=100 pMyel=0.1 pUnmyel=0.9 L=20000 nAxons=500/bundle00000')
    # bundle = PyPN.open_bundle_from_location('/media/carl/4ECC-1C44/PyPN/dt=0.0025 tStop=100 pMyel=0.1 pUnmyel=0.9 L=20000 nAxons=500/bundle00001')
    bundle = PyPN.open_bundle_from_location(
        '/media/carl/4ECC-1C44/Siwoo Data/Myelinated/dt=0.0025 tStop=50 pMyel=1.0 pUnmyel=0.0 L=100000 nAxons=50')

# ------------------------------------------------------------------------------
# ---------------------------------- PLOTTING ----------------------------------
# ------------------------------------------------------------------------------

print '\nStarting to plot'

# # pp = pprint.PrettyPrinter(indent=4)
# # pp.pprint(bundle)
# pprint (vars(bundle))
# # for axon in bundle.axons:
# #     # print axon.nbytes
# #     pprint (vars(axon))
# pprint(vars(bundle.axons[0]))
# pprint(vars(bundle.recordingMechanisms[0]))




# first load the desired data from file
for i in range(len(bundle.recordingMechanisms)):
    time, CAP = bundle.get_CAP_from_file(i)
    plt.plot(time, CAP, label='recMech'+str(i))
plt.legend()



# # # # PyPN.plot.geometry_definition(bundle)
# PyPN.plot.CAP1D(bundle)
# PyPN.plot.CAP1D(bundle, recMechIndex=1)
# PyPN.plot.CAP1D(bundle, recMechIndex=2)
# PyPN.plot.CAP1D(bundle, recMechIndex=3)

# plt.figure()
# time, CAP = bundle.get_CAP_from_file(0)
# plt.plot(time, CAP[-1,:], label='FEM')
# time, CAP = bundle.get_CAP_from_file(1)
# plt.plot(time, CAP[-1,:]/2*0.3, label='homogeneous')
# plt.xlabel('time [ms]')
# plt.ylabel('voltage [mV]')
# plt.legend()
# plt.tight_layout()
#
# plt.figure()
# time, CAP = bundle.get_CAP_from_file(2)
# plt.plot(time, CAP[-1,:], label='FEM')
# time, CAP = bundle.get_CAP_from_file(3)
# plt.plot(time, CAP[-1,:]/2*0.3, label='homogeneous')
# plt.xlabel('time [ms]')
# plt.ylabel('voltage [mV]')
# plt.legend()
# plt.tight_layout()
#
# plt.figure()
# time, CAP = bundle.get_CAP_from_file(0)
# plt.plot(time, CAP[-1,:], label='FEM monopolar')
# time, CAP = bundle.get_CAP_from_file(2)
# plt.plot(time, CAP[-1,:]/2*0.3, label='FEN bipolar')
# plt.xlabel('time [ms]')
# plt.ylabel('voltage [mV]')
# plt.legend()
# plt.tight_layout()

# t, CAP = bundle.get_CAP_from_file()
# np.save(os.path.join('/media/carl/4ECC-1C44/PyPN/FEM_CAPs/forPoster', 'homogeneous2.npy'), [t, CAP])


# PyPN.plot.CAP1D(bundle, recMechIndex=1)
PyPN.plot.voltage(bundle)
# PyPN.plot.diameterHistogram(bundle)
plt.show()

bundle = None